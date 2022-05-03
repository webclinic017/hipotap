from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine(
    "postgresql://hipotap:hipotap@hipotap_offer_db:5432/offer_db"
)
DBModel = declarative_base()


class Offer_Table(DBModel):
    __tablename__ = "offer"
    id = Column(Integer, primary_key=True)
    title = Column(String(100))


DBModel.metadata.drop_all(engine)
DBModel.metadata.create_all(engine)

db_session = sessionmaker(bind=engine)()
db_session.add(Offer_Table(title="offer 1"))
db_session.add(Offer_Table(title="offer 2"))
db_session.add(Offer_Table(title="offer 3"))
db_session.add(Offer_Table(title="offer 4"))
db_session.commit()
