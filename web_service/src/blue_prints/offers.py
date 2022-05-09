from flask import Blueprint, render_template, session
from ..session.offers import get_offer_list, get_single_offer

offers = Blueprint("offers", __name__)


@offers.get("/offers")
def get_offers():
    offer_list = get_offer_list()
    return render_template("offers.html", session=session, offers=offer_list)

@offers.get('/offer/<offer_id>')
def get_offer(offer_id):
    offer = get_single_offer(offer_id)
    return render_template("offer.html", session=session, offer=offer)
