import logging

from models import db_init, bridges
from models import engine, Base

from sqlalchemy import Table, Column, ForeignKey, Integer, String, Float, Boolean, DateTime

from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship, backref


class User(Base):
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


class Project(Base):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250))

    expeditions = relationship("Expedition",
                               secondary=bridges.project_expedition_bridge,
                               backref="projects")

    def __repr__(self):
        return "<< %s >>" % (self.name)


class Expedition(Base):
    __tablename__ = 'expedition'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250))

    locations = relationship("Location",
                             secondary=bridges.expedition_location_bridge,
                             backref="expedition")

    users = association_proxy('user', 'project')


class Location(Base):
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250))
    coordinates = Column(String(250))

    samples = relationship("Sample", back_populates="location")
    project = association_proxy('expedition', 'project')

    def __repr__(self):
        return "<< %s >>" % (self.name)


class Sample(Base):
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


class Specimen(Base):
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


class Data(Base):
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True)
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=True)

    quantity_id = Column(Integer, ForeignKey('quantity.id'))
    quantity = relationship('Quantity')

    specimen_id = Column(Integer, ForeignKey('specimen.id'))
    location_id = Column(Integer, ForeignKey('location.id'))
    machine_id = Column(Integer, ForeignKey('machine.id'))

    measurement_id = Column(Integer, ForeignKey('measurement.id'))
    measurement = relationship("Measurement", back_populates="data")

    atmosphere = relationship("Atmosphere",
                              secondary=bridges.atmosphe_data_bridge,
                              backref="data")

    def is_si_unit(self, unit):
        """
        Checks if unit is the SI unit of the attached quantity

        Parameters
        ----------
        unit

        Returns
        -------
        bool
        """
        if unit in self.quantity.associated_SI_unit_names:
            return True
        else:
            return False

    def convert_to(self, unit):
        """
        Returns the conversion factor to the given unit
        Parameters
        ----------
        unit: str


        Returns
        -------
        float:
            conversion factor to the unit

        """
        if not unit in self.quantity.associated_unit_names:
            raise TypeError('%s not in unit database' % unit)
        if self.is_si_unit(unit):
            print(unit, self.quantity.associated_SI_unit_names)
            return 1
        else:
            return []


class Machine(Base):
    __tablename__ = 'machine'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(Integer, ForeignKey('location.id'))


class Atmosphere(Base):
    __tablename__ = 'atmosphere'
    id = Column(Integer, primary_key=True)
    gas = Column(String, nullable=False)
    percentage = Column(Float, nullable=False, default=100)
    data_id = Column(Integer, ForeignKey('data.id'))


### measurement history

class Protocol(Base):
    __tablename__ = 'protocol'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)


class Sequence(Base):
    __tablename__ = 'sequence'
    id = Column(Integer, primary_key=True)
    instruction_id = Column(Integer, ForeignKey('instruction.id'))
    protocol_id = Column(Integer, ForeignKey('protocol.id'))
    quantity_id = Column(Integer, ForeignKey('quantity.id'))

    Start = Column(Float, nullable=True)
    Stop = Column(Float, nullable=True)
    N = Column(Integer, nullable=True)
    Rate = Column(Float, nullable=True)
    label = Column(String, nullable=True)

    measurements = relationship("Measurement", back_populates="sequence")
    indentation = Column(String, nullable=True, default=0)

    # treatment_id = Column(Integer, ForeignKey('treatment.id'))


class Instruction(Base):
    __tablename__ = 'instruction'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)


class Quantity(Base):
    """
    Quantity object

    Parameters
    ----------
        id: automatic
        si_unit: SI_unit object
        non_si_unit: non_SI_unit object

    """
    __tablename__ = 'quantity'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    units = relationship("unit", back_populates="quantity")

    @property
    def si_unit(self):
        return [u for u in self.units if u.SI][0]

    @property
    def non_si_units(self):
        return [u for u in self.units if not u.SI]

    @property
    def associated_unit_names(self):
        """
        returns list of all unitnames associated to the quantity, both SI and Non SI
        """
        return [u.name for u in self.units] + \
               [u.longname for u in self.units] + \
               [u.texname for u in self.units]

    @property
    def associated_SI_unit_names(self):
        return [u.name for u in self.si_unit] + \
               [u.longname for u in self.si_unit] + \
               [u.texname for u in self.si_unit]


class unit(Base):
    __tablename__ = 'unit'
    id = Column(Integer, primary_key=True, autoincrement=True)
    SI = Column(Boolean, nullable=False, default=False)
    name = Column(String, nullable=False)
    longname = Column(String, nullable=False)
    texname = Column(String, nullable=False)

    quantity_id = Column(Integer, ForeignKey('quantity.id'))
    quantity = relationship("Quantity", back_populates="si_unit", foreign_keys=[quantity_id])
    # non_si_units = relationship("non_SI_unit", back_populates="si_unit")
    si_unit_id = Column(Integer)
    conversion_to_si = Column(Float, nullable=False)
    offset_to_si = Column(Float, nullable=False)


# class non_SI_unit(Base):
#     __tablename__ = 'non_si_unit'
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     longname = Column(String, nullable=False)
#     texname = Column(String, nullable=False)
#
#
#     quantity_id = Column(Integer, ForeignKey('quantity.id'))
#     quantity = relationship("Quantity", back_populates="non_si_units")
#
#     si_unit_id = Column(Integer, ForeignKey('si_unit.id'))
#     si_unit = relationship("SI_unit", back_populates="non_si_units")


class Measurement(Base):
    __tablename__ = 'measurement'
    id = Column(Integer, primary_key=True)
    sequence_id = Column(Integer, ForeignKey('sequence.id'))
    sequence = relationship("Sequence", back_populates="measurements")
    data = relationship('Data', back_populates="measurement")
