# db_init.py
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///../PHD-data.db')
Base = declarative_base()


