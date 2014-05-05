import db_init
import fetch
import add
from experiments import mass_dim

add.measurement_type('mass')
project(session, 'PalInt_under_Pressure')

import_data.sample_mass_dimensions(file='/Users/Mike/Dropbox/database/demo/sample_info.csv', project='PalInt_under_Pressure',
                                  experiment='measurement of samples mass',
                                  length_unit='mm', mass_unit='mg', db=True, sample_set='LF4C')
print fetch.measurements('5a', 'mass')
# db_init.init()

# mass_dim.show(project='PalInt_under_Pressure', s_set='LF4C')



