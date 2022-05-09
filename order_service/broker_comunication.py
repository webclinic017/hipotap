import pika
from hipotap_common.proto_messages.hipotap_pb2 import BaseResponsePB, BaseStatus
from hipotap_common.proto_messages.order_pb2 import OrderListPB, OrderPB
from hipotap_common.queues.order_queues import (
    GET_ORDER_QUEUE,
    ORDER_RESERVE_REQUEST_QUEUE,
    ORDER_LIST_QUEUE,
    ORDER_PAYMENT_REQUEST_QUEUE,
)
from hipotap_common.rpc.clients.payment_rpc_client import PaymentRpcClient
from hipotap_common.rpc.rpc_subscriber import RpcSubscriber

from hipotap_common.db import Order_Table, db_session


from sagas.order_saga import OrderPaymentSaga, ReserveOrderSaga


def broker_requests_handling_loop():
    subscriber = RpcSubscriber()
    subscriber.subscribe_to_queue(
        ORDER_RESERVE_REQUEST_QUEUE, on_order_reservation_request
    )
    subscriber.subscribe_to_queue(ORDER_LIST_QUEUE, on_order_list_request)
    subscriber.subscribe_to_queue(ORDER_PAYMENT_REQUEST_QUEUE, on_order_payment_request)
    subscriber.subscribe_to_queue(GET_ORDER_QUEUE, on_get_order_request)
    subscriber.handling_loop()


def on_order_reservation_request(ch, method, properties, body):
    from hipotap_common.proto_messages.order_pb2 import OrderRequestPB

    order_request_pb = OrderRequestPB()
    order_request_pb.ParseFromString(body)
    print(f"[x] Order for offer id = {order_request_pb.offer_id} requested")
    response_pb = BaseResponsePB()
    response_pb.status = BaseStatus.OK

    order_saga = ReserveOrderSaga(order_request_pb)

    if not order_saga.run():
        response_pb.status = BaseStatus.FAIL
    else:
        response_pb.message.CopyFrom(order_saga.order.to_any())
        print(f'SAGA FINISHED: response: {response_pb}')

    # Send response
    ch.basic_publish(
        "",
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(correlation_id=properties.correlation_id),
        body=response_pb.SerializeToString(),
    )


def on_get_order_request(ch, method, properties, body):
    from hipotap_common.proto_messages.order_pb2 import GetOrderRequestPB

    get_order_request_pb = GetOrderRequestPB()
    get_order_request_pb.ParseFromString(body)

    print(f"[x] Get order for order_id = {get_order_request_pb.order_id} requested")
    order_pb = None
    try:
        order = (
            db_session.query(Order_Table)
            .filter_by(id=get_order_request_pb.order_id)
            .one()
        )
        order_pb = order.to_pb()
    except Exception as e:
        print(f"Cannot find order with id = {get_order_request_pb.order_id}")

    # Send response
    ch.basic_publish(
        "",
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(correlation_id=properties.correlation_id),
        body=order_pb.SerializeToString(),
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
    response_pb.status = BaseStatus.OK
    payment_saga = OrderPaymentSaga(order_payment_request_pb)
    if not payment_saga.run():
        response_pb.status = BaseStatus.FAIL

    # payment_client = PaymentRpcClient()
    # payment_responst = payment_client.authorize_payment(
    #     order_payment_request_pb.payment_info
    # )
    # if payment_responst.status == BaseStatus.OK:
    #     order = (
    #         db_session.query(Order_Table)
    #         .filter_by(id=order_payment_request_pb.order_id)
    #         .one()
    #     )
    #     order.payment_status = "PAID"
    #     db_session.commit()
    #     response_pb.status = BaseStatus.OK
    # else:
    #     response_pb.status = BaseStatus.FAIL

    # Send response
    ch.basic_publish(
        "",
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(correlation_id=properties.correlation_id),
        body=response_pb.SerializeToString(),
    )
