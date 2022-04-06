# from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship, sessionmaker

# baza = create_engine('postgresql://hipotap:hipotap@hipotap_customer_db:5432/customer_db')

# DBModel = declarative_base()

# from .models import *
# # create tables
# DBModel.metadata.create_all(baza)
# db_session = sessionmaker(bind=baza)()
