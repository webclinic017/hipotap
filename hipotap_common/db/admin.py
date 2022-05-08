from datetime import datetime

from . import DBModel, engine, db_session, Customer_Table, Offer_Table

def init_db():
    DBModel.metadata.drop_all(engine)
    DBModel.metadata.create_all(engine)

    db_session.add(Customer_Table(email="a@a", name="Joe", surname="Doe", password="123"))

    db_session.add(Offer_Table(
        title='Super wypoczynek w Costa Brava',
        description='super wypoczynek dla całej rodziny',
        place='Costa Brava',
        hotel='Grand Hotel',
        max_adult_count=2,
        max_children_count=2,
        price_adult=2.20,
        price_children=3.30,
        date_start=datetime.strptime('23/02/23 00:00:00', '%d/%m/%y %H:%M:%S'),
        date_end=datetime.strptime('01/03/23 00:00:00', '%d/%m/%y %H:%M:%S')
    ))
    db_session.add(Offer_Table(
        title='Super wypoczynek w Grecji',
        description='super wypoczynek dla całej dorosłych',
        place='Grecja',
        hotel='Hotel Mercury',
        max_adult_count=2,
        max_children_count=0,
        price_adult=2.20,
        price_children=0,
        date_start=datetime.strptime('11/09/23 00:00:00', '%d/%m/%y %H:%M:%S'),
        date_end=datetime.strptime('22/09/23 00:00:00', '%d/%m/%y %H:%M:%S')
    ))

    db_session.commit()
