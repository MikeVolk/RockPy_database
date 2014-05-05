import data
import definitions
import project
import db_init

db_init.Base.metadata.create_all(db_init.engine)