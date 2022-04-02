import base64
import pickle

from ..proto_messages.customer_pb2 import CustomerCredentialsPB, CustomerPB

class CustomerCredentials:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __str__(self):
        return f"{self.email} {self.password}"

    def serialize(self):
        customer_credentials_pb = CustomerCredentialsPB()
        customer_credentials_pb.email = self.email
        customer_credentials_pb.password = self.password

        return base64.b64encode(customer_credentials_pb.SerializeToString())
        # return pickle.dumps(self)

    @classmethod
    def deserialize(cls, bytes: bytes):
        customer_credentials_pb = CustomerCredentialsPB()
        customer_credentials_pb.ParseFromString(base64.b64decode(bytes))
        return cls(customer_credentials_pb.email, customer_credentials_pb.password)

class Customer:
    def __init__(self, name="", surname="", credentials=CustomerCredentials("", "")):
        self.name = name
        self.surname = surname
        self.credentials = CustomerCredentials(email, password)

    def __str__(self):
        return f"{self.name} {self.surname} {self.credentials}"

    def serialize(self):
        customer_pb = CustomerPB()
        customer_pb.name = self.name
        customer_pb.surname = self.surname
        customer_pb.credentials = self.credentials.serialize()

        return base64.b64encode(customer_pb.SerializeToString())

    @classmethod
    def deserialize(cls, bytes: bytes):
        customer_pb = CustomerPB()
        customer_pb.ParseFromString(base64.b64decode(bytes))
        return cls(customer_pb.name, customer_pb.surname, credentials=CustomerCredentials.deserialize(customer_pb.credentials))

        return pickle.loads(bytes)
