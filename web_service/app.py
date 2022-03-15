#!/usr/bin/env python3

from flask import Flask
import pika
import sys

app = Flask(__name__)

@app.route('/')
def hello_world():
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('hipotap_brocker',
                                            5672,
                                            '/',
                                            credentials)
    connection = pika.BlockingConnection(parameters)
    # connection = pika.BlockingConnection(pika.ConnectionParameters('hipotap_brocker'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')
    channel.basic_publish(exchange='',
            routing_key='hello',
            body='Hello world')
    print("Message sent", file=sys.stdout)

    connection.close()
    return 'Hello, Docker!'


