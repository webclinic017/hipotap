import pika
import datetime
from hipotap_common.proto_messages.hipotap_pb2 import BaseResponsePB, BaseStatus
from hipotap_common.proto_messages.offer_pb2 import OfferListPB, OfferPB, OfferRequestPB, OfferFilterPB
from hipotap_common.proto_messages.order_pb2 import OrderRequestPB
from hipotap_common.queues.offer_queues import (
    OFFER_LIST_QUEUE,
    OFFER_QUEUE,
    OFFER_FILTERING_QUEUE,
    VALIDATE_ORDER_QUEUE,
)
from hipotap_common.rpc.rpc_subscriber import RpcSubscriber
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.sql import extract, func

from hipotap_common.db import Offer_Table, db_session


def broker_requests_handling_loop():
    subscriber = RpcSubscriber()
    subscriber.subscribe_to_queue(OFFER_LIST_QUEUE, on_offer_list_request)
    subscriber.subscribe_to_queue(OFFER_FILTERING_QUEUE, on_offer_filter_request)
    subscriber.subscribe_to_queue(OFFER_QUEUE, on_offer_request)
    subscriber.subscribe_to_queue(VALIDATE_ORDER_QUEUE, validate_offer)
    subscriber.handling_loop()


def on_offer_list_request(ch, method, properties, body):
    print(" [x] Offer list requested")

    offer_list_response_pb = OfferListPB()

    try:
        offers = db_session.query(Offer_Table)

        for offer in offers:
            offer_list_response_pb.offers.append(offer.to_pb())

    except NoResultFound:
        print("No offers in database")

    # Send response
    ch.basic_publish(
        "",
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(correlation_id=properties.correlation_id),
        body=offer_list_response_pb.SerializeToString(),
    )


def timestamp_to_datetime(timestamp):
    return datetime.datetime.fromtimestamp(timestamp.seconds + timestamp.nanos/1e9)


def on_offer_filter_request(ch, method, properties, body):
    print(" [x] Offer list filtered requested")

    offer_filter_pb = OfferFilterPB()
    offer_filter_pb.ParseFromString(body)

    offer_list_response_pb = OfferListPB()

    try:
        filters = []
        if offer_filter_pb.use_allowed_adult_count:
            filters.append(Offer_Table.max_adult_count >= offer_filter_pb.allowed_adult_count)
        if offer_filter_pb.use_allowed_children_count:
            filters.append(Offer_Table.max_children_count >= offer_filter_pb.allowed_children_count)
        if offer_filter_pb.use_max_adult_price:
            filters.append(Offer_Table.max_adult_count > 0)
            filters.append(Offer_Table.price_adult <= offer_filter_pb.max_adult_price)
        if offer_filter_pb.use_max_children_price:
            filters.append(Offer_Table.max_children_count > 0)
            filters.append(Offer_Table.price_children <= offer_filter_pb.max_children_price)
        if offer_filter_pb.use_place:
            filters.append(func.lower(Offer_Table.place).contains(offer_filter_pb.place.lower()))
        if offer_filter_pb.use_hotel:
            filters.append(func.lower(Offer_Table.hotel).contains(offer_filter_pb.hotel.lower()))
        if offer_filter_pb.use_date_start:
            filters.append(extract('day', Offer_Table.date_start) == timestamp_to_datetime(offer_filter_pb.date_start).day)
            filters.append(extract('month', Offer_Table.date_start) == timestamp_to_datetime(offer_filter_pb.date_start).month)
            filters.append(extract('year', Offer_Table.date_start) == timestamp_to_datetime(offer_filter_pb.date_start).year)
        if offer_filter_pb.use_date_end:
            filters.append(extract('day', Offer_Table.date_end) == timestamp_to_datetime(offer_filter_pb.date_end).day)
            filters.append(extract('month', Offer_Table.date_end) == timestamp_to_datetime(offer_filter_pb.date_end).month)
            filters.append(extract('year', Offer_Table.date_end) == timestamp_to_datetime(offer_filter_pb.date_end).year)

        offers = db_session.query(Offer_Table).filter(*filters)

        for offer in offers:
            offer_list_response_pb.offers.append(offer.to_pb())

    except NoResultFound:
        print("No offers in database")

    # Send response
    ch.basic_publish(
        "",
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(correlation_id=properties.correlation_id),
        body=offer_list_response_pb.SerializeToString(),
    )


def on_offer_request(ch, method, properties, body):
    print(" [x] Offer requested")

    offer_request_pb = OfferRequestPB()
    offer_request_pb.ParseFromString(body)
    offer_id = offer_request_pb.offer_id

    offer_pb = OfferPB()

    try:
        offer = db_session.query(Offer_Table).filter_by(id=offer_id).one()
        offer_pb = offer.to_pb()
    except MultipleResultsFound:
        print("Multiple offers with such id - how is that even possible?")
    except NoResultFound:
        print("No such offer in database")

    # Send response
    ch.basic_publish(
        "",
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(correlation_id=properties.correlation_id),
        body=offer_pb.SerializeToString(),
    )


def validate_offer(ch, method, properties, body):
    print(" [x] Offer validation requested")

    order_request_pb = OrderRequestPB()
    order_request_pb.ParseFromString(body)
    offer_id = order_request_pb.offer_id

    response_pb = BaseResponsePB()
    try:
        offer = db_session.query(Offer_Table).filter_by(id=offer_id).one()
        response_pb.status = BaseStatus.OK
        response_pb.message.CopyFrom(offer.to_any())
    except MultipleResultsFound:
        print("Multiple offers with such id - how is that even possible?")
        response_pb.status = BaseStatus.FAIL
        response_pb.message = f"Multiple offers with id = {offer_id}"
    except NoResultFound:
        print("No such offer in database")
        response_pb.status = BaseStatus.FAIL
        response_pb.message = f"No offer in database with id = {offer_id}"

    # Send response
    ch.basic_publish(
        "",
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(correlation_id=properties.correlation_id),
        body=response_pb.SerializeToString(),
    )
