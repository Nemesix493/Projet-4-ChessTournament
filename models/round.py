import datetime
import json


from .model import Model
from .player import Player


class Round(Model):
    field_dict = {
        'name': {
            'type': str
        },
        'start': {
            'type': datetime.datetime
        },
        'end': {
            'type': datetime.datetime
        },
        'matches': {
            'type': list
        }
    }

    def __init__(self, **kwargs):
        self_value_dict = {key: val for key, val in kwargs.items()}
        if 'pk' in self_value_dict.keys():
            matches = json.loads(self_value_dict['matches'])
            self_value_dict['matches'] = [
                (
                    [Player.get(key='pk', value=match[0][0]), match[0][1]],
                    [Player.get(key='pk', value=match[1][0]), match[1][1]]
                )
                for match in matches
            ]
            self_value_dict['start'] = datetime.datetime.fromtimestamp(self_value_dict['start'])
            self_value_dict['end'] = datetime.datetime.fromtimestamp(self_value_dict['end'])
        super(Round, self).__init__(**self_value_dict)

    def serialize(self) -> dict:
        """
        Return the serialized object
        :return: dict
        """
        result = super(Round, self).serialize()
        result['matches'] = json.dumps(
            [
                (
                    [match[0][0].pk, match[0][1]],
                    [match[1][0].pk, match[1][1]]
                )
                for match in result['matches']
            ]
        )
        result['start'] = result['start'].timestamp()
        result['end'] = result['end'].timestamp()
        return result

    def check_field_value(self, name, value) -> bool:
        """
        Check if the value of the property is correct
        :param name: str
        :param value:
        :return: bool
        """
        super(Round, self).check_field_value(name=name, value=value)
        if name == 'matches':
            for match in value:
                if type(match) == tuple:
                    for line in match:
                        if type(line[0]) != Player:
                            raise TypeError(f'The player must be a Player object but is a {type(line[0])}')
                        if type(line[1]) != int and type(line[1]) != float:
                            raise TypeError(f'The score must be a int or float but is a {type(line[1])}')
                else:
                    raise TypeError(f'All item of the matches list must be a tuple but one is a {type(match)}')
        return True
