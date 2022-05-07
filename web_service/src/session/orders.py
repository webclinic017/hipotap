from flask import session
import requests

from ..hipotap_common.api.endpoints import ORDER_REQUEST_ENDPOINT, ORDER_LIST_ENDPOINT


def get_order_list():
    """
    Get customer orders
    """
    # call to API Gateway for getting offers
    response = requests.get(
        ORDER_LIST_ENDPOINT,
        data={
              "customer_email": session["email"]
        })

    if response.status_code != 200:
        raise NotImplementedError

    return response.json()["orders"]


def order_request(offer_id: int):
    """
    Request order offer
    """
    # call to API Gateway for getting offers
    response = requests.post(
        ORDER_REQUEST_ENDPOINT,
        data={"offer_id": offer_id,
              "customer_email": session["email"],
              "price": 0
        })

    if response.status_code != 200:
        raise NotImplementedError

    # return response.json()["offers"]
