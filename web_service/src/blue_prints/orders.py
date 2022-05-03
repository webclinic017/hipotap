from flask import Blueprint, render_template, session
from ..session.orders import order_request

orders = Blueprint("orders", __name__)


@orders.get("/orders/")
def get_customer_orders():
    offer_list = get_offer_list()
    return render_template("orders.html", session=session, offers=offer_list)

@orders.get('/order/<order_id>')
def get_order(order_id):
    return f'Noting here, ID: {order_id}'

@orders.post('/order/order_offer/<offer_id>')
def post_order_offer(offer_id):
    order_request(offer_id)
    return f'Order request for offer {offer_id}'
    # return f'Noting here, ID: {offer_id}'
