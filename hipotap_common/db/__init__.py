from sqlalchemy import Column, Float, Integer, String, DateTime, Date, create_engine
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from google.protobuf.any_pb2 import Any

from ..proto_messages.offer_pb2 import OfferPB
from ..proto_messages.order_pb2 import OrderPB
import os

DB_PATH = os.environ.get("DB_PATH", "postgresql://hipotap:hipotap@hipotap_db:5432/hipotap_db")
# postgresql://postgres:student@10.40.71.55:5432/RSWW_172127_1
print("CONNECTING TO DB:", DB_PATH)
engine = create_engine(DB_PATH)
engine.connect()

DBModel = declarative_base()


class Customer_Table(DBModel):
    __tablename__ = "customer"
    email = Column(String(100), primary_key=True)
    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)


class Offer_Table(DBModel):
    __tablename__ = "offer"
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    description = Column(String(600))
    place = Column(String(100))
    hotel = Column(String(100))
    max_adult_count = Column(Integer)
    max_children_count = Column(Integer)
    price_adult = Column(Float)
    price_children = Column(Float)
    date_start = Column(DateTime)
    date_end = Column(DateTime)

    def to_pb(self) -> OfferPB:
        offer_pb = OfferPB()
        offer_pb.id = self.id
        offer_pb.title = self.title
        offer_pb.description = self.description
        offer_pb.place = self.place
        offer_pb.hotel = self.hotel
        offer_pb.max_adult_count = self.max_adult_count
        offer_pb.max_children_count = self.max_children_count
        offer_pb.price_adult = self.price_adult
        offer_pb.price_children = self.price_children
        offer_pb.date_start.FromDatetime(self.date_start)
        offer_pb.date_end.FromDatetime(self.date_end)
        return offer_pb

    def to_any(self)  -> Any:
        any = Any()
        any.Pack(self.to_pb())
        return any

class Order_Table(DBModel):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True)
    offer_id = Column(Integer)
    customer_id = Column(String)
    adult_count = Column(Integer)
    children_count = Column(Integer)
    price = Column(Float)
    creation_time = Column(DateTime, server_default=func.now())
    payment_status = Column(String(100))

    def to_pb(self) -> OrderPB:
        order_pb = OrderPB()
        order_pb.id = self.id
        order_pb.offer_id = self.offer_id
        order_pb.customer_id = self.customer_id
        order_pb.adult_count = self.adult_count
        order_pb.children_count = self.children_count
        order_pb.price = self.price
        order_pb.creation_time.FromDatetime(self.creation_time)
        order_pb.payment_status = self.payment_status
        return order_pb

    def to_any(self)  -> Any:
        any = Any()
        any.Pack(self.to_pb())
        return any


db_session = sessionmaker(bind=engine)()
