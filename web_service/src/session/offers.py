from flask import session
import requests

from ..hipotap_common.api.endpoints import OFFERS_ENDPOINT


def get_offer_list():
    """
    Get offer list
    """
    # call to API Gateway for getting offers
    response = requests.get(
        OFFERS_ENDPOINT, data=None
    )

    if response.status_code != 200:
        raise NotImplementedError

    return response.json()['offers']
