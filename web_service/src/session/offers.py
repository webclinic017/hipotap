from flask import session
import requests

from ..hipotap_common.api.endpoints import OFFERS_ENDPOINT, OFFER_ENDPOINT, OFFER_FILTERING_ENDPOINT


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

def get_single_offer(offer_id):
    """
    Get single offer
    """
    # call to API Gateway for getting offer
    response = requests.get(
        OFFER_ENDPOINT, data={
            'offer_id': offer_id
        }
    )

    if response.status_code != 200:
        raise NotImplementedError

    return response.json()

def get_filtered_offers(filter):
    """
    Get filtered offers
    """
    # call to API Gateway for getting offers
    response = requests.get(
        OFFER_FILTERING_ENDPOINT, data=filter
    )

    if response.status_code != 200:
        raise NotImplementedError

    return response.json()['offers']
