from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

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


class Order_Table(DBModel):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True)
    offer_id = Column(Integer)
    customer_id = Column(String)
    price = Column(Float)


db_session = sessionmaker(bind=engine)()
