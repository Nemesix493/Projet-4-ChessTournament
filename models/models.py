from models import Field, db_init


class Model:
    initialized = False
    database = db_init("TinyDB", {'file': 'test.json'})

    def __new__(cls, *args, **kwargs):
        if cls.initialized:
            return super(Model, cls).__new__(cls)
        else:
            raise Exception('models not initialized')

    @classmethod
    def get(cls, **query):
        doc = cls.database.get(cls=cls, **query)
        for key, val in cls.__dict__.items():
            if isinstance(val, Field):
                if not val.serialize:
                    doc[key] = val.load_function(doc['id'])
        return cls(**doc)

    @classmethod
    def getall(cls, **query):
        pass

    def __init__(self, **kwargs):
        if 'id' in kwargs.keys():
            self.id = kwargs['id']
        else:
            self.id = None
        for key, field in self.__class__.__dict__.items():
            if isinstance(field, Field) and key in kwargs.keys():
                self.__setattr__(key, field.load_function(kwargs[key]))
            elif isinstance(field, Field):
                self.__setattr__(key, field.default)

    def serialize(self):
        serialized_self = {}
        if self.check_all_attr():
            for key, field in self.__class__.__dict__.items():
                if isinstance(field, Field):
                    if field.serialize:
                        serialized_self[key] = field.save_function(self.__getattribute__(key))
        return serialized_self

    def save(self):
        if self.check_all_attr():
            for key, field in self.__class__.__dict__.items():
                if isinstance(field, Field):
                    if not field.serialize:
                        field.save_function(self.__getattribute__(name=key))
        if self.id:
            self.database.update(self.__class__, self.serialize(), id=self.id)
        else:
            self.id = self.database.insert(self.__class__, self.serialize())

    def check_all_attr(self) -> bool:
        for key, field in self.__class__.__dict__.items():
            if isinstance(field, Field):
                field.check_field(value=self.__getattribute__(name=key))
        return True

    def __getattribute__(self, item):
        if item in self.__class__.__dict__.keys():
            if issubclass(self.__class__.__dict__[item], Field):
                field = self.__class__.__dict__[item]
                if not field.serialize and self.id is not None:
                    return field.update(
                        value=super(Model, self).__getattribute__(item),
                        id=self.id
                    )
        return super(Model, self).__getattribute__(item)

