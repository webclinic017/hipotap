import pika
import uuid
from typing import Tuple, Optional

from .rpc_client import RpcClient
from hipotap_common.queues.customer_queues import CUSTOMER_AUTH_QUEUE
from hipotap_common.models.customer import CustomerCredentials, CustomerData
from hipotap_common.models.auth import AuthResponse

class CustomerRpcClient(RpcClient):

    def authenticate(self, customer_creds: CustomerCredentials) -> AuthResponse:
        if not isinstance(customer_creds, CustomerCredentials):
            raise  TypeError("Expected CustomerCredentials object")

        self._open_channel()
        self._open_response_queue()

        # Set idenfitier of the request
        self.corr_id = str(uuid.uuid4())

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
