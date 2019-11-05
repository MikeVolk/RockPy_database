# db_init.py

from sqlalchemy.orm import sessionmaker

from models.definitions import Quantity, unit
from models import engine, Base

Session = sessionmaker(bind=engine)
session = Session()

def declare_core():
    # Quantities

    mass = Quantity(name='mass')
    magnetic_field = Quantity(name='magnetic_field')
    magnetic_flux = Quantity(name='magnetic_flux')
    magnetization = Quantity(name='magnetization')
    magnetic_induction = Quantity(name='magnetic_induction')
    magnetic_moment = Quantity(name='magnetic_moment')

    susceptibility = Quantity(name='susceptibility')

    # add all quantities to the session
    session.add_all([mass,
                     magnetic_field, magnetic_induction, magnetic_flux,
                     magnetization, magnetic_moment,
                     susceptibility])


    # Si units
    kilogram = unit(name = 'kg', texname = 'kg', longname='kilogram',
                    SI=True, conversion_to_si=1, offset_to_si=0)
    tesla = unit(name = 'T', texname = 'T', longname='Tesla',
                 SI=True, conversion_to_si=1, offset_to_si=0)

    # add all si units to the session
    session.add_all([kilogram, tesla])
    session.commit()



    # non SI

    gram = unit(name = 'g', texname='g', longname='gram',
                       conversion_to_si=1e3, offset_to_si=0, si_unit_id=kilogram.id)
    milligram = unit(name = 'mg', texname='mg', longname='milligram',
                            conversion_to_si=1e6, offset_to_si=0, si_unit_id=kilogram.id)
    microgram = unit(name = 'mug', texname='$\mu$g', longname='microgramm',
                            conversion_to_si=1e9, offset_to_si=0, si_unit_id=kilogram.id)



    gauss = unit(name = 'G', texname = 'G', longname='Gauss',
                        conversion_to_si=10000, offset_to_si=0, si_unit_id=tesla.id)
    gamma = unit(name = 'gamma', texname = 'gamma', longname='Gamma',
                        conversion_to_si=1e9, offset_to_si=0, si_unit_id=tesla.id)

    # add all non-si units to the session
    session.add_all([gram, milligram, microgram, gauss, gamma])
    session.commit()


    # attaching Units

    mass.si_unit.append(kilogram)
    mass.non_si_units.append(gram)
    mass.non_si_units.append(milligram)
    mass.non_si_units.append(microgram)

    magnetic_field.si_unit.append(tesla)
    magnetic_field.non_si_units.append(gauss)
    magnetic_field.non_si_units.append(gamma)

    session.commit()
    session.flush()
