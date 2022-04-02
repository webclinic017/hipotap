#!/usr/bin/env python3

from asyncio import queues
import pika, os, sys, time

# from customer_queues import CUSTOMER_AUTH_QUEUE
from hipotap_common.queues.customer_queues import CUSTOMER_AUTH_QUEUE
from hipotap_common.models.customer import CustomerCredentials

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
        ch.basic_publish('', routing_key=properties.reply_to,
                         properties=pika.BasicProperties(correlation_id = \
                                                         properties.correlation_id),
                         body='Aloha')
        # ch.basic_ack(delivery_tag=method_frame.delivery_tag)


def main():
    print("Customer SERIVCE STARTED")
    time.sleep(5)
    broker_requests_handling_loop()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
