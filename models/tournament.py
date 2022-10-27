import json
import datetime


from .model import Model
from .player import Player
from .round import Round


class Tournament(Model):
    field_dict = {
        'name': {
            'type': str,
        },
        'place': {
            'type': str
        },
        'date': {
            'type': list
        },
        'round_number': {
            'type': int,
            'default': 4
        },
        'description': {
            'type': str
        },
        'time_control': {
            'type': str
        },
        'rounds': {
            'type': list
        },
        'players': {
            'type': list
        }
    }

    def __init__(self, **kwargs):
        super(Tournament, self).__init__(**kwargs)
        if 'date' in kwargs.keys():
            dates = json.loads(kwargs['date'])
            self.date = [datetime.date(*date[:3]) for date in dates]
        if self.pk:
            players = json.loads(kwargs['players'])
            self.players = [Player.get(key='pk', value=player) for player in players]
            rounds = json.loads(kwargs['rounds'])
            self.players = [Round.get(key='pk', value=tournament_round) for tournament_round in rounds]

    def check_field_value(self, name, value) -> bool:
        """
        Check if the value of the property is correct
        :param name: str
        :param value:
        :return: bool
        """
        super(Tournament, self).check_field_value(name=name, value=value)
        if name == 'rounds':
            for tournament_round in value:
                if type(tournament_round) != Round:
                    raise TypeError(
                        f'All items in rounds property has to be {Round} but one is {type(tournament_round)}'
                    )
        if name == 'players':
            for player in value:
                if type(player) != Player:
                    raise TypeError(f'All items in players property has to be {Player} but one is {type(player)}')
        if name == 'date':
            for date in value:
                if type(date) != datetime.date:
                    raise TypeError(
                        f'All items in date property has to be {datetime.date} but one is {type(date)}'
                    )
        return True

    def serialize(self) -> dict:
        """
        Return the serialized object
        :return: dict
        """
        result = super(Tournament, self).serialize()
        result['date'] = json.dumps([date.timetuple() for date in result['date']])
        result['players'] = json.dumps([player.pk for player in result['players']])
        result['rounds'] = json.dumps([tournament_round.pk for tournament_round in result['rounds']])
        return result
