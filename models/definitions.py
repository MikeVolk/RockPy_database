from sqlalchemy import Column, Integer, Text, String, Float, Date
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, Table
from sqlalchemy.ext.declarative import declarative_base

from models import bridges
from models import db_init

import logging

from sqlalchemy import Table, Column, ForeignKey, Integer, String, Float, Boolean

from sqlalchemy import exc
from sqlalchemy.ext.associationproxy import association_proxy
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

    expeditions = association_proxy('projects', 'expeditions')

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

    users = association_proxy('user', 'project')

class Location(db_init.Base):
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250))
    coordinates = Column(String(250))

    samples = relationship("Sample", back_populates="location")
    project = association_proxy('expedition', 'project')

    def __repr__(self):
        return "<< %s >>" % (self.name)


class Sample(db_init.Base):
    __tablename__ = 'sample'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250))

    # sample / location
    location_id = Column(Integer, ForeignKey('location.id'))
    location = relationship("Location", back_populates="samples")
    # sample / specimen
    specimens = relationship("Specimen", back_populates="sample")


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

    #  specimen / sample
    sample_id = Column(Integer, ForeignKey('sample.id'))
    sample = relationship("Sample", back_populates="specimens")

    # specimen / location
    location = association_proxy('sample', 'location')

    def __repr__(self):
        return "<< %s >>" % (self.name)


class Data(db_init.Base):

    __tablename__ = 'data'
    id = Column(Integer, primary_key=True)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)

    dtype_id = Column(Integer, ForeignKey('dtype.id'))
    specimen_id = Column(Integer, ForeignKey('specimen.id'))
    location_id = Column(Integer, ForeignKey('location.id'))
    measurement_id = Column(Integer, ForeignKey('measurement.id'))
    protocol_id = Column(Integer, ForeignKey('protocol.id'))
    machine_id = Column(Integer, ForeignKey('machine.id'))
    treatment_id = Column(Integer, ForeignKey('treatment.id'))
    atmosphere_id = Column(Integer, ForeignKey('atmosphere.id'))


class Dtype(db_init.Base):
    __tablename__ = 'dtype'
    id = Column(Integer, primary_key=True)

class Protocol(db_init.Base):
    __tablename__ = 'protocol'
    id = Column(Integer, primary_key=True)

class Sequence(db_init.Base):
    __tablename__ = 'sequence'
    id = Column(Integer, primary_key=True)
    treatment_id = Column(Integer, ForeignKey('treatment.id'))


class Machine(db_init.Base):
    __tablename__ = 'machine'
    id = Column(Integer, primary_key=True)

class Treatment(db_init.Base):
    __tablename__ = 'treatment'
    id = Column(Integer, primary_key=True)

class Atmosphere(db_init.Base):
    __tablename__ = 'atmosphere'
    id = Column(Integer, primary_key=True)


class SI_unit(db_init.Base):
    __tablename__ = 'si_unit'
    id = Column(Integer, primary_key=True)
    quantity = relationship("quantity", back_populates="su_unit")

class non_si_unit(db_init.Base):
    __tablename__ = 'non_si_unit'
    id = Column(Integer, primary_key=True)
    conversion_to_si = Column(Float, primary_key=True)
    quantity = relationship("quantity", back_populates="su_unit")
    si_unit = relationship("si_unit", back_populates="non_su_units")


class Quantity(db_init.Base):
    __tablename__ = 'quantity'
    id = Column(Integer, primary_key=True)


db_init.Base.metadata.create_all(db_init.engine)