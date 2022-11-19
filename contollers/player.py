import datetime


from .checkers import check_menu, check_form
from .date import DateController
from views.viewsinterface import ViewsInterface
import models


class PlayerController:
    @staticmethod
    def normalize_name(name) -> str:
        """
        Capitalize name including composit name
        :param name: str
        :return: str
        """
        normed_list = [[word.capitalize() for word in words.split('-')]
                       for words in name.split(' ')]
        normed_name = ' '.join(['-'.join(words) for words in normed_list])
        return normed_name

    @staticmethod
    def check_birthdate(birthdate: str) -> bool:
        """
        Check the validity of birthdate
        :param birthdate: str
        :return: bool
        """
        date_controller = DateController()
        if date_controller.check_date_validity(date=birthdate):
            if date_controller.str_date_to_date(date=birthdate) <\
                    datetime.date.today():
                return True
        return False

    def new_player(self, view: ViewsInterface,
                   title: str | None = "Ajout d'un nouveau joueur")\
            -> None | models.Player:
        """
        Display a form do add a new player, control its validity and return it
        or None if the user cancel the procedure
        :param view: ViewsInterface
        :param title: str | None
        :return: None | models.Player
        """
        options = {
            'last_name': [
                'Nom: ',
                lambda last_name:
                last_name.replace(' ', '').replace('-', '').isalpha(),
                'n\'est pas un nom valide'
            ],
            'first_name': [
                'Prénom: ',
                lambda first_name:
                first_name.replace(' ', '').replace('-', '').isalpha(),
                'n\'est pas un prénom valide'
            ],
            'birthdate':
                [
                    'Date de naissance (JJ/MM/YYYY): ',
                    self.check_birthdate,
                    'n\'est pas une date de naissance valide'
                ],
            'gender': [
                'Genre (M/F): ',
                lambda gender: gender == 'F' or gender == 'M',
                'n\'est pas un genre valide'
            ],
            'rank': [
                'Rang: ',
                lambda rank: rank.isnumeric(),
                'n\'est pas une valeur de rang valide'
            ]
        }
        player_dict = check_form(
            view=view,
            title=title,
            fields=options
        )
        if player_dict is None:
            return None
        player = models.Player()
        player.last_name = self.normalize_name(player_dict['last_name'])
        player.first_name = self.normalize_name(player_dict['first_name'])
        player.birthdate = DateController().str_date_to_date(
            date=player_dict['birthdate']
        )
        player.gender = player_dict['gender']
        player.rank = int(player_dict['rank'])
        result = check_menu(
            view=view,
            items=[
                'Enregistrer le nouveau joueur',
                'Ne pas enregistrer'
            ]
        )
        if result == 0:
            player.save()
            return player
        elif result == 1:
            return None

    @staticmethod
    def list_player(view: ViewsInterface, players: list,
                    title: str | None = None,
                    order_property: str = 'first_name') -> None:
        """
        Display a list of players ordered by "order_property"
        :param view: ViewsInterface
        :param players: list
        :param order_property: str
        :param title: str
        :return: None
        """
        players.sort(key=lambda player: getattr(player, order_property))
        header = '\n'.join([
            f'{player.first_name} {player.last_name} : '
            f'{player.rank} pt' for player in players
        ])
        view.header(text=header)

    @staticmethod
    def choose_player(view: ViewsInterface, players: list,
                      title: str | None = None,
                      order_property: str = 'first_name')\
            -> None | models.Player:
        """
        Display a list of players ordered by "order_property" to choose it
        :param view: ViewsInterface
        :param players: list
        :param order_property: str
        :param title: str | None
        :return: None
        """
        players.sort(key=lambda player: getattr(player, order_property))
        option = check_menu(
            view=view,
            items=[
                *[
                    f'{player.first_name} {player.last_name} '
                    f': {player.rank} pt'
                    for player in players
                ],
                'Retour'
            ],
            title=title,
        )
        if option == len(players):
            return None
        else:
            return players[option]

    @staticmethod
    def edit_player_rank(view: ViewsInterface, players: list | None = None,
                         title: str | None =
                         'Mise a jour du rang d\'un joueur') -> None:
        """
        Choose a player to edit/update its rank
        :param players: list
        :param view: ViewsInterface
        :param title: str|None
        :return: None
        """
        if players is None:
            players = models.Player.get_all(key=None, value=None)
        items = [
            *[f'{player.first_name} {player.last_name}' for player in players],
            'Retour'
        ]
        option = check_menu(
            view=view,
            items=items,
            title=title,
            invalid_header='Choix invalide\n Veuillez réessayer !'
        )
        if option == len(items)-1:
            return None
        player_to_update = players[option]
        header = f'{player_to_update.firs_name} {player_to_update.last_name}\n'
        header += 'Né' if player_to_update.gender == 'M' else 'Née'
        header += f' le: {player_to_update.birthdate}\n'
        header += f'Rang actuel : {player_to_update.rank}'
        new_rank = check_form(
            view=view,
            fields={'rank': [
                'Nouveau rang :',
                lambda rank: rank.isnumeric(),
                'n\'est pas une valeur de rang valide'
            ]},
            header=header
        )
        if new_rank is None:
            return None
        save_option = check_menu(
            view=view,
            items=[
                'Enregistrer',
                'Ne pas enregistrer'
            ],
            header=f'Voulez vous enregistre ce nouveau rang '
                   f'({new_rank["rank"]})'
        )
        if save_option == 1:
            return None
        player_to_update.rank = int(new_rank['rank'])
        player_to_update.save()

    @staticmethod
    def get_all_players_without(pks: list) -> list[models.Player]:
        all_players = models.Player.get_all(
            key=None,
            value=None
        )
        result = []
        for player in all_players:
            if player.pk not in pks:
                result.append(player)
        return result

    @classmethod
    def player_report(cls, view: ViewsInterface) -> None:
        options = [
            ('Afficher la liste de joueurs par ordre de prenom', 'first_name'),
            ('Afficher la liste de joueurs par ordre de nom', 'last_name'),
            ('Afficher la liste de joueurs par ordre de rang', 'rank'),
            ('Retour', None)
        ]
        view.title(title='Liste des joueurs')
        while True:
            option_index = check_menu(
                view=view,
                items=[option[0] for option in options]
            )
            if option_index == 3:
                return None
            players = models.Player.get_all(key=None, value=None)
            cls.list_player(
                view=view,
                players=players,
                order_property=options[option_index][1]
            )
