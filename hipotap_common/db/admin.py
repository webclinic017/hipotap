from datetime import datetime

from . import DBModel, engine, db_session, Customer_Table, Offer_Table
from .scrapper import Scrapper


def init_db():
    scrapper = Scrapper()
    offers_dict = scrapper.parce()
    DBModel.metadata.drop_all(engine)
    DBModel.metadata.create_all(engine)

    db_session.add(Customer_Table(email="a@a", name="Joe", surname="Doe", password="123"))

    for offer in offers_dict:
        db_session.add(Offer_Table(
            title=offer["title"],
            description=offer["description"],
            place=offer["place"],
            hotel=offer["hotel"],
            max_adult_count=offer["max_adult_count"],
            max_children_count=offer["max_children_count"],
            price_adult=offer["price_adult"],
            price_children=offer["price_children"],
            date_start=datetime.strptime(offer["date_start"], '%d/%m/%y %H:%M:%S'),
            date_end=datetime.strptime(offer["date_end"], '%d/%m/%y %H:%M:%S')
        ))

    db_session.commit()
