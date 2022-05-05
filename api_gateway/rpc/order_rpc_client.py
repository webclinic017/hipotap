import pika
from hipotap_common.proto_messages.hipotap_pb2 import BaseResponsePB
from hipotap_common.queues.order_queues import ORDER_REQUEST_QUEUE

from .rpc_client import RpcClient


class OrderRpcClient(RpcClient):
    def order_request(self, order_request_pb) -> BaseResponsePB:
        self.init_callback()

        # Send request
        self.channel.basic_publish(
            exchange="",
            routing_key=ORDER_REQUEST_QUEUE,
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
