class Model:

    field_dict = {}

    def __init__(self, **kwargs):
        self.saved = 'pk' in kwargs.keys()
        for key, value in self.__class__.field_dict.items():
            if key in kwargs.keys():
                self.__setattr__(name=key, value=kwargs[key])
            else:
                super(Model, self).__setattr__(name=key, value=None)

    def __setattr__(self, name, value):
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
                super(Model, self).__setattr__(name=name, value=value)
            elif value is None:
                if field_blank:
                    super(Model, self).__setattr__(name=name, value=value)
                elif field_default is not None:
                    super(Model, self).__setattr__(name=name, value=field_default)
                else:
                    raise ValueError(f'Value can not be None !')
            else:
                raise TypeError(f'{name} has to be a {field_type} and the value is a {type(value)} !')
        else:
            super(Model, self).__setattr__(name=name, value=value)

    def serialize(self) -> dict:
        pass

    def save(self) -> None:
        pass


class Round(Model):
    pass


class Player(Model):
    pass


class Tournament(Model):
    pass
