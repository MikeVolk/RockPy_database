from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///RockPy.db')
Base = declarative_base()

from models import db_init

db_init.Base.metadata.create_all(db_init.engine)