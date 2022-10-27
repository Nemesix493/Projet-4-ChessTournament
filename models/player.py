import json
import datetime


from .model import Model


class Player(Model):
    field_dict = {
        'last_name': {
            'type': str
        },
        'first_name': {
            'type': str
        },
        'birthdate': {
            'type': datetime.date
        },
        'gender': {
            'type': str
        },
        'rank': {
            'type': int
        }
    }

    def __init__(self, **kwargs):
        if 'birthdate' in kwargs.keys():
            kwargs['birthdate'] = datetime.date(*json.loads(kwargs['birthdate'])[:3])
        super(Player, self).__init__(**kwargs)

    def serialize(self) -> dict:
        """
        Return the serialized object
        :return: dict
        """
        result = super(Player, self).serialize()
        result['birthdate'] = json.dumps(result['birthdate'].timetuple())
        return result

    def check_field_value(self, name, value) -> bool:
        """
        Check if the value of the property is correct
        :param name: str
        :param value:
        :return: bool
        """
        super(Player, self).check_field_value(name=name, value=value)
        if name == 'rank':
            if value < 0:
                raise ValueError(f'rank property has to be positive but it is {value}')
        return True
