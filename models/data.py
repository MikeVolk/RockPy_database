from sqlalchemy import Column, Integer, Text, String, Float, Date, DateTime
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation

import db_init


class Experiment(db_init.Base):
    ''' describes the different experiments '''
    __tablename__ = "experiments"
    id = Column(Integer, primary_key=True) # individual id for each set
    experiment_type_id = Column(Integer, ForeignKey('experiment_defs.id'))
    name = Column(Text) # name of set
    comment = Column(String) # user comment
    notes = Column(String)
    reference = Column(String)

    '''
    defA-defM are the definitions for certain parameters that get their definitions from the experiment table. For expample
    for a pTRM:
    valA: 10        defA: C/min
    valB: 100       defB: Tmin
    valC: 200       defC: Tmax
    calD: 35e-6     defD: field
    '''
    valA = Column(Float)
    valB = Column(Float)
    valC = Column(Float)
    valD = Column(Float)
    valE = Column(Float)
    valF = Column(Float)
    valG = Column(Float)
    valH = Column(Float)
    valI = Column(Float)
    valJ = Column(Float)
    valK = Column(Float)
    valL = Column(Float)
    valM = Column(Float)

    date_added = Column(Date)

    def __init__(self, name):
        """"""
        self.name = name
        #self.mass = mass


class Instrument(db_init.Base):
    ''' describes a set of samples '''
    __tablename__ = "instruments"
    id = Column(Integer, primary_key=True) # individual id for each set
    name = Column(Text)  # name of set
    company = Column(Text)  # name of set
    serial_nr = Column(Text)
    comment = Column(String)  # user comment
    notes = Column(String)
    reference = Column(String)

    last_calibration_date = Column(DateTime)
    date_added = Column(Date)

    def __init__(self, name):
        """"""
        self.name = name
        #self.mass = mass

    def __repr__(self):
        return "Instrument: %s - %s SN: %s" % (self.company, self.name, self.serial_nr)


class Treatment(db_init.Base):
    ''' describes a set of samples '''
    __tablename__ = "treatments"
    id = Column(Integer, primary_key=True) # individual id for each set
    name = Column(Text) # name of set
    comment = Column(String) # user comment
    notes = Column(String)
    reference = Column(String)

    '''
    valA-valM are the values for certain parameters defined by defA-defM in the treatment_defs table. For expample
    for HCl clean:

    Treatment       Treatment_Type
    valA: 10        defA: [%]
    valB: 20        defB: Temperature
    valC: 86400     defC: Time[s]
    '''

    valA = Column(Float)
    valB = Column(Float)
    valC = Column(Float)
    valD = Column(Float)
    valE = Column(Float)
    valF = Column(Float)
    valG = Column(Float)
    valH = Column(Float)
    valI = Column(Float)
    valJ = Column(Float)
    valK = Column(Float)
    valL = Column(Float)
    valM = Column(Float)

    date_added = Column(Date)


class Measurement(db_init.Base):
    ''' describes a set of samples '''
    __tablename__ = "measurements"
    id = Column(Integer, primary_key=True) # individual id for each set
    calibration_id = Column(Integer) # individual id for each set
    name = Column(Text) # name of set
    comment = Column(String) # user comment
    notes = Column(String)
    reference = Column(String)

    instrument = Column(Integer, ForeignKey('instruments.id'))
    treatment_id = Column(Integer, ForeignKey('treatments.id'))
    sample_id = Column(Integer, ForeignKey('samples.id'))
    experiment_id = Column(Integer, ForeignKey('experiments.id'))
    measurement_type_id = Column(Integer, ForeignKey('measurement_defs.id'))

    #calibrations = relation("Calibration", secondary=Calibration)

    '''
    valA-valM are the values for certain parameters defined by defA-defM in the measurement_defs table. For expample
    for a Hysteresis @ VFTB:
    valA: 20        defA: temp
    valB: 1         defB: dwelltime
    valC: None      defC: amplitude
    calD: 1         defD: gain
    '''

    valA = Column(Float)
    valB = Column(Float)
    valC = Column(Float)
    valD = Column(Float)
    valE = Column(Float)
    valF = Column(Float)
    valG = Column(Float)
    valH = Column(Float)
    valI = Column(Float)
    valJ = Column(Float)
    valK = Column(Float)
    valL = Column(Float)
    valM = Column(Float)

    date_added = Column(Date)

    def __init__(self, name):
        """"""
        self.name = name
        #self.mass = mass

    def __repr__(self):
        return "<Measurement: %s %s>" % (self.name, self.instrument)


class Data_Point(db_init.Base):
    ''' describes a set of samples '''
    __tablename__ = "data_points"
    id = Column(Integer, primary_key=True) # individual id for each set
    measurement_id = Column(Integer, ForeignKey('measurements.id'))
    time = Column(DateTime)


class Data(db_init.Base):
    ''' describes a set of samples '''
    __tablename__ = "data"
    id = Column(Integer, primary_key=True) # individual id for each set
    data_point_id = Column(Integer, ForeignKey('data_points.id'))
    data_type_id = Column(Integer, ForeignKey('data_defs.id'))
    valA = Column(Float)
    valB = Column(Float)
    valC = Column(Float)
    physical_property = Column(String)
    unit = Column(String)

    def __repr__(self):
        return "<Data: %f unit: %s>" % (self.valA, self.unit)


class Calibration(db_init.Base):
    """ connects a measurement with a calibration measurement:
        assume:
            hysteresis calibration measurement id = 1
        the measurement following it will have:
            id = 2
            measurement_id = 1 -> linking the new measurement to the previous for calibration reference
    """
    __tablename__ = "calibrations"
    id = Column(Integer, primary_key=True)
    measurements_id = Column(Integer, ForeignKey('measurements.id'))
    calibration_measurement_id = Column(Integer, ForeignKey('measurements.calibration_id'))