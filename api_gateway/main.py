from fastapi import FastAPI, HTTPException, Form
import pika
import sys, time
from hipotap_common.models.customer import CustomerCredentials, Customer
from hipotap_common.models.auth import AuthStatus
from hipotap_common.proto_messages.hipotap_pb2 import BaseStatus
from rpc.customer_rpc_client import CustomerRpcClient
from pydantic import BaseModel


CUSTOMER_AUTH_QUEUE = 'customer_auth'


class AuthData(BaseModel):
    email: str
    password: str


app = FastAPI()

time.sleep(5)


@app.post("/customer/authenticate/")
async def authenticate(email: str = Form(...), password: str = Form(...)):
    print(f"Got [POST]/customer/authenticate/ with databaseemail={email}&password={password}")
    sys.stdout.flush()
    customer_client = CustomerRpcClient()
    auth_response = customer_client.authenticate(CustomerCredentials(email, password))

    if auth_response.status == AuthStatus.OK:
        print("Authentication OK")
        sys.stdout.flush()
        return {"name": auth_response.customer_data.name, "surname": auth_response.customer_data.surname}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@app.post("/customer/register/")
async def register(name: str = Form(...), surname: str = Form(...), email: str = Form(...), password: str = Form(...)):
    print(f"Got [POST]/customer/register/ with name={name}, surname={surname}, email={email}, password={password}")
    sys.stdout.flush()

    customer_client = CustomerRpcClient()
    reg_response = customer_client.register(Customer(name, surname, email, password))

    if reg_response.status == BaseStatus.OK:
        print("Registration OK")
        sys.stdout.flush()
        return {'status': "OK"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
