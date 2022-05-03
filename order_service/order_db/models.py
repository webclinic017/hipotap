from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine(
    "postgresql://hipotap:hipotap@hipotap_order_db:5432/order_db"
)
DBModel = declarative_base()


class Order_Table(DBModel):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True)
    offer_id = Column(Integer)
    customer_id = Column(String)
    price = Column(Float)


DBModel.metadata.drop_all(engine)
DBModel.metadata.create_all(engine)

db_session = sessionmaker(bind=engine)()
db_session.commit()
