import pika
import time


MAX_CONNECTION_ATTEMPTS = 100


def connect_to_brocker():
    credentials = pika.PlainCredentials("guest", "guest")
    parameters = pika.ConnectionParameters("broker", 5672, "/", credentials)
    counter = 1
    while True:
        try:
            connection = pika.BlockingConnection(parameters)
            return connection
        except Exception as e:
            print(
                f"Failed to connect to broker, retrying in 1 second ... [{counter}]"
            )
            print(e)
            counter += 1
            time.sleep(1)

    raise Exception("Broker server is not available")
