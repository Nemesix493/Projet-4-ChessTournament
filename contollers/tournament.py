import datetime

import models
from views import ViewsInterface
from .date import DateController
from .checkers import check_menu, check_form
from .player import PlayerController
from .swisstournament import SwissTournament


class TournamentController:
    @staticmethod
    def tournament_to_str(tournament: models.Tournament) -> str:
        tournament_date = DateController.list_of_date_to_str_list_of_date(
            list_dates=tournament.date
        )
        return f'Nom : {tournament.name}\n' \
               f'Lieu du tournoi : {tournament.place}\n' \
               f'Le tournoi se déroule ' \
               f'{tournament_date}' \
               f'\nNombre de tours : {tournament.round_number}\n' \
               f'Description : {tournament.description}\n' \
               f'Contrôle du temps : {tournament.time_control}'

    @staticmethod
    def round_to_str(tournament_round: models.Round) -> str:
        return f'{tournament_round.name} du ' \
               f'{tournament_round.start.strftime("%d/%m/%Y, %H:%M:%S")} au ' \
               f'{tournament_round.end.strftime("%d/%m/%Y, %H:%M:%S")}'

    @staticmethod
    def match_to_str(match: tuple) -> str:
        resum = f'{match[0][0].first_name} {match[0][0].last_name}'
        if match[0][1] == 1:
            resum += ' <- victoire | défaite -> '
        elif match[0][1] == 0:
            resum += ' <- défaite | victoire -> '
        else:
            resum += ' | ex aequo | '
        resum += f'{match[1][0].first_name} {match[1][0].last_name}'
        return resum

    @staticmethod
    def check_tournament_date(dates: str) -> bool:
        dates_list = [[date for date in dates_summed.split('-')]
                      if len(dates_summed.split('-')) > 1
                      else dates_summed
                      for dates_summed in dates.split(',')]
        check_list = []
        for date in dates_list:
            if type(date) == list:
                if len(date) == 2 and False not in [
                    DateController().check_date_validity(sub_date)
                    for sub_date in date
                ]:
                    check_list.append(
                        DateController().str_date_to_date(date[0]) <
                        DateController().str_date_to_date(date[1])
                    )
                else:
                    check_list.append(False)
            else:
                check_list.append(DateController().check_date_validity(date))
        return False not in check_list

    @staticmethod
    def check_player_number(tournament: models.Tournament) -> bool:
        if tournament.players is not None:
            if len(tournament.players) % 2 == 0 and \
                    len(tournament.players) != 0:
                return True
        return False

    @staticmethod
    def is_finished(tournament: models.Tournament) -> bool:
        return len(tournament.rounds) == tournament.round_number

    @staticmethod
    def is_round_finished(tournament_round: models.Round) -> bool:
        for match in tournament_round.matches:
            if match[0][1] == 0 and match[1][1] == 0:
                return False
        return True

    @staticmethod
    def get_unsolved_match_index(tournament_round: models.Round):
        unsolved_match_index = []
        for match in range(len(tournament_round.matches)):
            if tournament_round.matches[match][0][1] == 0 and \
                    tournament_round.matches[match][1][1] == 0:
                unsolved_match_index.append(match)
        return unsolved_match_index

    def new_tournament(self, view: ViewsInterface) -> None:
        tournament_dict = self.init_tournament(view=view)
        if tournament_dict is None:
            return None
        tournament_dict['date'] = DateController().\
            str_list_of_date_to_list_of_date(
            dates_str=tournament_dict['date']
        )
        tournament_dict['round_number'] = int(tournament_dict['round_number'])
        tournament = models.Tournament()
        for key, val in tournament_dict.items():
            setattr(tournament, key, val)
        tournament.rounds = []
        self.add_tournament_players(view=view, tournament=tournament)
        self.play_tournament(
            view=view,
            tournament=tournament
        )
        tournament.save()

    @staticmethod
    def add_existing_players(view: ViewsInterface,
                             tournament: models.Tournament) -> None:
        player_controller = PlayerController()
        while True:
            new_player = player_controller.choose_player(
                view=view,
                players=player_controller.get_all_players_without(
                    pks=[player.pk for player in tournament.players]
                )
            )
            if new_player is not None:
                tournament.players.append(new_player)
            else:
                return None

    @staticmethod
    def add_new_players(view: ViewsInterface,
                        tournament: models.Tournament) -> None:
        player_controller = PlayerController()
        while True:
            new_player = player_controller.new_player(
                view=view,
                title=None
            )
            if new_player is None:
                return None
            tournament.players.append(new_player)
            option = check_menu(
                view=view,
                items=[
                    'Créer un nouveau joueur',
                    'Retour'
                ],
            )
            if option == 1:
                return None

    def add_tournament_players(self, view: ViewsInterface,
                               tournament: models.Tournament) -> None:
        tournament.players = []
        options = [
            (
                'Ajouter des joueurs existants',
                self.add_existing_players,
                {'view': view, 'tournament': tournament}
            ),
            (
                'Ajouter de nouveau joueurs',
                self.add_new_players,
                {'view': view, 'tournament': tournament}
            ),
            ['Valider ces joueurs']
        ]
        view.title(title='Ajout des joueurs')
        while True:
            PlayerController.list_player(
                view=view,
                players=tournament.players,
                order_property='rank'
            )
            option_index = check_menu(
                view=view,
                items=[option[0] for option in options]
                if self.check_player_number(tournament=tournament)
                else [option[0] for option in options[:-1]]
            )
            if option_index == 2:
                return None
            options[option_index][1](**options[option_index][2])

    def init_tournament(self, view: ViewsInterface) -> None | dict:
        fields = {
            'name': (
                'Nom : ',
                lambda name: True,
                'n\'est pas un nom valide'
            ),
            'place': (
                'Lieu du tournoi : ',
                lambda place:
                place.replace(' ', '').replace('\'', '').isalpha(),
                'n\'est pas valide'
            ),
            'date': (
                'Date du tournoi\n'
                'Écrivez les dates sous la forme: JJ/MM/AAAA\n'
                'Pour date_1 et date_2 écrivez : date_1,date_2\n'
                'Pour date_1 au date_2 écrivez: date_1-date_2\n'
                'Date(s) : ',
                self.check_tournament_date,
                'l\'une des dates n\'est pas valide ou la syntaxe est '
                'incorecte'
            ),
            'round_number': (
                'Nombre de tours (4 par défaut) : ',
                lambda round_number: int(round_number) > 0
                if round_number.isnumeric() else round_number == '',
                'n\'est pas valide'
            ),
            'description': (
                'Description du tournoi : ',
                lambda description: True,
                ''
            )
        }
        tournament_dict = check_form(
            view=view,
            fields=fields,
            title="Création d'un nouveau tournoi !"
        )
        if tournament_dict is None:
            return None
        time_controls = ['Bullet', 'Blitz', 'Coup rapide']
        time_control = check_menu(
            view=view,
            items=time_controls,
            header='Quel est le contrôle du temps ?'
        )
        tournament_dict['time_control'] = time_controls[time_control]
        while True:
            if tournament_dict['round_number'] == '':
                tournament_dict['round_number'] = 4
            data_validity = check_menu(
                view=view,
                items=[
                    'Modifier',
                    'Valider ces informations',
                    'Retour au menu principal '
                    '(Toutes les informations seront perdues)'
                ],
                header=f'\nNom : {tournament_dict["name"]}\n'
                       f'Lieu du tournoi : {tournament_dict["place"]}\n'
                       f'Le tournoi se déroule : {tournament_dict["date"]}\n'
                       f'Nombre de tours : {tournament_dict["round_number"]}\n'
                       f'Description : {tournament_dict["description"]}\n'
                       f'Contrôle du temps : {tournament_dict["time_control"]}'
                       f'\n'
            )
            if data_validity == 1:
                return tournament_dict
            elif data_validity == 2:
                return None
            fields_name = [
                *[
                    (key, val[0][:-3]) if key != 'date' else (key, 'Date(s)')
                    for key, val in fields.items()
                ],
                ('time_control', 'Contrôle du temps')
            ]
            modify_field = check_menu(
                view=view,
                items=[
                    *[field[1] for field in fields_name],
                    'Ne rien modifier'
                ],
                header='Quel champ voulez-vous modifier ?'
            )
            if modify_field != len(fields_name):
                if fields_name[modify_field][0] != 'time_control':
                    new_field = check_form(
                        view=view,
                        fields={
                            fields_name[modify_field][0]:
                                fields[fields_name[modify_field][0]]
                        }
                    )
                    if new_field is not None:
                        tournament_dict[fields_name[modify_field][0]] = \
                            new_field[fields_name[modify_field][0]]
                else:
                    time_control = check_menu(
                        view=view,
                        items=time_controls,
                        header='Quel est le contrôle du temps ?'
                    )
                    tournament_dict['time_control'] = \
                        time_controls[time_control]

    def pick_up_tournament_again(self, view: ViewsInterface):
        all_tournament = models.Tournament.get_all(
            key=None,
            value=None
        )
        unfinished_tournament = []
        for tournament in all_tournament:
            if not self.is_finished(tournament=tournament):
                unfinished_tournament.append(tournament)
        tournament = self.list_tournament(
            view=view,
            tournaments=unfinished_tournament,
            title='Reprendre un tournoi'
        )
        if tournament is None:
            return None
        round_resum = '\n'.join(
            [self.round_to_str(tournament_round=tournament_round) + '\n' +
             '\n'.join([
                 f'    {self.match_to_str(match)}'
                 for match in tournament_round.matches
             ])
             for tournament_round in tournament.rounds]
        )

        view.header(
            text=f'\n Résumé du tournoi \n'
                 f'{self.tournament_to_str(tournament=tournament)}\n'
                 f'{round_resum}\n'
        )
        self.play_tournament(
            view=view,
            tournament=tournament
        )

    @staticmethod
    def list_tournament(view: ViewsInterface, tournaments: list,
                        title: str | None = 'Liste des tournois',
                        header: str | None = None) -> None | models.Tournament:
        """

        :param view: ViewsInterface
        :param tournaments: list(models.Tournament)
        :param title: str
        :param header: str
        :return: None | models.Tournament
        """
        items_list = [
            *[
                f'{tournament.name} à {tournament.place}'
                for tournament in tournaments
            ],
            'Retour'
        ]
        items_list_index = check_menu(
            view=view,
            items=items_list,
            title=title,
            header=header
        )
        if items_list_index == len(tournaments):
            return None
        return tournaments[items_list_index]

    @classmethod
    def play_tournament(cls, view: ViewsInterface,
                        tournament: models.Tournament):
        options = [
            'Jouer le prochain tour',
            'Modifier le rang d\'un joueur',
            'Reprendre le tournoi plus tard'
        ]
        while len(tournament.rounds) < tournament.round_number:
            option = check_menu(
                view=view,
                items=options,
            )
            if option == 2:
                return None
            elif option == 1:
                PlayerController().edit_player_rank(
                    view=view,
                    players=tournament.players,
                    title=None
                )
            else:
                cls.play_round(
                    view=view,
                    tournament=tournament
                )
                tournament.save()

    @classmethod
    def play_round(cls, view: ViewsInterface,
                   tournament: models.Tournament) -> None:
        round_dict = check_form(
            view=view,
            fields={
                'name': (
                    'Nom du tour :',
                    lambda name: True,
                    ''
                )
            }
        )
        if round_dict is None:
            return None
        tournament_round = SwissTournament.select_peer(tournament=tournament)
        tournament_round.name = round_dict['name']
        tournament_round.start = datetime.datetime.now()
        cls.match_result(
            view=view,
            tournament_round=tournament_round
        )
        tournament_round.end = datetime.datetime.now()
        tournament.rounds.append(tournament_round)
        tournament_round.save()

    @classmethod
    def match_result(cls, view: ViewsInterface,
                     tournament_round: models.Round):
        while not cls.is_round_finished(tournament_round=tournament_round):
            unsolved_match_index = cls.get_unsolved_match_index(
                tournament_round=tournament_round
            )
            options = [
                f'{tournament_round.matches[index][0][0].first_name} '
                f'{tournament_round.matches[index][0][0].last_name}'
                f' contre '
                f'{tournament_round.matches[index][1][0].first_name} '
                f'{tournament_round.matches[index][1][0].last_name}'
                for index in unsolved_match_index
            ]
            solved_match = []
            for index in range(len(tournament_round.matches)):
                if index not in unsolved_match_index:
                    resum = \
                        f'{tournament_round.matches[index][0][0].first_name} '\
                        f'{tournament_round.matches[index][0][0].last_name}'
                    if tournament_round.matches[index][0][1] == 1:
                        resum += ' <- victoire | défaite -> '
                    elif tournament_round.matches[index][0][1] == 0:
                        resum += ' <- défaite | victoire -> '
                    else:
                        resum += ' ex aequo '
                    resum += \
                        f'{tournament_round.matches[index][1][0].first_name} '\
                        f'{tournament_round.matches[index][1][0].last_name}'
                    solved_match.append(resum)
            header = '\n'.join(solved_match)
            match = check_menu(
                view=view,
                items=options,
                header=header
            )
            player_one_name = getattr(
                tournament_round.matches[unsolved_match_index[match]][0][0],
                'first_name'
            )
            player_one_name += ' '
            player_one_name += getattr(
                tournament_round.matches[unsolved_match_index[match]][0][0],
                'last_name'
            )
            player_two_name = getattr(
                tournament_round.matches[unsolved_match_index[match]][1][0],
                'first_name'
            )
            player_two_name += ' '
            player_two_name += getattr(
                tournament_round.matches[unsolved_match_index[match]][1][0],
                'last_name'
            )
            match_result = check_menu(
                view=view,
                items=[
                    'ex aequo',
                    f'victoire de {player_one_name}',
                    f'victoire de {player_two_name}'
                ],
                submit='Quel est le résultat du match : '
            )
            if match_result == 0:
                tournament_round.matches[unsolved_match_index[match]][0][1] = \
                    0.5
                tournament_round.matches[unsolved_match_index[match]][1][1] = \
                    0.5
            elif match_result == 1:
                tournament_round.matches[unsolved_match_index[match]][0][1] = 1
                tournament_round.matches[unsolved_match_index[match]][1][1] = 0
            else:
                tournament_round.matches[unsolved_match_index[match]][0][1] = 0
                tournament_round.matches[unsolved_match_index[match]][1][1] = 1

    @classmethod
    def tournament_report(cls, view: ViewsInterface):
        view.title(title='Rapport de tournois')
        all_tournament = models.Tournament.get_all(
            key=None,
            value=None
        )
        while True:
            tournament = cls.list_tournament(
                view=view,
                tournaments=all_tournament,
                title=None
            )
            if tournament is None:
                return None
            cls.display_tournament(view=view, tournament=tournament)

    @classmethod
    def display_tournament(cls, view: ViewsInterface,
                           tournament: models.Tournament):
        while True:
            option = check_menu(
                    view=view,
                    items=[
                        'Afficher les joueurs du '
                        'tournoi par ordre alphabétique',
                        'Afficher les joueurs du tournoi par ordre de rang',
                        'Afficher les tours du tournoi',
                        'Retour'
                    ],
                    header=f'\n{cls.tournament_to_str(tournament=tournament)}'
                           f'\n'
            )
            if option == 3:
                return None
            elif option == 0:
                PlayerController().list_player(
                    view=view,
                    players=tournament.players,
                    title=None
                )
            elif option == 1:
                PlayerController().list_player(
                    view=view,
                    players=tournament.players,
                    order_property='rank',
                    title=None
                )
            else:
                cls.display_tournament_rounds(
                    view=view,
                    tournament=tournament
                )

    @classmethod
    def display_tournament_rounds(cls, view: ViewsInterface,
                                  tournament: models.Tournament):
        while True:
            option = check_menu(
                view=view,
                items=[
                    *[
                        cls.round_to_str(tournament_round=tournament_round)
                        for tournament_round in tournament.rounds
                    ],
                    'Retour'
                ],
                header='Selectionnez un tour pour consulter '
                       'le details des matchs'
            )
            if option == len(tournament.rounds):
                return None
            cls.display_tournament_match(
                view=view,
                tournament_round=tournament.rounds[option]
            )

    @classmethod
    def display_tournament_match(cls, view: ViewsInterface,
                                 tournament_round: models.Round):
        view.menu(
            items=[],
            header='\n'.join([
                cls.match_to_str(match=match)
                for match in tournament_round.matches
            ]),
            submit='Retour'
        )
