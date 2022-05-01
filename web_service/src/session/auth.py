from flask import session
import requests

from ..hipotap_common.exceptions import (
    InvalidCredentialsException,
    UserAlreadyExistsException,
)
from ..hipotap_common.api.endpoints import AUTHENTICATE_ENDPOINT, REGISTER_ENDPOINT


def login_user(email, password):
    """
    Authenticate user
    """
    # call to API Gateway for authentication
    response = requests.post(
        AUTHENTICATE_ENDPOINT, data={"email": email, "password": password}
    )

    if response.status_code != 200:
        raise InvalidCredentialsException()

    customer_data = response.json()
    session["authenticated"] = True
    session["username"] = customer_data["name"]
    session["email"] = email


def logout_user():
    """
    Logout user
    """
    session.clear()


def signup_user(name, surname, email, password):
    """
    Create user account
    """
    # call to API Gateway for authentication
    response = requests.post(
        REGISTER_ENDPOINT,
        data={"name": name, "surname": surname, "email": email, "password": password},
    )

    if response.status_code != 200:
        raise UserAlreadyExistsException()

    customer_data = response.json()
