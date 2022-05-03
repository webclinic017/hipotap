from flask import session
import requests

from ..hipotap_common.api.endpoints import ORDER_REQUEST_ENDPOINT


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
