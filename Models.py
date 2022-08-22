from database import TinyDBDataBase


class Model:

    database = TinyDBDataBase(file='db.json')

    field_dict = {}

    def __init__(self, **kwargs):
        self.pk = None
        if 'pk' in kwargs.keys():
            self.pk = kwargs['pk']
        for key, value in self.__class__.field_dict.items():
            if key in kwargs.keys():
                self.__setattr__(name=key, value=kwargs[key])
            else:
                super(Model, self).__setattr__(name=key, value=None)

    def check_field_value(self, name, value) -> bool:
        if name in self.__class__.field_dict.keys():
            field = self.__class__.field_dict[name]
            field_type = field['type']
            field_blank = False
            if 'blank' in field.keys():
                field_blank = field['blank']
            field_default = None
            if 'default' in field.keys():
                field_default = field['default']
            if field_type == type(value):
                return True
            elif value is None:
                if field_blank:
                    return True
                elif field_default is not None:
                    return True
                else:
                    raise ValueError(f'Value can not be None !')
            else:
                raise TypeError(f'{name} has to be a {field_type} and the value is a {type(value)} !')
        else:
            raise ValueError(f'{name} is not a field')

    def __setattr__(self, name, value):
        if name in self.__class__.field_dict.keys():
            if self.check_field_value(name=name, value=value):
                field = self.__class__.field_dict[name]
                if value is None and 'default' in field.keys():
                    value = field['default']
                super(Model, self).__setattr__(name=name, value=value)
        else:
            super(Model, self).__setattr__(name=name, value=value)

    def serialize(self) -> dict:
        result_dict = {}
        for key, val in self.__class__.field_dict.items():
            field_value = self.__getattribute__(name=key)
            self.__setattr__(name=key, value=field_value)
            result_dict[key] = self.__getattribute__(name=key)
        return result_dict

    def save(self) -> None:
        if self.pk:
            self.__class__.database.update(
                cls=self.__class__,
                serialized_obj=self.serialize(),
                pk=self.pk
            )
        else:
            self.pk = self.__class__.database.insert(
                cls=self.__class__,
                serialized_obj=self.serialize()
            )

    def remove(self) -> None:
        if self.pk:
            self.__class__.database.remove(
                cls=self.__class__,
                pk=self.pk
            )
        del self

    @classmethod
    def get(cls, key: str, value) -> 'Model':
        return cls(
            **cls.database.get(
                cls=cls,
                key_name=key,
                value=value
            )
        )

    @classmethod
    def get_all(cls, key: str, value) -> list['Model']:
        doc_list = cls.database.get_all(
            cls=cls,
            key_name=key,
            value=value
        )
        return [cls(**document) for document in doc_list]


class Round(Model):
    pass


class Player(Model):
    pass


class Tournament(Model):
    pass
