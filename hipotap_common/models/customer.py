import base64

from ..proto_messages.customer_pb2 import CustomerCredentialsPB, CustomerDataPB, CustomerPB

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


class CustomerData:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname

    def __str__(self):
        return f"{self.name} {self.surname}"

    def serialize(self):
        customer_data_pb = CustomerDataPB()
        customer_data_pb.name = self.name
        customer_data_pb.surname = self.surname

        return base64.b64encode(customer_data_pb.SerializeToString())

    @classmethod
    def deserialize(cls, bytes: bytes):
        customer_data_pb = CustomerDataPB()
        customer_data_pb.ParseFromString(base64.b64decode(bytes))
        return cls(customer_data_pb.name, customer_data_pb.surname)


class Customer:
    def __init__(self, name, surname, credentials):
        self.name = name
        self.surname = surname
        self.credentials = credentials

    def __str__(self):
        return f"{self.name} {self.surname} {self.credentials}"

    def serialize(self):
        customer_pb = CustomerPB()
        customer_pb.data = CustomerData(self.name, self.surname).serialize()
        customer_pb.credentials = self.credentials.serialize()

        return base64.b64encode(customer_pb.SerializeToString())

    @classmethod
    def deserialize(cls, bytes: bytes):
        customer_pb = CustomerPB()
        customer_pb.ParseFromString(base64.b64decode(bytes))
        customer_data_pb = CustomerDataPB()
        customer_data_pb.ParseFromString(base64.b64decode(customer_pb.data))
        return cls(customer_data_pb.name, customer_data_pb.surname, credentials=CustomerCredentials.deserialize(customer_pb.credentials))
