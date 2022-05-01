from flask import session
import requests

from ..hipotap_common.api.endpoints import OFFERS_ENDPOINT


def get_offers():
    """
    Authenticate user
    """
    # call to API Gateway for authentication
    response = requests.get(
        OFFERS_ENDPOINT, data=None
    )

    return response.json()['offers']

    if response.status_code != 200:
        raise NotImplementedError

    return response.json()
