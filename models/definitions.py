from sqlalchemy import Column, Integer, Text, String, Float, Date
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, Table
from sqlalchemy.ext.declarative import declarative_base
import db_init
import logging


class Experiment_Def(db_init.Base):
    log = logging.getLogger(name='RockPy.experiments')
    log.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh = logging.FileHandler('RPV2.log')
    fh.setFormatter(formatter)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    log.addHandler(fh)
    log.addHandler(ch)
    ''' describes the type of experiment '''
    __tablename__ = "experiment_defs"
    id = Column(Integer, primary_key=True)  # individual id for each set
    name = Column(Text)  # name of set
    comment = Column(String)  # user comment
    notes = Column(String)
    reference = Column(String)
    exp_class = Column(String)

    defA = Column(String)
    defB = Column(String)
    defC = Column(String)
    defD = Column(String)

    date_added = Column(Date)

    def __init__(self, name, defA, defB=None, defC=None,
                 comment=None, notes=None, references=None, exp_class=None):
        self.name = name
        self.defA = defA
        self.defB = defB
        self.defC = defC
        self.comment = comment
        self.notes = notes
        self.exp_class = exp_class

    def __repr__(self):
        return "<Experiment Definition: %s>" % self.name


class Measurement_Def(db_init.Base):
    log = logging.getLogger(name='RockPy.measurements')
    log.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh = logging.FileHandler('RPV2.log')
    fh.setFormatter(formatter)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    log.addHandler(fh)
    log.addHandler(ch)

    ''' describes the type of measurement '''

    __tablename__ = "measurement_defs"
    id = Column(Integer, primary_key=True)  # individual id for each set
    name = Column(Text)  # name of measurement
    comment = Column(String)  # user comment
    notes = Column(String)
    reference = Column(String)
    measurement_class = Column(String)

    '''
    defA-defM are the definitions for certain parameters that get their values from the measurement table. For expample
    for a Hysteresis @ VFTB:
    valA: 20        defA: temp
    valB: 1         defB: dwelltime
    valC: None      defC: amplitude
    calD: 1         defD: gain
    '''

    defA = Column(String)
    defB = Column(String)
    defC = Column(String)
    defD = Column(String)
    defE = Column(String)
    defF = Column(String)
    defG = Column(String)
    defH = Column(String)
    defI = Column(String)
    defJ = Column(String)
    defK = Column(String)
    defL = Column(String)
    defM = Column(String)
    defN = Column(String)
    defO = Column(String)
    defP = Column(String)
    defQ = Column(String)
    defR = Column(String)
    defS = Column(String)
    defT = Column(String)
    defU = Column(String)
    defV = Column(String)
    defW = Column(String)
    defX = Column(String)
    defY = Column(String)
    defZ = Column(String)

    date_added = Column(Date)

    def __init__(self, name, comment='', notes='', measurement_class=None,
                 defA=None, defB=None, defC=None, defD=None, defE=None, defF=None, defG=None, defH=None, defI=None,
                 defJ=None, defK=None, defL=None, defM=None, defN=None, defO=None, defP=None, defQ=None, defR=None,
                 defS=None, defT=None, defU=None, defV=None, defW=None, defX=None, defY=None, defZ=None):
        """"""
        self.name = name
        self.defA = defA
        self.defB = defB
        self.defC = defC
        self.defD = defD
        self.defE = defE
        self.defF = defF
        self.defG = defG
        self.defH = defH
        self.defI = defI
        self.defJ = defJ
        self.defK = defK
        self.defL = defL
        self.defM = defM
        self.defN = defN
        self.defO = defO
        self.defP = defP
        self.defQ = defQ
        self.defR = defR
        self.defS = defS
        self.defT = defT
        self.defU = defU
        self.defV = defV
        self.defW = defW
        self.defX = defX
        self.defY = defY
        self.defZ = defZ

        self.comment = comment
        self.notes = notes
        self.measurement_class = measurement_class

    def __repr__(self):
        return "<Measurement Definition: %s>" % self.name


class Treatment_Def(db_init.Base):
    ''' describes the type of treatment '''
    __tablename__ = "treatment_defs"
    id = Column(Integer, primary_key=True)  # individual id for each set
    name = Column(Text)  # name of set
    comment = Column(String)  # user comment
    notes = Column(String)
    reference = Column(String)

    '''
    defA-defM are the definitions for certain parameters that get their values from the treatment table. For expample
    for HCl clean:

    Treatment       Treatment_Type
    valA: 10        defA: [%]
    valB: 20        defB: Temperature
    valC: 86400     defC: Time[s]
    '''

    defA = Column(String)
    defB = Column(String)
    defC = Column(String)
    defD = Column(String)
    defE = Column(String)
    defF = Column(String)
    defG = Column(String)
    defH = Column(String)
    defI = Column(String)
    defJ = Column(String)
    defK = Column(String)
    defL = Column(String)
    defM = Column(String)

    date_added = Column(Date)


class Data_Def(db_init.Base):
    ''' describes the type of data '''
    __tablename__ = "data_defs"
    id = Column(Integer, primary_key=True)  # individual id for each set
    name = Column(Text)  # name of set
    comment = Column(String)  # user comment
    notes = Column(String)
    defA = Column(String)
    defB = Column(String)
    defC = Column(String)

    def __init__(self, name, defA, defB, defC, comment, notes):
        """"""
        self.name = name
        self.defA = defA
        self.defB = defB
        self.defC = defC
        self.comment = comment
        self.notes = notes


    def all(self):
        print '--------------------'
        print '\t', self.name
        print '--------------------'
        print 'comment: ', self.comment
        print 'notes: ', self.notes
        print 'definition A: ', self.defA
        print 'definition B: ', self.defB
        print 'definition C: ', self.defC

    def __repr__(self):
        return "<Data Type: %s>" % self.name