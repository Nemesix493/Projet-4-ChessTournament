import json


class Field:
    def __init__(self, field_type, blank=False):
        self.field_type = field_type
        self.blank = blank

    def save_function(self, value):
        return value

    def load_function(self, value):
        return value

    def check_field(self, value):
        return type(value) == self.field_type


class StringField(Field):
    def __init__(self, blank=False):
        super(StringField, self).__init__(field_type=str, blank=blank)


class IntField(Field):
    def __init__(self, blank=False):
        super(IntField, self).__init__(field_type=int, blank=blank)


class FloatField(Field):
    def __init__(self, blank=False):
        super(FloatField, self).__init__(field_type=float, blank=blank)


class JsonField(Field):
    def __init__(self, blank=False, **kwargs):
        if 'field_type' in kwargs.keys():
            field_type = kwargs['field_type']
            self.custom_field_type = True
        else:
            field_type = str
            self.custom_field_type = False
        super(JsonField, self).__init__(field_type=field_type, blank=blank)

    def load_function(self, value):
        return json.load(value)

    def save_function(self, value):
        return json.dump(value)

    def check_field(self, value):
        if self.custom_field_type:
            return type(value) == self.field_type
        return True


class ModelField(Field):
    def __init__(self, field_type, blank=False):
        self.field_type = field_type
        self.blank = blank

    def load_function(self, value):
        return self.field_type.get(id=value)

    def save_function(self, value):
        if value.id:
            return value.id
        else:
            value.save()
            return value.id