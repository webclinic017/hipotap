import sys
import time

from fastapi import FastAPI, Form, HTTPException
from google.protobuf import json_format
from hipotap_common.api.endpoints import ORDER_REQUEST_PATH
from hipotap_common.proto_messages.auth_pb2 import AuthStatus
from hipotap_common.proto_messages.customer_pb2 import CustomerCredentialsPB, CustomerPB
from hipotap_common.proto_messages.hipotap_pb2 import BaseStatus
from hipotap_common.proto_messages.offer_pb2 import OfferListPB
from hipotap_common.proto_messages.order_pb2 import OrderRequestPB
from pydantic import BaseModel

from rpc.customer_rpc_client import CustomerRpcClient
from rpc.offer_rpc_client import OfferRpcClient

CUSTOMER_AUTH_QUEUE = "customer_auth"


class AuthData(BaseModel):
    email: str
    password: str


app = FastAPI()

time.sleep(5)


@app.post("/customer/authenticate/")
async def authenticate(email: str = Form(...), password: str = Form(...)):
    print(f"Got [POST]/customer/authenticate/ with email={email}&password={password}")
    sys.stdout.flush()

    customer_credentials = CustomerCredentialsPB()
    customer_credentials.email = email
    customer_credentials.password = password

    customer_client = CustomerRpcClient()
    auth_response_pb = customer_client.authenticate(customer_credentials)

    if auth_response_pb.status == AuthStatus.OK:
        print("Authentication OK")
        sys.stdout.flush()
        return {
            "name": auth_response_pb.customer_data.name,
            "surname": auth_response_pb.customer_data.surname,
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@app.post("/customer/register/")
async def register(
    name: str = Form(...),
    surname: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
):
    print(
        f"Got [POST]/customer/register/ with name={name}, surname={surname}, email={email}, password={password}"
    )
    sys.stdout.flush()

    customer_client = CustomerRpcClient()
    customer_pb = CustomerPB()
    customer_pb.data.name = name
    customer_pb.data.surname = surname
    customer_pb.credentials.email = email
    customer_pb.credentials.password = password
    reg_response = customer_client.register(customer_pb)

    if reg_response.status == BaseStatus.OK:
        print("Registration OK")
        sys.stdout.flush()
        return {"status": "OK"}
    else:
        raise HTTPException(status_code=401, detail="Email is taken")


@app.get("/offers/")
async def offers():
    print(f"Got [GET]/offers/")
    sys.stdout.flush()

    offer_client = OfferRpcClient()
    offer_list_pb = offer_client.get_offers()

    return json_format.MessageToDict(offer_list_pb)


@app.post(ORDER_REQUEST_PATH)
async def order_request(
    offer_id: int = Form(...), customer_email: str = Form(...), price: float = Form(...)
):
    from rpc.order_rpc_client import OrderRpcClient

    order_client = OrderRpcClient()
    order_request_pb = OrderRequestPB()
    order_request_pb.offer_id = offer_id
    order_request_pb.customer_email = customer_email
    order_request_pb.price = price
    order_response = order_client.order_request(order_request_pb)

    if order_response.status == BaseStatus.OK:
        print("Order OK")
        sys.stdout.flush()
        return {"status": "OK"}
    else:
        raise HTTPException(status_code=401, detail="Email is taken")
