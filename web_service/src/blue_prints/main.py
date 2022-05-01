from flask import Blueprint, render_template, session
from ..session.offers import get_offers

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html", session=session)


@main.route("/profile")
def profile():
    return render_template("profile.html", username=session)

@main.get("/offers")
def offers():
    offers = get_offers()
    return render_template("offers.html", session=session, offers=offers)
