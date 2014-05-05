import RockPy.helper as RPhelper
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.project import Project, Sample

from models.data import Data
from models.definitions import Data_Def
import logging


def connect_db(db_name='sqlite:///PHD-data.db', echo=True):

    log = logging.getLogger(name='RockPy.database')
    log.info('connecting to database << %s >>' %db_name)
    engine = create_engine(db_name)

    # create a Session
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def check_sample_exists(session, name, *args):
    res = session.query(Sample).filter(Sample.name == name).first()
    if res:
        OUT = res
        print '#', res.name, 'already in database'
        if 'delete' in args:
            session.delete(res)
            session.commit()
    else:
        OUT = False
    return OUT


def check_project(session, name, *args, **kwargs):
    res = session.query(Project).filter(Project.name == name).first()
    if res:
        return res
    else:
        print 'Project: \'%s\' does not exist. Please initiate first using helper.new_project(session, project_name)' % name
        return


def import_structure():
    structure = {'project_id': 1,
                 'location_id': 2,
                 'name': 3,
                 'comment': 5,
                 'desription': 6,
                 'notes': 7,
                 'natural': 8,
                 'diameter': 9,
                 'height': 10,
                 'mass': 11,
                 'prep_date': 12
    }
    return structure


def input_data(session, point, data, definition, unit='mg', unit_type='mass'):
    res = session.query(Data_Def).filter(Data_Def.name == definition).first()
    if not res:
        print 'Data definition <%s> non existent, please check' % definition
        return
    d = Data()
    d.data_type_id = res.id
    d.data_point_id = point.id

    #Todo  def SI_Unit(unit_type)-> returns e.g. 'kg'
    ### conversion from input unit to storage unit [SI]
    if unit != 'kg' and unit_type == 'mass':
        d_conv = data[1]
        d_conv *= RPhelper.convert2(unit, 'kg', 'mass')
        d.unit = 'kg'
    if unit != 'm' and unit_type == 'length':
        if definition == 'height':
            d_conv = data[2]
        if definition == 'diameter':
            d_conv = data[3]

        d_conv *= RPhelper.convert2(unit, 'm', 'length')
        d.unit = 'm'

    d.valA = d_conv
    d.physical_property = definition

    session.add(d)
    session.commit()


def new_subsamples():
    pass


def new_project():
    pass

