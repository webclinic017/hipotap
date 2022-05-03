from sqlalchemy.orm.exc import NoResultFound
import pika

from hipotap_common.queues.offer_queues import (
    OFFER_LIST_QUEUE
)
from hipotap_common.proto_messages.offer_pb2 import OfferListPB, OfferPB
from hipotap_common.broker import connect_to_brocker
from offer_db.models import db_session, Offer_Table

def broker_requests_handling_loop():
    connection = connect_to_brocker()
    channel = connection.channel()
    # Declare queues
    channel.queue_declare(queue=OFFER_LIST_QUEUE)

    channel.basic_consume(
        queue=OFFER_LIST_QUEUE,
        auto_ack=True,
        on_message_callback=on_offer_list_request,
    )

    # Start handling requests
    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


def on_offer_list_request(ch, method, properties, body):
    print(" [x] Offer list requested")

    offer_list_response_pb = OfferListPB()

    try:
        offers = (
            db_session.query(Offer_Table)
        )

        for offer in offers:
            elem = OfferPB()
            elem.id = offer.id
            elem.title = offer.title
            offer_list_response_pb.offers.append(elem)

    except NoResultFound:
        print("No offers in database")

    # Send response
    ch.basic_publish(
        "",
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(correlation_id=properties.correlation_id),
        body=offer_list_response_pb.SerializeToString(),
    )
