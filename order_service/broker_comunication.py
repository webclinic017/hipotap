import pika
from hipotap_common.proto_messages.hipotap_pb2 import BaseResponsePB, BaseStatus
from hipotap_common.proto_messages.order_pb2 import OrderListPB
from hipotap_common.queues.order_queues import (
    ORDER_RESERVE_REQUEST_QUEUE,
    ORDER_LIST_QUEUE,
    ORDER_PAYMENT_REQUEST_QUEUE
)
from hipotap_common.rpc.rpc_subscriber import RpcSubscriber

from hipotap_common.db import Order_Table, db_session


from sagas.order_saga import OrderSaga


def broker_requests_handling_loop():
    subscriber = RpcSubscriber()
    subscriber.subscribe_to_queue(
        ORDER_RESERVE_REQUEST_QUEUE, on_order_reservation_request
    )
    subscriber.subscribe_to_queue(ORDER_LIST_QUEUE, on_order_list_request)
    subscriber.subscribe_to_queue(ORDER_PAYMENT_REQUEST_QUEUE, on_order_payment_request)
    subscriber.handling_loop()


def on_order_reservation_request(ch, method, properties, body):
    from hipotap_common.proto_messages.order_pb2 import OrderRequestPB

    order_request_pb = OrderRequestPB()
    order_request_pb.ParseFromString(body)
    print(f"[x] Order for offer id = {order_request_pb.offer_id} requested")
    response_pb = BaseResponsePB()
    response_pb.status = BaseStatus.OK

    order_saga = OrderSaga(order_request_pb)

    if not order_saga.run():
        response_pb.status = BaseStatus.FAIL

    # Send response
    ch.basic_publish(
        "",
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(correlation_id=properties.correlation_id),
        body=response_pb.SerializeToString(),
    )


def on_order_list_request(ch, method, properties, body):
    from hipotap_common.proto_messages.order_pb2 import OrderListRequestPB

    order_list_request_pb = OrderListRequestPB()
    order_list_request_pb.ParseFromString(body)
    print(
        f"[x] Order list for customer_email = {order_list_request_pb.customer_email} requested"
    )

    order_list_pb = OrderListPB()
    try:
        orders = db_session.query(Order_Table).filter_by(
            customer_id=order_list_request_pb.customer_email
        )
        for order in orders:
            order_list_pb.orders.append(order.to_pb())
    except Exception as e:
        print(f"Cannot find orders: {e}")

    # Send response
    ch.basic_publish(
        "",
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(correlation_id=properties.correlation_id),
        body=order_list_pb.SerializeToString(),
    )

def on_order_payment_request(ch, method, properties, body):
    from hipotap_common.proto_messages.order_pb2 import OrderPaymentRequestPB

    order_payment_request_pb = OrderPaymentRequestPB()
    order_payment_request_pb.ParseFromString(body)

    print(
        f"[x] Order payment for order_id = {order_payment_request_pb.order_id} requested"
    )
    response_pb = BaseResponsePB()
    # TODO: Saga for payment
    order = db_session.query(Order_Table).filter_by(id=order_payment_request_pb.order_id).one()
    # .update({Order_Table.payment_status: "PAID"})
    order.payment_status = "PAID"
    db_session.commit()
    response_pb.status = BaseStatus.OK

    # Send response
    ch.basic_publish(
        "",
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(correlation_id=properties.correlation_id),
        body=response_pb.SerializeToString(),
    )
