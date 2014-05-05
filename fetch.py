__author__ = 'Mike'
from helper import connect_db
from models.data import Measurement
from models.definitions import Measurement_Def


def measurement_type(type, *args, **kwargs):
    session = connect_db()
    measurement_type = (
        session.query(Measurement_Def)
        .filter(Measurement_Def.name == type)
    ).first()
    if not measurement_type:
        '%s not implemented' % type

    return measurement_type


def measurements(sample_name, type, *args, **kwargs):
    session = connect_db()
    m_out = (
        session.query(Measurement)
        .filter(Measurement.name == sample_name)
        # .filter(Measurement.measurement_type_id == measurement_type(type).id)
    ).all()
    print m_out
    return m_out