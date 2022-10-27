import json


from .model import Model
from .player import Player


class Round(Model):
    field_dict = {
        'matches': {
            'type': list
        }
    }

    def __init__(self, **kwargs):
        super(Round, self).__init__(**kwargs)
        if self.pk:
            matches = json.loads(kwargs['matches'])
            self.matches = [
                {
                    'player_1': Player.get(key='pk', value=match['player_1']),
                    'player_2': Player.get(key='pk', value=match['player_2']),
                    'winner': Player.get(key='pk', value=match['winner'])
                }
                for match in matches
            ]

    def serialize(self) -> dict:
        """
        Return the serialized object
        :return: dict
        """
        result = super(Round, self).serialize()
        result['matches'] = json.dumps(
            [
                {
                    'player_1': match['player_1'].pk,
                    'player_2': match['player_2'].pk,
                    'winner': match['winner'].pk
                }
                for match in result['matches']
            ]
        )
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
                if type(match) == dict:
                    keys = ['player_1', 'player_2', 'winner']
                    if False not in [key in match.keys() for key in keys]:
                        if False in [type(match[key]) == Player for key in keys]:
                            raise TypeError(f'One item of the a dict in the list is not a {Player} but must be one !')
                    else:
                        raise ValueError(
                            f'Missing a key in a dict of the list all dict in the list must have {keys} keys'
                        )
                else:
                    raise TypeError(f'All item of the matches list must be a dict but one is a {type(match)}')
        return True
