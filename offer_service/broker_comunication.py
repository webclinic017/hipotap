import pika
from hipotap_common.broker import connect_to_brocker
from hipotap_common.proto_messages.offer_pb2 import OfferListPB, OfferPB, OfferRequestPB
from hipotap_common.queues.offer_queues import OFFER_LIST_QUEUE, OFFER_QUEUE
from hipotap_common.rpc.rpc_subscriber import RpcSubscriber
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from hipotap_common.db import Offer_Table, db_session


def broker_requests_handling_loop():
    subscriber = RpcSubscriber()
    subscriber.subscribe_to_queue(OFFER_LIST_QUEUE, on_offer_list_request)
    subscriber.subscribe_to_queue(OFFER_QUEUE, on_offer_request)
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

        # offer_pb.id = offer.id
        # offer_pb.title = offer.title
        # offer_pb.description = offer.description
        # offer_pb.place = offer.place
        # offer_pb.max_adult_count = offer.max_adult_count
        # offer_pb.max_children_count = offer.max_children_count
        # offer_pb.price_adult = offer.price_adult
        # offer_pb.price_children = offer.price_children

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
