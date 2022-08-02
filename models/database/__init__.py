from models.database.database import Database
from models.database.tinydbdatabase import TinyDBDataBase


def db_init(db_type: str, infos: dict):
    if db_type == 'TinyDB':
        return TinyDBDataBase(**infos)


