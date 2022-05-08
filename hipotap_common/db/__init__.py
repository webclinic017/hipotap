from sqlalchemy import Column, Float, Integer, String, DateTime, Date, create_engine
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from google.protobuf.timestamp_pb2 import Timestamp

from ..proto_messages.offer_pb2 import OfferPB
from ..proto_messages.order_pb2 import OrderPB

engine = create_engine("postgresql://hipotap:hipotap@hipotap_db:5432/hipotap_db")
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


class Order_Table(DBModel):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True)
    offer_id = Column(Integer)
    customer_id = Column(String)
    adult_count = Column(Integer)
    children_count = Column(Integer)
    price = Column(Float)
    creation_time = Column(DateTime, server_default=func.now())

    def to_pb(self) -> OrderPB:
        order_pb = OrderPB()
        order_pb.offer_id = self.offer_id
        order_pb.customer_id = self.customer_id
        order_pb.adult_count = self.adult_count
        order_pb.children_count = self.children_count
        order_pb.price = self.price
        order_pb.creation_time.FromDatetime(self.creation_time)
        return order_pb


db_session = sessionmaker(bind=engine)()
