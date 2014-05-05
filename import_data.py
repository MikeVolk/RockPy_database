from add import measurement, sample_set, experiment, sample, data_point

__author__ = 'Mike'
from csv import reader
from datetime import datetime
import add
import helper


def sample_mass_dimensions(file, project, experiment, *args, **kwargs):
    """
    Import of Sample mass and dimension CSV files.

    :param:
       file: *str*
       project: *str*
       experiment: *str*

    :kwargs:
       mass_unit: *str* can specify the unit e.g. 'mg'
       length_unit: *str* can specify the unit for diameter and height e.g. 'mm'

    :filestructure:
       HEADER
       DATA

       :datastructure:
          Header:
           Sample \t mass \t height \t diameter

       :Data:
        Ia \t 435.2 \t 21.5 \t 23

    """ #Todo rewrite the info

    experiment_type = 'mass & dimensions'

    db = kwargs.get('db')
    natural = kwargs.get('natural')

    readall = reader(open(file), delimiter='\t')
    readall.next()

    mass_unit = kwargs.get('mass_unit')
    length_unit = kwargs.get('length_unit')
    s_set = kwargs.get('sample_set')

    entries = []

    for row in readall:  # Loop over rows of csv file
        sample = row[0]
        mass = float(row[1])
        height = float(row[2])
        diameter = float(row[3])
        aux = [sample, mass, height, diameter]
        entries.append(aux)
        #print row

    if db:
        session = helper.connect_db()
        project = helper.check_project(session, project)
        experiment = add.experiment(session=session, name=experiment, definition='mass & dimensions')

        if s_set:
            sample_set = add.sample_set(session, s_set)

        for sample in entries:
            if project:
                sample_obj = add.sample(session=session, name=sample[0], project_id=project.id)

                if s_set:
                    sample_set.samples.append(sample_obj)

                measurement = add.measurement(session=session, name='mass', definition='mass & dimensions',
                                                     sample=sample_obj, experiment=experiment, mtype='mass')
                data_point = add.data_point(session, sample, measurement)
                data = helper.input_data(session, data_point, data=sample, definition='mass')

                measurement2 = add.measurement(session=session, name='height', definition='mass & dimensions',
                                                      sample=sample_obj, experiment=experiment)
                data_point2 = add.data_point(session, sample, measurement2)
                data2 = helper.input_data(session, data_point2, data=sample, definition='height', unit='mm',
                                          unit_type='length')

                measurement3 = add.measurement(session=session, name='diameter', definition='mass & dimensions',
                                                      sample=sample_obj, experiment=experiment)
                data_point3 = add.data_point(session, sample, measurement3)
                data3 = helper.input_data(session, data_point3, data=sample, definition='diameter', unit='mm',
                                          unit_type='length')