import json
import inspect
import sys


class Field:
    def __init__(self, field_type, blank=False, default=None, serialize: bool = True ):
        self.field_type = field_type
        self.blank = blank
        self.default = default
        self.serialize = serialize

    def save_function(self, value):
        return value

    def load_function(self, value):
        return value

    def check_field(self, value):
        return type(value) == self.field_type or (self.blank and value is None)

    def update(self, value, id):
        raise Exception('update function call but it mustn\'t be called')

    def save(self):
        pass


class StringField(Field):
    def __init__(self, blank=False, default=None):
        super(StringField, self).__init__(field_type=str, blank=blank, default=default)


class IntField(Field):
    def __init__(self, blank=False, default=None):
        super(IntField, self).__init__(field_type=int, blank=blank, default=default)


class FloatField(Field):
    def __init__(self, blank=False, default=None):
        super(FloatField, self).__init__(field_type=float, blank=blank, default=default)


class JsonField(Field):
    def __init__(self, blank=False, default=None, **kwargs):
        if 'field_type' in kwargs.keys():
            field_type = kwargs['field_type']
            self.custom_field_type = True
        else:
            field_type = str
            self.custom_field_type = False
        super(JsonField, self).__init__(field_type=field_type, blank=blank, default=default)

    def load_function(self, value):
        return json.load(value)

    def save_function(self, value):
        return json.dump(value)

    def check_field(self, value):
        if self.custom_field_type:
            return type(value) == self.field_type or (self.blank and value is None)
        return True


class RelationalField(Field):
    def init_relation(self, cls: type, name: str):
        pass


class DomesticKey(Field):
    def __init__(self, field_type, foreign_key_name):
        self.foreign_key_name = foreign_key_name
        super(DomesticKey, self).__init__(field_type=field_type, blank=True, default=None, serialize=False)

    def load_function(self, id):
        query = {
            self.foreign_key_name: id
        }
        return self.field_type.get_all(**query)

    def update(self, value):
        pass

    def save_function(self, value):
        pass

    def save(self):
        pass


class ForeignKey(RelationalField):
    def __init__(self, field_type, domestic_key_name: str = None, blank=False, default=None):
        super(ForeignKey, self).__init__(field_type=field_type, blank=blank, default=default)
        self.domestic_key_name = domestic_key_name

    def init_relation(self, cls: type, name: str):
        if type(self.domestic_key_name) == str:
            setattr(cls, self.domestic_key_name, DomesticKey(cls, foreign_key_name=name))
        else:
            setattr(cls, f'{cls.__name__.lower()}s', DomesticKey(cls, foreign_key_name=name))
            self.domestic_key_name = f'{cls.__name__.lower()}s'

    def load_function(self, value):
        return self.field_type.get(id=value)

    def save_function(self, value):
        if value.id:
            return value.id
        else:
            value.save()
            return value.id
