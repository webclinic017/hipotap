import pika
from hipotap_common.proto_messages.auth_pb2 import AuthResponsePB

from hipotap_common.proto_messages.order_pb2 import PaymentInfoPB

from .rpc_client import RpcClient
from hipotap_common.queues.payment_queues import (
    AUTHORIZE_PAYMENT_QUEUE,
    RETURN_PAYMENT_QUEUE
)
from hipotap_common.proto_messages.hipotap_pb2 import BaseResponsePB


class PaymentRpcClient(RpcClient):
    def authorize_payment(self, payment_info_pb):
        if not isinstance(payment_info_pb, PaymentInfoPB):
            raise TypeError("Expected PaymentInfoPB object")

        self.init_callback()

        self.channel.basic_publish(
            exchange="",
            routing_key=AUTHORIZE_PAYMENT_QUEUE,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue, correlation_id=self.corr_id
            ),
            body=payment_info_pb.SerializeToString(),
        )

        # Wait for response
        while self.response is None:
            self.connection.process_data_events()
        base_response_pb = BaseResponsePB()
        base_response_pb.ParseFromString(self.response)
        return base_response_pb

    def return_payment(self, payment_info_pb):
        if not isinstance(payment_info_pb, PaymentInfoPB):
            raise TypeError("Expected PaymentInfoPB object")

        self.init_callback()

        self.channel.basic_publish(
            exchange="",
            routing_key=RETURN_PAYMENT_QUEUE,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue, correlation_id=self.corr_id
            ),
            body=payment_info_pb.SerializeToString(),
        )

        # Wait for response
        while self.response is None:
            self.connection.process_data_events()
        base_response_pb = BaseResponsePB()
        base_response_pb.ParseFromString(self.response)
        return base_response_pb
