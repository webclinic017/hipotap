import pika
from hipotap_common.proto_messages.hipotap_pb2 import BaseResponsePB, BaseStatus
from hipotap_common.proto_messages.offer_pb2 import OfferListPB, OfferPB, OfferRequestPB
from hipotap_common.proto_messages.order_pb2 import OrderRequestPB
from hipotap_common.queues.offer_queues import (
    OFFER_LIST_QUEUE,
    OFFER_QUEUE,
    VALIDATE_ORDER_QUEUE,
)
from hipotap_common.rpc.rpc_subscriber import RpcSubscriber
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from hipotap_common.db import Offer_Table, db_session


def broker_requests_handling_loop():
    subscriber = RpcSubscriber()
    subscriber.subscribe_to_queue(OFFER_LIST_QUEUE, on_offer_list_request)
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
