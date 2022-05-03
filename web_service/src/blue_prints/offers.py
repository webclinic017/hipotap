from flask import Blueprint, render_template, session
from ..session.offers import get_offer_list

offers = Blueprint("offers", __name__)


@offers.get("/offers")
def get_offers():
    offer_list = get_offer_list()
    return render_template("offers.html", session=session, offers=offer_list)

@offers.get('/offer/<offer_id>')
def get_offer(offer_id):
    return f'Noting here, ID: {offer_id}'
