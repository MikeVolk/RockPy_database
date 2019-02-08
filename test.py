import models
from sqlalchemy.orm import sessionmaker
from models.db_init import engine
from models.definitions import  *
if __name__ == '__main__':

    Session = sessionmaker(bind=engine)
    session = Session()

    # create User
    U1 = User(name='Mike')
    U2 = User(name='Chrissi')

    P1 = Project(name='Happy Family')
    P2 = Project(name='Hasimir der Große')
    P3 = Project(name='Boston Boston')

    U1.projects.append(P1)
    U2.projects.append(P1)
    U1.projects.append(P2)
    U1.projects.append(P3)

    for p in U1.projects:
        print(p.name, p.users)

    session.add_all([U1, U2, P1, P2, P3])