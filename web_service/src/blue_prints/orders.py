from flask import Blueprint, flash, redirect, render_template, session, url_for

from ..session.orders import order_request

orders = Blueprint("orders", __name__)


@orders.get("/orders/")
def get_customer_orders():
    # TODO
    return redirect(url_for("offers.get_offers"))


@orders.get("/order/<order_id>")
def get_order(order_id):
    return f"Noting here, ID: {order_id}"


@orders.post("/order/order_offer/<offer_id>")
def post_order_offer(offer_id):
    if not ('authenticated' in session and session['authenticated']):
        flash("You must be logged in to order offers")
        return redirect(url_for("offers.get_offers"))

    try:
        order_request(offer_id)
        flash("Order request sent", "is-success")
    except:
        flash("Order failed", "is-danger")
    return redirect(url_for("orders.get_customer_orders"))
    # return f'Noting here, ID: {offer_id}'
