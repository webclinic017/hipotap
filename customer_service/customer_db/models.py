from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine(
    "postgresql://hipotap:hipotap@hipotap_customer_db:5432/customer_db"
)
DBModel = declarative_base()


class Customer_Table(DBModel):
    __tablename__ = "customer"
    email = Column(String(100), primary_key=True)
    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)


DBModel.metadata.drop_all(engine)
DBModel.metadata.create_all(engine)

db_session = sessionmaker(bind=engine)()
db_session.add(Customer_Table(email="a@a", name="Joe", surname="Doe", password="123"))
db_session.commit()
