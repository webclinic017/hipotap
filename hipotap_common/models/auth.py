import base64

from ..proto_messages.auth_pb2 import AuthResponsePB, AuthStatus
from ..proto_messages.customer_pb2 import CustomerDataPB
from .customer import CustomerData
class AuthResponse:
    def __init__(self, status: AuthStatus, customer_data: CustomerData = None):
        self.status = status
        self.customer_data = customer_data

    def __str__(self):
        return f"{self.status} {self.customer_data}"

    def serialize(self):
        auth_response_pb = AuthResponsePB()
        auth_response_pb.status = self.status
        if self.status == AuthStatus.OK:
            auth_response_pb.customer_data.name = self.customer_data.name
            auth_response_pb.customer_data.surname = self.customer_data.surname

        return base64.b64encode(auth_response_pb.SerializeToString())
        # return pickle.dumps(self)

    @classmethod
    def deserialize(cls, bytes: bytes):
        auth_response_pb = AuthResponsePB()
        auth_response_pb.ParseFromString(base64.b64decode(bytes))

        return cls(auth_response_pb.status, CustomerData(auth_response_pb.customer_data.name, auth_response_pb.customer_data.surname))
