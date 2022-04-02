#!/usr/bin/env python3

from app import app
from flask import render_template
import pika
import sys
from app.auth import restricted

@app.route('/')
# @restricted(access_level="user")
# @restricted("user")
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

@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/logout')
def logout():
    return render_template('login.html')
