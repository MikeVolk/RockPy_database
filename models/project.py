from math import pi
from RockPy import helper
from sqlalchemy import Column, Integer, Text, String, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import relation, backref
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, Table
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import db_init


class Project(db_init.Base):
    """"""
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(Text) # name of set
    comment = Column(String) # user comment
    notes = Column(String)
    date_added = Column(DateTime)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Project: %s" % self.name


class Site(db_init.Base):
    """"""
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True)


class SampleSet(db_init.Base):
    ''' describes a set of samples '''
    __tablename__ = "sample_sets"
    id = Column(Integer, primary_key=True) # individual id for each set
    name = Column(String(30)) # name of set
    comment = Column(String) # user comment
    notes = Column(String)

    # samples = association_proxy('sample_sets_samples', 'samples')
    samples = relationship("Sample", secondary=lambda: Sample_Set_Samples)

    def __init__(self, name, comment=None):
        self.name = name
        self.comment = comment


    def __repr__(self):
        return "<SampleSet %s>" % self.name
        #
        # def _find_or_create_set(self, tag):
        #     q = Tag.query.filter_by(name=tag)
        #     t = q.first()
        #     if not(t):
        #         t = Tag(tag)
        #     return t
        #
        # def _get_tags(self):
        #     return [x.name for x in self.tags]
        #
        # def _set_tags(self, value):
        #     # clear the list first
        #     while self.tags:
        #         del self.tags[0]
        #     # add new tags
        #     for tag in value:
        #         self.tags.append(self._find_or_create_tag(tag))
        #
        #     str_tags = property(_get_tags,
        #                         _set_tags,
        #                         "Property str_tags is a simple wrapper for tags relation")


# class SampleSet_Sample(db_init.Base):
#     __tablename__ = 'sample_sets_samples'
#     sample_set_id = Column(Integer, ForeignKey('sample_sets.id'), primary_key=True)
#     sample_id = Column(Integer, ForeignKey('samples.id'), primary_key=True)
#     special_key = Column(String(50))
#
#     # bidirectional attribute/collection of "set"/"samples"
#     sample_set = relationship(SampleSet,
#                               backref=backref("user_keywords",
#                                               cascade="all, delete-orphan"))
#
#     # reference to the "Sample" object
#     sample = relationship("Sample")
#
#     def __init__(self, sample_set=None, sample=None, special_key=None):
#         self.sample_set = sample_set
#         self.sample = sample
#         self.special_key = special_key


class Sample(db_init.Base):
    """"""
    __tablename__ = "samples"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    location_id = Column(Integer, ForeignKey("locations.id"))

    name = Column(String)
    comment = Column(String)
    description = Column(String)
    notes = Column(String)

    natural = Column(Boolean)

    #### from automag ###
    #mag_azimuth = Column( Float) # insitu orientation correction: azimuth of sample
    #sun_azimuth = Column( Float) # insitu orientation correction: azimuth from sun compass
    #hade = Column( Float) # insitu orientation correction: hade of sample
    #dip = Column( Float) # bedding correction: dip angle
    #dipdir = Column( Float) # bedding correction: dip direction
    #stratigraphic_level = Column( Float) # stratigraphic height of sample
    #geo_lat = Column( Float) # geograpic coordinates latitude
    #geo_lon = Column( Float) # geographic coordinates longitude
    #geo_alt = Column( Float) # geographic altitude
    #orientation_time_utc = Column( DateTime) # date and time of sample orientation in the field
    #field_inclination = Column( Float) # measured magnetic field inclination at sampling location
    #field_strength = Column( Float) # measured field intensity

    # stored in SI units: d[m] h[m] m[kg]
    # Todo mass Diameter, height as separate measurements, sample.mass -> last mass measurement

    prep_date = Column(DateTime)
    date_added = Column(DateTime)

    sample_set = relationship("SampleSet", secondary=lambda: Sample_Set_Samples)

    def __repr__(self):
        return "<Sample %s>" % self.name


    #def SetFieldData( self, fielddata):
    #    self.mag_azimuth = fielddata['mag_azimuth']
    #    self.sun_azimuth = fielddata['sun_azimuth']
    #    self.hade = fielddata['hade']
    #    self.dip = fielddata['dip']
    #    self.dipdir = fielddata['dipdir']
    #    self.stratigraphic_level = fielddata['stratigraphic_level']
    #    self.geo_lat = fielddata['geo_lat']
    #    self.geo_lon = fielddata['geo_lon']
    #    self.geo_alt = fielddata['geo_alt']
    #    self.orientation_time_utc = fielddata['orientation_time_utc']
    #    self.field_inclination = fielddata['field_inclination']
    #    self.field_strength = fielddata['field_strength']

    #----------------------------------------------------------------------
    def __init__(self, name):
        """"""
        self.name = name
        #self.mass = mass

    def mass_conv(self, out_unit):
        return self.mass * helper.convert2('kg', out_unit, 'mass')

    def volume(self):
        OUT = (self.diameter / 2) ** 2 * pi
        return OUT


Sample_Set_Samples = Table('sample_sets_samples', db_init.Base.metadata,
                           Column('sampleset_id', Integer, ForeignKey('sample_sets.id')),
                           Column('sample_id', Integer, ForeignKey('samples.id')))