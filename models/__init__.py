from models.fields import Field
from models.database import Database, db_init
from models.models import Model

def change_db_settings(db_type: str, infos: dict):
    Model.database = db_init(db_type=db_type, infos=infos)




