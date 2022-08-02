from models.database import Database
from tinydb import TinyDB


class TinyDBDataBase(Database):
    def __init__(self, file):
        self.file = file
        self.db = TinyDB(file)

    def insert(self, cls, serialized_obj) -> int:
        table = self.db.table(name=cls.__name__.lower())
        return table.insert(serialized_obj)

    def update(self):
        pass
