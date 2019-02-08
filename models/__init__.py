from models import db_init

db_init.Base.metadata.create_all(db_init.engine)