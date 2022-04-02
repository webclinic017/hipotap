#!/usr/bin/env python3

from app import app
from flask import render_template
import pika
import sys


@app.route('/')
def index():
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('hipotap_brocker',
                                            5672,
                                            '/',
                                            credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    message = 'Hello World!'
    channel.basic_publish(exchange='',
            routing_key='hello',
            body=message)
    print(f"Message '{message}' sent.", file=sys.stdout)
    sys.stdout.flush()

    connection.close()
    return render_template('index.html')
#    return "hello world!"
