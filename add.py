import datetime
import helper
from models.data import Measurement, Instrument, Experiment, Data_Point, Data
from models.definitions import Experiment_Def, Measurement_Def
from models.project import SampleSet, Project, Sample
import fetch

__author__ = 'Mike'


def measurement(session, name, definition, sample, experiment, **kwargs):
    measurement = Measurement(name)
    measurement.comment = kwargs.get('comment')
    measurement.description = kwargs.get('description')
    measurement.notes = kwargs.get('notes')
    measurement.experiment_id = experiment.id
    measurement.sample_id = sample.id
    measurement.date_added = datetime.datetime.now()

    if 'mtype' in kwargs:
        m_type = fetch.measurement_type(kwargs['mtype'])
        if m_type:
            measurement.measurement_type_id = m_type.id


    session.add(measurement)
    session.commit()
    return measurement

class new(object):

    def __init__(self, session, name, type, notes=None, comment=None):
        res = session.query(type).filter(type.name == name).first()
        if res:
            print '%s already exists' % res
            print 'if same machine exists twice, add serial number [serial_nr]'# or location [location]'
        if not res:
            type = type(name)
            type.comment = comment
            type.notes = notes
            type.date_added = datetime.datetime.now()
            session.add(type)


class inst(new):
    def __init__(self, session, name, reference=None, notes=None, serial_nr=None, description=None,
               company=None, comment=None):
        super(inst, self).__init__(session=session, name=name, type=Instrument, notes=notes, comment=comment)

def instrument(session, name, reference=None, notes=None, serial_nr=None, description=None,
               company=None, comment=None, **kwargs):
    res, res_serial = None, None

    if serial_nr:
        res_serial = session.query(Instrument).filter(Instrument.name == name). \
            filter(Instrument.serial_nr == serial_nr).first()
    else:
        res = session.query(Instrument).filter(Instrument.name == name).first()

    if res:
        print '%s already exists' % res
        print 'if same machine exists twice, add serial number [serial_nr]'# or location [location]'

    if res_serial:
        print '%s already exists' % res_serial

    if not res:
        instrument = Instrument(name)
        instrument.comment = comment
        instrument.company = company
        instrument.description = description
        instrument.serial_nr = serial_nr
        instrument.notes = notes
        instrument.reference = reference
        instrument.date_added = datetime.datetime.now()
        session.add(instrument)

    session.commit()


def sample_set(session, name, **kwargs):
    res = session.query(SampleSet).filter(SampleSet.name == name).first()
    if res:
        print 'sample_set: <%s> already in database' % name
        return res
    if not res:
        sample_set = SampleSet(name)
        sample_set.comment = kwargs.get('comment')
        sample_set.description = kwargs.get('description')
        sample_set.notes = kwargs.get('notes')
        session.add(sample_set)
        session.commit()
        return sample_set


def experiment(session, name, definition, **kwargs):
    res = session.query(Experiment_Def).filter(Experiment_Def.name == definition).first()
    if not res:
        print 'experiment definition <%s> not implemented yet' % definition

    if res:
        experiment = Experiment(name)
        experiment.experiment_def_id = res.id
        experiment.comment = kwargs.get('comment')
        experiment.description = kwargs.get('description')
        experiment.notes = kwargs.get('notes')
        experiment.reference = kwargs.get('reference')
        experiment.last_calibration_date = kwargs.get('last_calibration_date')
        experiment.date_added = datetime.datetime.now()
        session.add(experiment)
        return experiment
    session.commit()


def project(session, name, **kwargs):
    res = session.query(Project).filter(Project.name == name).first()
    if res:
        print '%s already exists' % res
    if not res:
        project = Project(name)
        project.comment = kwargs.get('comment')
        project.description = kwargs.get('description')
        project.notes = kwargs.get('notes')
        project.date_added = datetime.datetime.now()
        session.add(project)

    session.commit()


def sample(session, name, **kwargs):
    '''
    Generates a new sample in the database.

    **kwargs:

       project_id: specify project id the sample belongs to
       location_id: specify location id the sample was taken from
       comment: add a comment
       description: add description to sample
       notes: add notes for sample
       natural: True or False
       prep_date: datetime - date / time of preparation
    '''

    mass = kwargs.get('mass', None)

    if 'mass_unit' in kwargs:
        if 'mass' in kwargs:
            mass = kwargs['mass'] * helper.convert2(kwargs['mass_unit'], 'kg', 'mass')

    if 'length_unit' in kwargs:
        if 'height' in kwargs:
            kwargs['height'] *= helper.convert2(kwargs['length_unit'], 'm', 'length')
        if 'diameter' in kwargs:
            kwargs['diameter'] *= helper.convert2(kwargs['length_unit'], 'm', 'length')

    check = helper.check_sample_exists(session, name)
    set = kwargs.get('sample_set')
    if not check:
        sample = Sample(name)
        sample.mass = mass
        sample.project_id = kwargs.get('project_id')
        sample.location_id = kwargs.get('location_id')
        sample.comment = kwargs.get('comment')
        sample.description = kwargs.get('description')
        sample.notes = kwargs.get('notes')
        sample.natural = kwargs.get('natural', False)
        sample.height = kwargs.get('height')
        sample.diameter = kwargs.get('diameter')
        sample.prep_date = kwargs.get('prep_date')
        sample.date_added = datetime.datetime.now()
        if set:
            sample.sample_sets = set

        session.add(sample)
        return sample
    else:
        return check
    session.commit()


def measurement_type(name, **kwargs):
    session = helper.connect_db()

    res = fetch.measurement_type(name)
    if not res:
        mdef = Measurement_Def(name)
        mdef.comment = kwargs.get('comment')
        mdef.notes = kwargs.get('notes')
        mdef.reference = kwargs.get('reference')

        mdef.defA = kwargs.get('defA')
        mdef.defB = kwargs.get('defB')
        mdef.defC = kwargs.get('defC')
        mdef.defD = kwargs.get('defD')
        mdef.defE = kwargs.get('defE')
        mdef.defF = kwargs.get('defF')
        mdef.defG = kwargs.get('defG')
        mdef.defH = kwargs.get('defH')
        mdef.defI = kwargs.get('defI')
        mdef.defJ = kwargs.get('defJ')
        mdef.defK = kwargs.get('defK')
        mdef.defL = kwargs.get('defL')
        mdef.defM = kwargs.get('defM')

        mdef.date_added = datetime.datetime.now()
        session.add(mdef)
        session.commit()
        return mdef
    else:
        return res


def data_point(session, point_data, measurement):
    point = Data_Point()
    point.measurement_id = measurement.id
    data = Data()
    session.add(point)
    session.commit()
    return point