#!/usr/bin/env python3

import pika, os, sys, time

def main():
    print("TRIP SERIVCE STARTED")
    time.sleep(5)
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('hipotap_broker',
                                            5672,
                                            '/',
                                            credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    channel.basic_consume(queue='hello',
            auto_ack=True,
            on_message_callback=callback)


    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
