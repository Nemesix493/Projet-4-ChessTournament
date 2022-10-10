import datetime
import json

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
                super(Model, self).__setattr__(key, None)

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
                super(Model, self).__setattr__(name, value)
        else:
            super(Model, self).__setattr__(name, value)

    def serialize(self) -> dict:
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
        result = super(Player, self).serialize()
        result['birthdate'] = json.dumps(result['birthdate'].timetuple())
        return result

    def check_field_value(self, name, value) -> bool:
        super(Player, self).check_field_value(name=name, value=value)
        if name == 'rank':
            if value < 0:
                raise ValueError(f'rank property has to be positive but it is {value}')
        return True


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
        result = super(Tournament, self).serialize()
        result['date'] = json.dumps([date.timetuple() for date in result['date']])
        result['players'] = json.dumps([player.pk for player in result['players']])
        result['rounds'] = json.dumps([tournament_round.pk for tournament_round in result['rounds']])
        return result
