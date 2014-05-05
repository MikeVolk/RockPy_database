__author__ = 'Mike'
from helper import connect_db
from models.definitions import Data_Def, Experiment_Def, Measurement_Def
import logging


def exp_def(name, defA=None, defB=None, defC=None, exp_class=None, comment=None, notes=None, references=None):
    '''    logging    '''
    log = logging.getLogger(name='RockPy.experiments')
    log.debug('ESTABLISHING CONNECTION to database')
    session = connect_db()
    log.debug('TRYING \t to create new experiment definition << %s >>' % name)
    res = session.query(Experiment_Def).filter(Experiment_Def.name == name).first()
    if not res:
        e_def = Experiment_Def(name=name, defA=defA, defB=defB, defC=defC,
                               exp_class=exp_class, comment=comment, notes=notes, references=references)
        log.info('SUCCESS \t new experiment definition << %s >> created' % name)
        session.add(e_def)
    if res:
        log.warning('FAIL \t << %s >>already in database, please check defintion!' % res)
    session.commit()
    session.close()


def meas_def(name, comment='', notes='', references='', measurement_class=None,
             defA=None, defB=None, defC=None, defD=None, defE=None, defF=None, defG=None, defH=None,
             defI=None, defJ=None, defK=None, defL=None, defM=None, defN=None, defO=None, defP=None,
             defQ=None, defR=None, defS=None, defT=None, defU=None, defV=None, defW=None, defX=None,
             defY=None, defZ=None):
    log = logging.getLogger(name='RockPy.measurements')
    log.debug('ESTABLISHING CONNECTION to database')
    session = connect_db()
    log.debug('TRYING \t to create new measurement definition << %s >>' % name)
    res = session.query(Measurement_Def).filter(Measurement_Def.name == name).first()
    if not res:
        e_def = Measurement_Def(name=name, comment=comment, notes=notes, measurement_class=measurement_class,
                               defA=defA, defB=defB, defC=defC, defD=defD, defE=defE, defF=defF, defG=defG, defH=defH,
                               defI=defI, defJ=defJ, defK=defK, defL=defL, defM=defM, defN=defN, defO=defO, defP=defP,
                               defQ=defQ, defR=defR, defS=defS, defT=defT, defU=defU, defV=defV, defW=defW, defX=defX,
                               defY=defY, defZ=defZ)
        log.info('SUCCESS \t new measurement definition << %s >> created' % name)
        session.add(e_def)
        if res:
            log.warning('FAIL \t << %s >> already in database, please check definition!' % res)
        session.commit()
        session.close()


def tret_def():
    pass


def d_def(name, defA, defB=None, defC=None, comment=None, notes=None):
    session = connect_db()
    res = session.query(Data_Def).filter(Data_Def.name == name).first()
    if not res:
        D_Type = Data_Def(name, defA, defB, defC, comment, notes)
        session.add(D_Type)
    else:
        print res, 'already in database, please check defintion:'
        print res.all()

    session.commit()