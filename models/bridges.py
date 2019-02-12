from sqlalchemy import Table, Column, ForeignKey, Integer, String, Float, Boolean

from sqlalchemy import exc
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from sqlalchemy import Sequence

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from models.db_init import Base

user_project_bridge = Table('user_project_bridge', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('project_id', Integer, ForeignKey('project.id'))
)
project_expedition_bridge = Table('project_expedition_bridge', Base.metadata,
    Column('expedition_id', Integer, ForeignKey('expedition.id')),
    Column('project_id', Integer, ForeignKey('project.id'))
)
project_sample_bridge = Table('project_sample_bridge', Base.metadata,
    Column('sample_id', Integer, ForeignKey('sample.id')),
    Column('project_id', Integer, ForeignKey('project.id'))
)
expedition_location_bridge = Table('expedition_location_bridge', Base.metadata,
    Column('expedition_id', Integer, ForeignKey('expedition.id')),
    Column('location_id', Integer, ForeignKey('location.id'))
)

# experiment_protocol_bridge = Table('experiment_protocol_bridge', Base.metadata,
#     Column('experiment_id', Integer, ForeignKey('experiment.id')),
#     Column('protocol_id', Integer, ForeignKey('protocol.id'))
# )