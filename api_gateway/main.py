import sys
import time

from fastapi import FastAPI, Form, HTTPException
from google.protobuf import json_format
from hipotap_common.api.endpoints import ORDER_REQUEST_PATH, ORDER_LIST_PATH, OFFER_PATH
from hipotap_common.proto_messages.auth_pb2 import AuthStatus
from hipotap_common.proto_messages.customer_pb2 import CustomerCredentialsPB, CustomerPB
from hipotap_common.proto_messages.hipotap_pb2 import BaseStatus
from hipotap_common.proto_messages.offer_pb2 import OfferListPB
from hipotap_common.proto_messages.order_pb2 import OrderRequestPB, OrderListRequestPB
from pydantic import BaseModel

from hipotap_common.rpc.clients.customer_rpc_client import CustomerRpcClient
from hipotap_common.rpc.clients.offer_rpc_client import OfferRpcClient
from hipotap_common.rpc.clients.order_rpc_client import OrderRpcClient
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
    print(f"Got [GET]/offers/", flush=True)

    offer_client = OfferRpcClient()
    offer_list_pb = offer_client.get_offers()

    return json_format.MessageToDict(
        offer_list_pb,
        preserving_proto_field_name=True,
        including_default_value_fields=True,
    )


@app.get(OFFER_PATH)
async def offers(
    offer_id: int = Form(...)
):
    print(f"Got [GET]/offer/ with offer_id={offer_id}", flush=True)

    offer_client = OfferRpcClient()
    offer_pb = offer_client.get_offer(offer_id)

    return json_format.MessageToDict(
        offer_pb,
        preserving_proto_field_name=True,
        including_default_value_fields=True,
    )


@app.post(ORDER_REQUEST_PATH)
async def order_request(
    offer_id: int = Form(...),
    customer_email: str = Form(...),
    adult_count: int = Form(...),
    children_count: int = Form(...)
):

    order_client = OrderRpcClient()
    order_request_pb = OrderRequestPB()
    order_request_pb.offer_id = offer_id
    order_request_pb.customer_email = customer_email
    order_request_pb.adult_count = adult_count
    order_request_pb.children_count = children_count
    order_response = order_client.order_request(order_request_pb)

    if order_response.status == BaseStatus.OK:
        print("Order OK",flush=True)
        return {"status": "OK"}
    else:
        raise HTTPException(status_code=401, detail="Cannot order offer")


@app.get(ORDER_LIST_PATH)
async def order_list_request(customer_email: str = Form(...)):

    order_client = OrderRpcClient()
    order_list_request_pb = OrderListRequestPB()
    order_list_request_pb.customer_email = customer_email
    order_list_pb = order_client.get_order_list(order_list_request_pb)
    return json_format.MessageToDict(
        order_list_pb,
        preserving_proto_field_name=True,
        including_default_value_fields=True,
    )
