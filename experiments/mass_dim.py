__author__ = 'Mike'
from helper import connect_db
import tabulate
from models.project import Project, Sample, SampleSet
from models.definitions import Measurement_Def, Data_Def
from models.data import Measurement, Data_Point, Data
import numpy as np


def show(project, s_set=None, samples='all'):
    session = connect_db()

    table = []

    if samples == 'all':
        set = session.query(SampleSet).filter(SampleSet.name == s_set).first()
        res = (
            session.query(Sample)
            # .join(SampleSet)     # It's necessary to join the "children" of Post
            .filter(Project.name == project)
            # here comes the magic:
            # you can filter with Tag, even though it was not directly joined)
            .filter(Sample.sample_set.contains(set))
        ).all()
        for S in res:
            print S.name
            print '-------------'
            d = None
            mass_measurements = (
                session.query(Measurement)
                .filter(Measurement.sample_id == S.id)
                .filter(Measurement.name == 'mass')
            ).all()
            height_measurements = (
                session.query(Measurement)
                .filter(Measurement.sample_id == S.id)
                .filter(Measurement.name == 'height')
            ).all()
            diameter_measurements = (
                session.query(Measurement)
                .filter(Measurement.sample_id == S.id)
                .filter(Measurement.name == 'diameter')
            ).all()

            for measurement in mass_measurements:
                mass_point = (
                    session.query(Data_Point)
                    .filter(Data_Point.measurement_id == measurement.id)
                ).all()
                for point in mass_point:
                    # print point.id
                    d = (session.query(Data)
                         .filter(Data.data_point_id == point.id).filter(Data.data_type_id == 1)).all()
                    # print d
                masses = [i.valA for i in d if type(i.valA)==float ]
                mass = np.mean(masses)
                print S.name, measurement.name, measurement.date_added, mass