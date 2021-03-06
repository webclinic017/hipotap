from flask import session
import requests

from ..hipotap_common.api.endpoints import (
    ORDER_RESERVE_REQUEST_ENDPOINT,
    ORDER_LIST_ENDPOINT,
    ORDER_PAYMENT_ENDPOINT,
    GET_ORDER_ENDPOINT,
)


def get_order_list():
    """
    Get customer orders
    """
    # call to API Gateway for getting offers
    response = requests.get(
        ORDER_LIST_ENDPOINT, data={"customer_email": session["email"]}
    )

    if response.status_code != 200:
        raise NotImplementedError

    return response.json()["orders"]


def get_order(order_id):
    """
    Get customer order
    """
    # call to API Gateway for getting offers
    response = requests.get(GET_ORDER_ENDPOINT, data={"order_id": order_id})

    if response.status_code != 200:
        raise NotImplementedError

    return response.json()


def reserve_offer_request(offer_id: int, adult_count: int, children_count: int):
    """
    Request order offer
    """
    # call to API Gateway for getting offers
    response = requests.post(
        ORDER_RESERVE_REQUEST_ENDPOINT,
        data={
            "offer_id": offer_id,
            "customer_email": session["email"],
            "adult_count": adult_count,
            "children_count": children_count,
        },
    )

    if response.status_code != 200:
        raise NotImplementedError

    return response.json()


def order_payment(order_id: int, card_number, price):
    """
    Pay for order
    """
    response = requests.post(
        ORDER_PAYMENT_ENDPOINT,
        data={"order_id": order_id, "card_number": card_number, "price": price},
    )

    if response.status_code != 200:
        raise NotImplementedError
