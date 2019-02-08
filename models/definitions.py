from sqlalchemy import Column, Integer, Text, String, Float, Date
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, Table
from sqlalchemy.ext.declarative import declarative_base

from models import bridges
from models import db_init

import logging

from sqlalchemy import Table, Column, ForeignKey, Integer, String, Float, Boolean

from sqlalchemy import exc
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from sqlalchemy import Sequence

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

class User(db_init.Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    affiliation = Column(String(250))
    email = Column(String(250))
    comment = Column(String(250))
    projects = relationship("Project",
                            secondary=bridges.user_project_bridge,
                            backref="users")

    def __repr__(self):
        return "<< %s >>" % (self.name)


class Project(db_init.Base):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250))

    expeditions = relationship("Expedition",
                               secondary=bridges.project_expedition_bridge,
                               backref="projects")

    def __repr__(self):
        return "<< %s >>" % (self.name)


class Expedition(db_init.Base):
    __tablename__ = 'expedition'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250))

    locations = relationship("Location",
                             secondary=bridges.expedition_location_bridge,
                             backref="expedition")

    def __repr__(self):
        return "<< %s >>" % (self.name)


class Location(db_init.Base):
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250))
    coordinates = Column(String(250))

    samples = relationship("Sample", back_populates="location")

    def __repr__(self):
        return "<< %s >>" % (self.name)


class Sample(db_init.Base):
    __tablename__ = 'sample'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250))

    location_id = Column(Integer, ForeignKey('location.id'))
    location = relationship("Location", back_populates="samples")

    specimens = relationship("Specimen", back_populates="sample")

#     expedition = relationship("Expedition", secondary="location",
#                               primaryjoin="Sample.location_id == Location.id",
#                               secondaryjoin="Expedition.id == Location.expedition_id",
#                               viewonly=True)

    projects = relationship("Project",
                            secondary=bridges.project_sample_bridge,
                            backref="samples")

    def __repr__(self):
        return "<< %s >>" % (self.name)


class Specimen(db_init.Base):
    __tablename__ = 'specimen'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250))
    sample_id = Column(Integer, ForeignKey('sample.id'))
    sample = relationship("Sample", back_populates="specimens")

    def __repr__(self):
        return "<< %s >>" % (self.name)


db_init.Base.metadata.create_all(db_init.engine)