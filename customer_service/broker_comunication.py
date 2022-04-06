from sqlalchemy.orm.exc import NoResultFound
import pika

from hipotap_common.queues.customer_queues import CUSTOMER_AUTH_QUEUE
from hipotap_common.models.customer import CustomerCredentials, CustomerData
from hipotap_common.models.auth import AuthResponse
from hipotap_common.proto_messages.auth_pb2 import AuthStatus
from customer_db.models import db_session, Customer_Table

def boker_connection():
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('hipotap_broker',
                                            5672,
                                            '/',
                                            credentials)
    return pika.BlockingConnection(parameters)


def broker_requests_handling_loop():
    connection = boker_connection()
    channel = connection.channel()
    # Declare queues
    channel.queue_declare(queue=CUSTOMER_AUTH_QUEUE)

    # Subscribe to queues
    channel.basic_consume(queue=CUSTOMER_AUTH_QUEUE,
            auto_ack=True,
            on_message_callback=on_auth_request)

    # Start handling requests
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


def on_auth_request(ch, method, properties, body):
        print(f" [x] Received body: {body}")
        customer_credentials = CustomerCredentials.deserialize(body)
        print(f" [x] Received Customer credentials: {customer_credentials}")

        try:
            customer = db_session.query(Customer_Table) \
                                 .filter_by(email = customer_credentials.email,
                                            password = customer_credentials.password) \
                                 .one()
            response = AuthResponse(AuthStatus.OK, CustomerData(name=customer.name, surname=customer.surname)).serialize()
        except NoResultFound:
            print("No such customer")
            response = AuthResponse(AuthStatus.INVALID_CREDENTIALS, None).serialize()

        ch.basic_publish('', routing_key=properties.reply_to,
                         properties=pika.BasicProperties(correlation_id = \
                                                         properties.correlation_id),
                         body=response)
        # ch.basic_ack(delivery_tag=method_frame.delivery_tag)
