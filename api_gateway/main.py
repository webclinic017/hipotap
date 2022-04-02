from multiprocessing import connection
from fastapi import FastAPI
import pika
import sys, time
from hipotap_common.models.customer import CustomerCredentials
from rpc.customer_rpc_client import CustomerRpcClient
CUSTOMER_AUTH_QUEUE = 'customer_auth'

app = FastAPI()

time.sleep(5)

def boker_connection():
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('hipotap_broker',
                                            5672,
                                            '/',
                                            credentials)
    return pika.BlockingConnection(parameters)

connection = boker_connection()

responses = {}

def on_service_response(ch, method, properties, body):
    global reply
    print(" [x] Received %r from CUSTOMER_SERVICE" % body)
    reply = body.decode("utf-8")
    ch.close()

@app.get("/customer/authenticate/")
async def root(email: str, password: str):
    print("Got [GET]/]")
    sys.stdout.flush()
    customer_client = CustomerRpcClient()
    response = customer_client.authenticate(CustomerCredentials(email, password))
    # channel = connection.channel()

    # consumer_tag = channel.basic_consume('amq.rabbitmq.reply-to',
    #                           on_service_response,
    #                           auto_ack=True)
    # channel.basic_publish(
    #     exchange='',
    #     routing_key=CUSTOMER_AUTH_QUEUE,
    #     body='Marco',
    #     properties=pika.BasicProperties(reply_to='amq.rabbitmq.reply-to'))
    # channel.start_consuming()

    return {"reply": f"{response}"}
