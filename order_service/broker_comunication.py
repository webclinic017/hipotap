import pika
from hipotap_common.proto_messages.hipotap_pb2 import BaseResponsePB, BaseStatus
from hipotap_common.queues.order_queues import ORDER_REQUEST_QUEUE
from hipotap_common.rpc.rpc_subscriber import RpcSubscriber

from hipotap_common.db import Order_Table, db_session


def broker_requests_handling_loop():
    subscriber = RpcSubscriber()
    subscriber.subscribe_to_queue(ORDER_REQUEST_QUEUE, on_order_request)
    subscriber.handling_loop()


def on_order_request(ch, method, properties, body):
    from hipotap_common.proto_messages.order_pb2 import OrderRequestPB

    order_request_pb = OrderRequestPB()
    order_request_pb.ParseFromString(body)
    print(f"[x] Order for offer id = {order_request_pb.offer_id} requested")

    response_pb = BaseResponsePB()
    try:
        order = db_session.add(
            Order_Table(
                offer_id=order_request_pb.offer_id,
                customer_id=order_request_pb.customer_email,
                price=order_request_pb.price,
            )
        )
        response_pb.status = BaseStatus.OK
    except:
        print("Cannot add order")
        response_pb.status = BaseStatus.FAIL

    # Send response
    ch.basic_publish(
        "",
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(correlation_id=properties.correlation_id),
        body=response_pb.SerializeToString(),
    )
