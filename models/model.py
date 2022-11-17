import abc


from .database import load_database


class Model(abc.ABC):

    database = load_database()

    field_dict = {}

    @abc.abstractmethod
    def __init__(self, **kwargs):
        self.pk = None
        if 'pk' in kwargs.keys():
            self.pk = kwargs['pk']
        for key, value in self.__class__.field_dict.items():
            if key in kwargs.keys():
                self.__setattr__(name=key, value=kwargs[key])
            else:
                super(Model, self).__setattr__(key, None)

    @abc.abstractmethod
    def check_field_value(self, name, value) -> bool:
        """
        Check if the value of the property is correct
        :param name: str
        :param value:
        :return: bool
        """
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
                raise TypeError(
                    f'{name} has to be a {field_type} '
                    f'and the value is a {type(value)} !'
                )
        else:
            raise ValueError(f'{name} is not a field')

    def __setattr__(self, name, value):
        if name in self.__class__.field_dict.keys():
            if self.check_field_value(name=name, value=value):
                field = self.__class__.field_dict[name]
                if value is None and 'default' in field.keys():
                    value = field['default']
                super(Model, self).__setattr__(name, value)
        else:
            super(Model, self).__setattr__(name, value)

    @abc.abstractmethod
    def serialize(self) -> dict:
        """
        Return the serialized object
        :return: dict
        """
        result_dict = {}
        for key, val in self.__class__.field_dict.items():
            field_value = self.__getattribute__(key)
            self.__setattr__(name=key, value=field_value)
            result_dict[key] = self.__getattribute__(key)
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

    @classmethod
    def get(cls, key: str, value) -> 'Model':
        """
        Return the first object corresponding to the key value
        :param key: str
        :param value:
        :return: Model
        """
        return cls(
            **cls.database.get(
                cls=cls,
                key_name=key,
                value=value
            )
        )

    @classmethod
    def get_all(cls, key: str | None, value) -> list['Model']:
        """
        Return all the objects corresponding to key value
        :param key:
        :param value:
        :return:
        """
        doc_list = cls.database.get_all(
            cls=cls,
            key_name=key,
            value=value
        )
        return [cls(**document) for document in doc_list]
