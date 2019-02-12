import models
from sqlalchemy.orm import sessionmaker
from models.db_init import engine, Base
from models.definitions import  *

import os

if __name__ == '__main__':
    os.remove("/Users/mike/Documents/GitHub/RockPy_database/RockPy.db")

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # create User
    U1 = User(name='Mike')
    U2 = User(name='Chrissi')
    U3 = User(name='Hasimir')

    P1 = Project(name='Happy Family')
    U1.projects.append(P1)
    U2.projects.append(P1)

    P2 = Project(name='Hasimir der Große')
    U1.projects.append(P2)
    U2.projects.append(P2)
    U3.projects.append(P2)

    P3 = Project(name='Boston Boston')
    U1.projects.append(P3)

    for p in U1.projects:
        print(p.name, p.users)

    session.add_all([U1, U2, P1, P2, P3])

    Exp1 = Expedition(name='North Pole')
    Exp2 = Expedition(name='Eyjafjallajökull')
    Exp3 = Expedition(name='Möhrenfeld')


    Loc1 = Location(name='Santas Home')
    Exp1.locations.append(Loc1)

    Loc2 = Location(name='Weiser Hase')
    Loc3 = Location(name='Hang')
    Exp2.locations.append(Loc2)
    Exp2.locations.append(Loc3)

    Loc4 = Location(name='Haus')
    Loc5 = Location(name='Feld')
    Exp3.locations.append(Loc4)
    Exp3.locations.append(Loc5)

    P1.expeditions.append(Exp1)
    P2.expeditions.append(Exp2)
    P2.expeditions.append(Exp3)



    ########### Samples / Specimen
    s1 = Sample(name = 'A')
    sp1 = Specimen(name = '1a')
    sp2 = Specimen(name = '1b')
    sp3 = Specimen(name = '1c')

    for sp in [sp1, sp2, sp3]:
        s1.specimens.append(sp)


    Loc1.samples.append(s1)

    # print(Loc1.project)
    print(U1.__dict__)
    print(U1.expeditions)

    session.add_all([Exp1, Exp2, Exp3, Loc1,Loc2,Loc3,Loc4,Loc5])

    session.commit()
    session.flush()