import pika
from hipotap_common.proto_messages.hipotap_pb2 import BaseResponsePB
from hipotap_common.proto_messages.order_pb2 import OrderListPB, OrderPaymentRequestPB
from hipotap_common.queues.order_queues import ORDER_PAYMENT_REQUEST_QUEUE, ORDER_RESERVE_REQUEST_QUEUE, ORDER_LIST_QUEUE

from .rpc_client import RpcClient


class OrderRpcClient(RpcClient):
    def order_reserve_request(self, order_request_pb) -> BaseResponsePB:
        self.init_callback()

        # Send request
        self.channel.basic_publish(
            exchange="",
            routing_key=ORDER_RESERVE_REQUEST_QUEUE,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue, correlation_id=self.corr_id
            ),
            body=order_request_pb.SerializeToString(),
        )

        # Wait for response
        while self.response is None:
            self.connection.process_data_events()

        response = BaseResponsePB()
        response.ParseFromString(self.response)
        return response

    def get_order_list(self, order_list_request_pb) -> BaseResponsePB:
        self.init_callback()

        # Send request
        self.channel.basic_publish(
            exchange="",
            routing_key=ORDER_LIST_QUEUE,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue, correlation_id=self.corr_id
            ),
            body=order_list_request_pb.SerializeToString(),
        )

        # Wait for response
        while self.response is None:
            self.connection.process_data_events()

        response = OrderListPB()
        response.ParseFromString(self.response)
        return response

    def order_payment_request(self, order_payment_request_pb: OrderPaymentRequestPB) -> BaseResponsePB:
        self.init_callback()

        # Send request
        self.channel.basic_publish(
            exchange="",
            routing_key=ORDER_PAYMENT_REQUEST_QUEUE,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue, correlation_id=self.corr_id
            ),
            body=order_payment_request_pb.SerializeToString(),
        )

        # Wait for response
        while self.response is None:
            self.connection.process_data_events()

        response = BaseResponsePB()
        response.ParseFromString(self.response)
        return response
