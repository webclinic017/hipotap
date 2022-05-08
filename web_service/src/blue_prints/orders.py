from flask import Blueprint, flash, redirect, render_template, session, url_for, request

from ..session.orders import order_request, get_order_list

orders = Blueprint("orders", __name__)


@orders.get("/orders/")
def get_customer_orders():
    if not ("authenticated" in session and session["authenticated"]):
        flash("You must be logged in to view your orders", "is-danger")
        return redirect(url_for("offers.get_offers"))

    orders = []
    try:
        orders = get_order_list()
    except Exception as e:
        flash("Cannot get customer's orders", "is-danger")
        print(e, flush=True)

    print(orders, flush=True)
    return render_template("orders.html", orders=orders)


@orders.get("/order/<order_id>")
def get_order(order_id):
    return f"Noting here, ID: {order_id}"


@orders.post("/order/order_offer/<offer_id>")
def post_order_offer(offer_id):
    adult_count = int(request.form['adult_count'])
    children_count = int(request.form['children_count'])

    if not ("authenticated" in session and session["authenticated"]):
        flash("You must be logged in to order offers", "is-danger")
        return redirect(url_for("offers.get_offers"))

    try:
        # data not validated
        order_request(offer_id, adult_count, children_count)

        flash("Order request sent", "is-success")
    except:
        flash("Order failed", "is-danger")
    return redirect(url_for("orders.get_customer_orders"))
