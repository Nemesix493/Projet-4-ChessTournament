from tinydb import TinyDB, where
from tinydb.table import Document


class TinyDBDataBase:
    def __init__(self, file: str):
        self.file = file
        self.db = TinyDB(file)

    def insert(self, cls: type, serialized_obj: dict) -> int:
        table = self.db.table(name=cls.__name__.lower())
        return table.insert(serialized_obj)

    def update(self, cls: type, serialized_obj: dict, pk: int) -> None:
        table = self.db.table(name=cls.__name__.lower())
        table.upsert(Document(serialized_obj, doc_id=pk))

    def get(self, cls: type, key_name: str, value) -> dict | None:
        table = self.db.table(name=cls.__name__.lower())
        if key_name == 'pk':
            doc = table.get(doc_id=value)
        else:
            docs = table.search(where(key_name) == value)
            if docs:
                doc = docs[0]
            else:
                return None
        result = {
            'pk': doc.doc_id
        }
        for key, val in doc.items():
            result[key] = val
        return result

    def get_all(self, cls: type, key_name: str | None, value) -> list[dict]:
        table = self.db.table(name=cls.__name__.lower())
        result = []
        docs = []
        if key_name is None or value is None:
            docs = table.all()
        else:
            docs = table.search(where(key_name) == value)
        for doc in docs:
            doc_dict = {
                'pk': doc.doc_id
            }
            for key, val in doc.items():
                doc_dict[key] = val
            result.append(doc_dict)
        return result

    def remove(self, cls: type, pk: int) -> None:
        table = self.db.table(name=cls.__name__.lower())
        table.remove(doc_ids=[pk])
