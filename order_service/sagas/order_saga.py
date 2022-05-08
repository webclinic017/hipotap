from hipotap_common.proto_messages.offer_pb2 import OfferPB
from hipotap_common.sagas.saga import Saga
from hipotap_common.proto_messages.hipotap_pb2 import BaseStatus
from hipotap_common.proto_messages.order_pb2 import OrderRequestPB
from hipotap_common.rpc.clients.offer_rpc_client import OfferRpcClient
from hipotap_common.db import db_session, Order_Table

# SAGA:
# 1. Check if offer is available
# 2. Create order
# 3. Process payment
# 4. Confirm order
# 5. Send order confirmation to customer


class OrderSaga(Saga):
    def __init__(self, order_request_pb: OrderRequestPB):
        super().__init__("OrderSaga")
        self.order_request_pb = order_request_pb

        self.add_step(
            self.check_offer_availability,
            lambda: print("No rollback for offer validation"),
        )
        self.add_step(
            self.create_order,
            self.delete_order
        )

    def check_offer_availability(self):
        offer_rpc_client = OfferRpcClient()
        response = offer_rpc_client.validate_order(self.order_request_pb)
        if response.status == BaseStatus.OK:
            self.offer_pb = OfferPB()
            response.message.Unpack(self.offer_pb)
            return True
        return False

    def create_order(self):
        price = (
            self.order_request_pb.adult_count * self.offer_pb.price_adult
            + self.order_request_pb.children_count * self.offer_pb.price_children
        )
        try:
            order = Order_Table(
                offer_id=self.order_request_pb.offer_id,
                customer_id=self.order_request_pb.customer_email,
                adult_count=self.order_request_pb.adult_count,
                children_count=self.order_request_pb.children_count,
                price=price,
            )
            db_session.add(order)
            db_session.commit()
            self.order = order
        except Exception as e:
            print(f"Cannot add order: {e}")
            return False

        return True

    def delete_order(self):
        db_session.delete(self.order)
        db_session.commit()
        return True
