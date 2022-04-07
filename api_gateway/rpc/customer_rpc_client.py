import pika
import typing
import base64

from .rpc_client import RpcClient
from hipotap_common.queues.customer_queues import CUSTOMER_AUTH_QUEUE, CUSTOMER_REGISTER_QUEUE
from hipotap_common.models.customer import CustomerCredentials, Customer
from hipotap_common.models.auth import AuthResponse
from hipotap_common.proto_messages.hipotap_pb2 import BaseResponsePB

class CustomerRpcClient(RpcClient):

    def authenticate(self, customer_creds: CustomerCredentials) -> AuthResponse:
        if not isinstance(customer_creds, CustomerCredentials):
            raise  TypeError("Expected CustomerCredentials object")

        self.init_callback()

        # Send request
        self.channel.basic_publish(exchange='',
                                   routing_key=CUSTOMER_AUTH_QUEUE,
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id),
                                   body=customer_creds.serialize())

        # Wait for response
        while self.response is None:
            self.connection.process_data_events()

        return  AuthResponse.deserialize(self.response)

    def register(self, customer: Customer):
        if not isinstance(customer, Customer):
            raise  TypeError("Expected Customer object")

        self.init_callback()

        self.channel.basic_publish(exchange='',
                                   routing_key=CUSTOMER_REGISTER_QUEUE,
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id),
                                   body=customer.serialize())

        # Wait for response
        while self.response is None:
            self.connection.process_data_events()
        base_response_bp = BaseResponsePB()
        base_response_bp.ParseFromString(base64.b64decode(self.response))
        return base_response_bp
