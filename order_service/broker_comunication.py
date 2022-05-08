import pika
from hipotap_common.proto_messages.hipotap_pb2 import BaseResponsePB, BaseStatus
from hipotap_common.proto_messages.order_pb2 import OrderPB, OrderListPB
from hipotap_common.queues.order_queues import ORDER_REQUEST_QUEUE, ORDER_LIST_QUEUE
from hipotap_common.rpc.rpc_subscriber import RpcSubscriber

from hipotap_common.db import Order_Table, Offer_Table, db_session


def broker_requests_handling_loop():
    subscriber = RpcSubscriber()
    subscriber.subscribe_to_queue(ORDER_REQUEST_QUEUE, on_order_request)
    subscriber.subscribe_to_queue(ORDER_LIST_QUEUE, on_order_list_request)
    subscriber.handling_loop()


def on_order_request(ch, method, properties, body):
    from hipotap_common.proto_messages.order_pb2 import OrderRequestPB

    order_request_pb = OrderRequestPB()
    order_request_pb.ParseFromString(body)
    print(f"[x] Order for offer id = {order_request_pb.offer_id} requested")

    response_pb = BaseResponsePB()
    try:
        offer = db_session.query(Offer_Table).filter_by(id=order_request_pb.offer_id).one()
        if order_request_pb.adult_count > offer.max_adult_count or order_request_pb.children_count > offer.max_children_count:
            raise NotImplementedError
        price = order_request_pb.adult_count * offer.price_adult + order_request_pb.children_count * offer.price_children

        db_session.add(
            Order_Table(
                offer_id=order_request_pb.offer_id,
                customer_id=order_request_pb.customer_email,
                adult_count=order_request_pb.adult_count,
                children_count=order_request_pb.children_count,
                price=price
            )
        )
        db_session.commit()
        print("############ Order added ############")
        response_pb.status = BaseStatus.OK
    except Exception as e:
        print(f"Cannot add order: {e}")
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
