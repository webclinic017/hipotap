import pika
from hipotap_common.proto_messages.auth_pb2 import AuthResponsePB

from hipotap_common.proto_messages.customer_pb2 import CustomerCredentialsPB, CustomerPB

from .rpc_client import RpcClient
from hipotap_common.queues.customer_queues import CUSTOMER_AUTH_QUEUE, CUSTOMER_REGISTER_QUEUE
from hipotap_common.proto_messages.hipotap_pb2 import BaseResponsePB

class CustomerRpcClient(RpcClient):

    def authenticate(self, customer_creds: CustomerCredentialsPB) -> AuthResponsePB:
        if not isinstance(customer_creds, CustomerCredentialsPB):
            raise  TypeError("Expected CustomerCredentialsPB object")

        self.init_callback()

        # Send request
        self.channel.basic_publish(exchange='',
                                   routing_key=CUSTOMER_AUTH_QUEUE,
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id),
                                #    body=customer_creds.serialize())
                                   body=customer_creds.SerializeToString())

        # Wait for response
        while self.response is None:
            self.connection.process_data_events()

        auth_response_pb = AuthResponsePB()
        auth_response_pb.ParseFromString(self.response)
        return auth_response_pb

    def register(self, customer_pb: CustomerPB):
        if not isinstance(customer_pb, CustomerPB):
            raise  TypeError("Expected CustomerPB object")

        self.init_callback()

        self.channel.basic_publish(exchange='',
                                   routing_key=CUSTOMER_REGISTER_QUEUE,
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id),
                                   body=customer_pb.SerializeToString())

        # Wait for response
        while self.response is None:
            self.connection.process_data_events()
        base_response_pb = BaseResponsePB()
        base_response_pb.ParseFromString(self.response)
        return base_response_pb
