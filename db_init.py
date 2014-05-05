from add import instrument, project, inst

__author__ = 'Mike'
import import_data
import helper
import models
from create_def import d_def , exp_def, meas_def
from models.definitions import Experiment_Def
import logging

def make_measurement_def():
    meas_def('test')

def make_data_def():
    d_def('mass', 'mass')
    d_def('height', 'height')
    d_def('diameter', 'diameter')

def make_experiment_def():
    exp_def('mass & dimensions', comment='Experiment can contain mass, diameter, height data', notes='', references='')
    exp_def('hysteresis', comment='', notes='', references='', exp_class='MvB')
    exp_def('forc', comment='', notes='', references='', exp_class='MvB')
    exp_def('thellier-thellier', comment='', notes='', references='', exp_class = 'paleointensity')

def init():
    '''
    db initialisieren
    '''
    make_experiment_def()
    make_measurement_def()
    # make_data_def()
    # make_treatment_def()

def logger():
    log = logging.getLogger(name='RockPy.database')
    log.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh = logging.FileHandler('RPV2.log')
    fh.setFormatter(formatter)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    log.addHandler(fh)
    log.addHandler(ch)

logger()
init()