import time
import pika
from hipotap_common.proto_messages.auth_pb2 import AuthResponsePB, AuthStatus
from hipotap_common.proto_messages.customer_pb2 import CustomerCredentialsPB, CustomerPB
from hipotap_common.proto_messages.hipotap_pb2 import BaseResponsePB, BaseStatus
from hipotap_common.proto_messages.order_pb2 import PaymentInfoPB
from hipotap_common.queues.payment_queues import AUTHORIZE_PAYMENT_QUEUE, RETURN_PAYMENT_QUEUE
from hipotap_common.rpc.rpc_subscriber import RpcSubscriber
from sqlalchemy.orm.exc import NoResultFound

from hipotap_common.db import Customer_Table, db_session


def broker_requests_handling_loop():
    subscriber = RpcSubscriber()
    subscriber.subscribe_to_queue(AUTHORIZE_PAYMENT_QUEUE, on_authorize_payment_request)
    subscriber.subscribe_to_queue(RETURN_PAYMENT_QUEUE, on_return_payment_request)
    subscriber.handling_loop()


def on_authorize_payment_request(ch, method, properties, body):
    payment_info_pb = PaymentInfoPB()
    payment_info_pb.ParseFromString(body)

    print(f" [x] Received Authorize payment request with: {payment_info_pb}")

    response_pb = BaseResponsePB()

    animation = [".", "..", "...", "...."]
    for i in range(5):
        print(
            f"Simulating payment authorization process{animation[i % len(animation)]}"
        )
        time.sleep(1)

    response_pb.status = BaseStatus.OK

    ch.basic_publish(
        "",
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(correlation_id=properties.correlation_id),
        body=response_pb.SerializeToString(),
    )


def on_return_payment_request(ch, method, properties, body):
    payment_info_pb = PaymentInfoPB()
    payment_info_pb.ParseFromString(body)

    print(f" [x] Received Return payment request with: {payment_info_pb}")

    response_pb = BaseResponsePB()

    animation = [".", "..", "...", "...."]
    for i in range(5):
        print(f"Simulating payment return process{animation[i % len(animation)]}")
        time.sleep(1)

    response_pb.status = BaseStatus.OK

    ch.basic_publish(
        "",
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(correlation_id=properties.correlation_id),
        body=response_pb.SerializeToString(),
    )
