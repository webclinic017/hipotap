from flask import Blueprint, render_template, session, request
from ..session.offers import get_offer_list, get_single_offer, get_filtered_offers

offers = Blueprint("offers", __name__)


@offers.get("/offers")
def get_offers():
    offer_list = get_offer_list()
    return render_template("offers.html", session=session, offers=offer_list)


@offers.get('/offer/<offer_id>')
def get_offer(offer_id):
    offer = get_single_offer(offer_id)
    return render_template("offer.html", session=session, offer=offer)


@offers.get('/offers/filter')
def filter_offers():
    offer_list = get_filtered_offers({
        'allowed_adult_count': request.args.get('allowed_adult_count'),
        'allowed_children_count': request.args.get('allowed_children_count'),
        'max_adult_price': request.args.get('max_adult_price'),
        "max_children_price": request.args.get("max_children_price"),
        "hotel": request.args.get("hotel"),
        "place": request.args.get("place"),
        "date_start": request.args.get("date_start"),
        "date_end": request.args.get("date_end")
    })
    return render_template("offers.html", session=session, offers=offer_list)
