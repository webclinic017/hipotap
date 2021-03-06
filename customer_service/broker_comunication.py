import pika
from hipotap_common.proto_messages.auth_pb2 import AuthResponsePB, AuthStatus
from hipotap_common.proto_messages.customer_pb2 import CustomerCredentialsPB, CustomerPB
from hipotap_common.proto_messages.hipotap_pb2 import BaseResponsePB, BaseStatus
from hipotap_common.queues.customer_queues import (
    CUSTOMER_AUTH_QUEUE,
    CUSTOMER_REGISTER_QUEUE,
)
from hipotap_common.rpc.rpc_subscriber import RpcSubscriber
from sqlalchemy.orm.exc import NoResultFound

from hipotap_common.db import Customer_Table, db_session


def broker_requests_handling_loop():
    subscriber = RpcSubscriber()
    subscriber.subscribe_to_queue(CUSTOMER_AUTH_QUEUE, on_auth_request)
    subscriber.subscribe_to_queue(CUSTOMER_REGISTER_QUEUE, on_register_request)
    subscriber.handling_loop()


def on_auth_request(ch, method, properties, body):
    print(f" [x] Received body: {body}")
    # Parse received message
    customer_credentials = CustomerCredentialsPB()
    customer_credentials.ParseFromString(body)

    print(f" [x] Received Customer credentials: {customer_credentials}")
    response = AuthResponsePB()
    # Check if customer exists
    try:
        customer = (
            db_session.query(Customer_Table)
            .filter_by(
                email=customer_credentials.email, password=customer_credentials.password
            )
            .one()
        )
        response.status = AuthStatus.OK
        response.customer_data.name = customer.name
        response.customer_data.surname = customer.surname

    except NoResultFound:
        print("No such customer")
        response.status = AuthStatus.INVALID_CREDENTIALS
        response.customer_data.name = None

    # Send response
    ch.basic_publish(
        "",
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(correlation_id=properties.correlation_id),
        body=response.SerializeToString(),
    )


def on_register_request(ch, method, properties, body):
    print(f" [x] Received body: {body}")
    customer_pb = CustomerPB()
    customer_pb.ParseFromString(body)

    print(f" [x] Received Customer: {customer_pb}")

    response_pb = BaseResponsePB()
    try:
        customer = db_session.add(
            Customer_Table(
                email=customer_pb.credentials.email,
                name=customer_pb.data.name,
                surname=customer_pb.data.surname,
                password=customer_pb.credentials.password,
            )
        )
        response_pb.status = BaseStatus.OK
    except:
        print("Customer already exists")
        response_pb.status = BaseStatus.FAIL

    ch.basic_publish(
        "",
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(correlation_id=properties.correlation_id),
        body=response_pb.SerializeToString(),
    )
