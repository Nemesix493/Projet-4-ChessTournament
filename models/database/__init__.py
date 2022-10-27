from .databaseinterface import DatabaseInterface
from .tinydbdatabase import TinyDBDatabase
from settings import DATABASE


def load_database() -> DatabaseInterface:
    """
    Return the database in settings
    :return: DatabaseInterface
    """
    if DATABASE['type'] == 'tinydb':
        return TinyDBDatabase(file=DATABASE['file'])
