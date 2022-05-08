import pika
import time


MAX_CONNECTION_ATTEMPTS = 100


def connect_to_brocker():
    credentials = pika.PlainCredentials("guest", "guest")
    parameters = pika.ConnectionParameters("hipotap_broker", 5672, "/", credentials)
    for i in range(MAX_CONNECTION_ATTEMPTS):
        try:
            connection = pika.BlockingConnection(parameters)
            return connection
        except pika.exceptions.AMQPConnectionError:
            print(
                f"Failed to connect to broker, retrying in 1 second ... [{i+1}/{MAX_CONNECTION_ATTEMPTS}]"
            )
            time.sleep(1)

    raise Exception("Broker server is not available")
