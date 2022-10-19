import Models
from Views.Main import ViewsInterface
from .date import DateController


class TournamentController:
    def new_tournament(self, view: ViewsInterface):
        field = {
            'name': 'Nom : ',
            'place': 'Lieu du tournoi : ',
            'date': 'Date du tournoi\n'
                    'Écrivez les dates sous la forme: JJ/MM/AAAA\n'
                    'Pour date_1 et date_2 écrivez : date_1,date_2\n'
                    'Pour date_1 au date_2 écrivez: date_1-date_2\n'
                    'Date(s) : ',
            'round_number': 'Nombre de tour (4 par défaut) : ',
            'description': 'Description du tournoi : ',
        }
        while True:
            tournament_dict = view.form(
                title="Création d'un nouveau tournoi !",
                fields=field
            )
            tournament_dict['date'] = DateController().str_list_of_date_to_list_of_date(dates_str=tournament_dict['date'])
            if tournament_dict['round_number'].isnumeric():
                tournament_dict['round_number'] = int(tournament_dict['round_number'])
            else:
                print(f'"{tournament_dict["round_number"]}" '
                      f'n\'est pas un nombre valide et sera remplacé par 4 (la valeur par defaut)')
                tournament_dict['round_number'] = 4

            data_validity = view.menu(
                items=[
                    'Modifier',
                    'Valider ces informations',
                    'Retour au menu principal (Toute les informations seront perdu)'
                ],
                header=f'\nNom : {tournament_dict["name"]}\n'
                       f'Lieu du tournoi : {tournament_dict["place"]}\n'
                       f'Le tournoi se deroule '
                       f'{DateController().list_of_date_to_str_list_of_date(tournament_dict["date"])}\n'
                       f'Nombre de tour {tournament_dict["round_number"]}\n'
                       f'Description :{tournament_dict["description"]}\n'
            )
            if data_validity == '2':
                break
            elif data_validity == '3':
                return None

    def list_tournament(self, view: ViewsInterface):
        all_tournaments = Models.Tournament.get_all(key=None, value=None)
        items_list = [
            *[f'{tournament.name} à {tournament.place}' for tournament in all_tournaments],
            'Retour au menu principal'
        ]
        while True:
            option_key = view.menu(title="Tournois", items=items_list)
            while not (option_key.isnumeric() and option_key != '0'):
                option_key = view.menu(header='Option invalide !', items=[])
            option_key = int(option_key)
            if option_key >= len(items_list):
                return None
            self.display_tournament(tournament=all_tournaments[option_key - 1])
            option_key = view.menu(items=['Continuer', 'Retour au menu principal'])
            while not (option_key.isnumeric() and option_key != '0'):
                option_key = view.menu(header='Option invalide !', items=[])
            option_key = int(option_key)
            if option_key >= 2:
                return None

    def display_tournament(self, tournament: Models.Tournament):
        pass
