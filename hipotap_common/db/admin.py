from . import DBModel, engine, db_session, Customer_Table, Offer_Table

def init_db():
    DBModel.metadata.drop_all(engine)
    DBModel.metadata.create_all(engine)

    db_session.add(Customer_Table(email="a@a", name="Joe", surname="Doe", password="123"))

    db_session.add(Offer_Table(title="offer 1"))
    db_session.add(Offer_Table(title="offer 2"))
    db_session.add(Offer_Table(title="offer 3"))
    db_session.add(Offer_Table(title="offer 4"))

    db_session.commit()
