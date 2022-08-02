from models import Field, db_init

class Model:

    instantiated_object = {}
    database = db_init("TinyDB", {'file': 'database.json'})

    @classmethod
    def get(cls, id):
        pass

    def __init__(self, **kwargs):
        if 'id' in kwargs.keys():
            self.id = kwargs['id']
        else:
            self.id = None
        for key, field in self.__class__.__dict__.items():
            if isinstance(field, Field) and key in kwargs.keys():
                self.__setattr__(key, field.load_function(kwargs[key]))


    def serialize(self):
        serialized_self = {}
        if self.check_all_attr():
            for key, field in self.__class__.__dict__.items():
                if isinstance(field, Field):
                    serialized_self[key] = field.save_function(self.__getattribute__(key))
        return serialized_self


    def save(self):
        if self.id:
            self.database.update(self.__class__, self.serialize(), id=self.id)
        else:
            self.id = self.database.insert(self.__class__, self.serialize())
            self.__class__.instantiated_object[self.id] = self

    def check_all_attr(self) -> bool:
        for key, field in self.__class__.__dict__.items():
            if isinstance(field, Field):
                if not self.__getattribute__(key):
                    if not field.blank:
                        raise ValueError(f"{key} can not be {None} !")
                elif type(self.__getattribute__(key)) != field.field_type:
                    raise TypeError(f"{key} must be a {field.field_type} type !")
        return True

    def __setattr__(self, key, value):
        if key in self.__class__.__dict__.keys():
            if isinstance(self.__class__.__dict__[key], Field):
                if type(value) == self.__class__.__dict__[key].field_type:
                    super(Model, self).__setattr__(key, value)
                else:
                    raise TypeError(f"{key} must be a {self.__class__.__dict__[key].field_type} type !")
            else:
                super(Model, self).__setattr__(key, value)
        else:
            super(Model, self).__setattr__(key, value)
