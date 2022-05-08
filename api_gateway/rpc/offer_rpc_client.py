import pika
from hipotap_common.proto_messages.offer_pb2 import OfferListPB, OfferRequestPB, OfferPB

from .rpc_client import RpcClient
from hipotap_common.queues.offer_queues import OFFER_LIST_QUEUE, OFFER_QUEUE


class OfferRpcClient(RpcClient):
    def get_offers(self) -> OfferListPB:
        self.init_callback()

        # Send request
        self.channel.basic_publish(
            exchange="",
            routing_key=OFFER_LIST_QUEUE,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue, correlation_id=self.corr_id
            ),
            body="",
        )

        # Wait for response
        while self.response is None:
            self.connection.process_data_events()

        offer_list_pb = OfferListPB()
        offer_list_pb.ParseFromString(self.response)
        return offer_list_pb

    def get_offer(self, offer_id) -> OfferListPB:
        self.init_callback()

        offer_request_pb = OfferRequestPB()
        offer_request_pb.offer_id = offer_id

        # Send request
        self.channel.basic_publish(
            exchange="",
            routing_key=OFFER_QUEUE,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue, correlation_id=self.corr_id
            ),
            body=offer_request_pb.SerializeToString(),
        )

        # Wait for response
        while self.response is None:
            self.connection.process_data_events()

        offer_pb = OfferPB()
        offer_pb.ParseFromString(self.response)
        return offer_pb
