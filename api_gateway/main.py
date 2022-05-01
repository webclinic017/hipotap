from fastapi import FastAPI, HTTPException, Form
import sys, time
from hipotap_common.proto_messages.auth_pb2 import AuthStatus
from hipotap_common.proto_messages.customer_pb2 import CustomerCredentialsPB, CustomerPB
from hipotap_common.proto_messages.hipotap_pb2 import BaseStatus
from rpc.customer_rpc_client import CustomerRpcClient
from pydantic import BaseModel


CUSTOMER_AUTH_QUEUE = "customer_auth"


class AuthData(BaseModel):
    email: str
    password: str


app = FastAPI()

time.sleep(5)


@app.post("/customer/authenticate/")
async def authenticate(email: str = Form(...), password: str = Form(...)):
    print(
        f"Got [POST]/customer/authenticate/ with databaseemail={email}&password={password}"
    )
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
