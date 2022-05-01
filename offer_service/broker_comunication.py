from sqlalchemy.orm.exc import NoResultFound
import pika

from hipotap_common.queues.offer_queues import (
    OFFERS_QUEUE
)
from hipotap_common.proto_messages.offer_pb2 import OfferListPB, OfferPB
from hipotap_common.proto_messages.hipotap_pb2 import BaseResponsePB, BaseStatus
from customer_db.models import db_session, Offer_Table


def boker_connection():
    credentials = pika.PlainCredentials("guest", "guest")
    parameters = pika.ConnectionParameters("hipotap_broker", 5672, "/", credentials)
    return pika.BlockingConnection(parameters)


def broker_requests_handling_loop():
    connection = boker_connection()
    channel = connection.channel()
    # Declare queues
    channel.queue_declare(queue=OFFERS_QUEUE)

    channel.basic_consume(
        queue=OFFERS_QUEUE,
        auto_ack=True,
        on_message_callback=on_offers_request,
    )

    # Start handling requests
    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


def on_offers_request(ch, method, properties, body):
    print(" [x] Offers requested")

    offers_response_pb = OfferListPB()

    try:
        offers = (
            db_session.query(Offer_Table)
        )

        for offer in offers:
            elem = OfferPB()
            elem.title = offer.title
            offers_response_pb.offers.append(elem)

    except NoResultFound:
        print("No offers in database")

    # Send response
    ch.basic_publish(
        "",
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(correlation_id=properties.correlation_id),
        body=offers_response_pb.SerializeToString(),
    )
