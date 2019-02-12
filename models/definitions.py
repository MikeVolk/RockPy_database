import logging

from models import bridges
from models import db_init

from sqlalchemy import Table, Column, ForeignKey, Integer, String, Float, Boolean

from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship, backref


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
    value = Column(Float, nullable=False)
    timestamp = Column(Float, nullable=True)

    quantity_id = Column(Integer, ForeignKey('quantity.id'))
    specimen_id = Column(Integer, ForeignKey('specimen.id'))
    location_id = Column(Integer, ForeignKey('location.id'))
    machine_id = Column(Integer, ForeignKey('machine.id'))
    atmosphere_id = Column(Integer, ForeignKey('atmosphere.id'))

    protocol_id = Column(Integer, ForeignKey('protocol.id'))
    measurement_id = Column(Integer, ForeignKey('measurement.id'))
    measurement = relationship("Measurement", back_populates="data")

class Machine(db_init.Base):
    __tablename__ = 'machine'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(Integer, ForeignKey('location.id'))


class Atmosphere(db_init.Base):
    __tablename__ = 'atmosphere'
    id = Column(Integer, primary_key=True)


### measurement history

class Protocol(db_init.Base):
    __tablename__ = 'protocol'
    id = Column(Integer, primary_key=True)


class Sequence(db_init.Base):
    __tablename__ = 'sequence'
    id = Column(Integer, primary_key=True)
    instruction_id = Column(Integer, ForeignKey('instruction.id'))
    protocol_id = Column(Integer, ForeignKey('protocol.id'))
    Quantity_id = Column(Integer, ForeignKey('quantity.id'))

    Start = Column(Float, nullable=True)
    Stop = Column(Float, nullable=True)
    N = Column(Integer, nullable=True)
    Rate = Column(Float, nullable=True)
    measurements = relationship("Measurement", back_populates="sequence")
    label = Column(String, nullable=True)

    # treatment_id = Column(Integer, ForeignKey('treatment.id'))


class Instruction(db_init.Base):
    __tablename__ = 'instruction'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)


class Quantity(db_init.Base):
    __tablename__ = 'quantity'
    id = Column(Integer, primary_key=True)
    si_unit = relationship("SI_unit", back_populates="quantity")
    non_si_units = relationship("non_SI_unit", back_populates="quantity")


class SI_unit(db_init.Base):
    __tablename__ = 'si_unit'
    id = Column(Integer, primary_key=True)

    quantity_id = Column(Integer, ForeignKey('quantity.id'))
    quantity = relationship("Quantity", back_populates="si_unit", foreign_keys=[quantity_id])
    non_si_units = relationship("non_SI_unit", back_populates="si_unit")


class non_SI_unit(db_init.Base):
    __tablename__ = 'non_si_unit'
    id = Column(Integer, primary_key=True)

    conversion_to_si = Column(Float, nullable=False)
    offset_to_si = Column(Float, nullable=False)

    quantity_id = Column(Integer, ForeignKey('quantity.id'))
    quantity = relationship("Quantity", back_populates="non_si_units")

    si_unit_id = Column(Integer, ForeignKey('si_unit.id'))
    si_unit = relationship("SI_unit", back_populates="non_si_units")



class Measurement(db_init.Base):
    __tablename__ = 'measurement'
    id = Column(Integer, primary_key=True)
    sequence_id = Column(Integer, ForeignKey('sequence.id'))
    sequence = relationship("Sequence", back_populates="measurements")
    data = relationship('Data', back_populates="measurement")


db_init.Base.metadata.create_all(db_init.engine)
