from flask import Blueprint, flash, redirect, render_template, session, url_for, request

from ..session.orders import (
    get_order,
    get_order_list,
    order_payment,
    reserve_offer_request,
)

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
def get_customer_order(order_id):
    if not ("authenticated" in session and session["authenticated"]):
        flash("You must be logged in to view your orders", "is-danger")
        return redirect(url_for("offers.get_offers"))

    print(f"Getting order with id = {order_id}", flush=True)
    order = None
    try:
        order = get_order(order_id)
    except Exception as e:
        flash("Cannot get customer's order", "is-danger")
        print(e, flush=True)

    print(order, flush=True)
    return render_template("order.html", order=order)


@orders.post("/order/order_offer/<offer_id>")
def post_order_offer(offer_id):
    adult_count = int(request.form["adult_count"])
    children_count = int(request.form["children_count"])

    if not ("authenticated" in session and session["authenticated"]):
        flash("You must be logged in to order or reserve offers", "is-danger")
        return redirect(url_for("offers.get_offers"))

    if "purchase_button" in request.form:
        try:
            print("########### Purchasing offer ###########", flush=True)
            # data not validated
            order = reserve_offer_request(offer_id, adult_count, children_count)
            return redirect(url_for("orders.get_order_payment", order_id=order["id"]))
        except Exception as e:
            print(e)
            flash("Order reservation failed", "is-danger")

    elif "reserve_button" in request.form:
        try:
            print("########### Reserving offer ###########", flush=True)
            # data not validated
            order = reserve_offer_request(offer_id, adult_count, children_count)
            flash("Order reserved", "is-success")
        except:
            flash("Order reservation failed", "is-danger")
    return redirect(url_for("orders.get_customer_orders"))


@orders.get("/order/payment/<order_id>")
def get_order_payment(order_id):
    order = get_order(order_id)
    return render_template("order_payment.html", order=order)


@orders.post("/order/payment/<order_id>")
def post_order_payment(order_id):
    card_number = request.form["card_number"]
    price = request.form["price"]

    if not ("authenticated" in session and session["authenticated"]):
        flash("You must be logged in to pay for order", "is-danger")
        return redirect(url_for("offers.get_offers"))

    try:
        # data not validated
        order_payment(order_id, card_number, price)
        flash("Order paid", "is-success")
    except Exception as e:
        print(f"Order payment failed {e}", flush=True)
        flash("Payment failed", "is-danger")
    return redirect(url_for("orders.get_customer_orders"))
