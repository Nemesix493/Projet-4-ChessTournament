import datetime

from Views.Main import ViewsInterface
import Models


class PlayerController:
    @staticmethod
    def normalize_name(name) -> str:
        if not name.replace(' ', '').replace('-', '').isalpha():
            raise ValueError('contient des caractères spéciaux autre que "-" ou des chiffres !')
        normed_list = [[word.capitalize() for word in words.split('-')]
                       for words in name.split(' ')]
        normed_name = ' '.join(['-'.join(words) for words in normed_list])
        return normed_name

    def new_player(self, view: ViewsInterface) -> None | Models.Player:
        options = {
            'last_name': 'Nom: ',
            'first_name': 'Prénom: ',
            'birthdate': 'Date de naissance (JJ/MM/YYYY): ',
            'gender': 'Genre (M/F): ',
            'rank': 'Rang: '
        }
        player_dict = view.form(
            title="Ajout d'un nouveau joueur",
            fields=options
        )
        while True:
            player = Models.Player()
            no_error = True
            error = None
            while True:
                try:
                    player_dict['last_name'] = self.normalize_name(player_dict['last_name'])
                    break
                except ValueError as e:
                    player_dict['last_name'] = view.form(
                        header=f'Nom invalide !\n{player_dict["last_name"]} {e}',
                        fields={'last_name': 'Nom: '}
                    )
            while True:
                try:
                    player_dict['first_name'] = self.normalize_name(player_dict['first_name'])
                    break
                except ValueError as e:
                    player_dict['first_name'] = view.form(
                        header=f'Prénom invalide !\n"{player_dict["first_name"]}" {e}',
                        fields={'first_name': 'Prénom: '}
                    )
            if no_error:
                try:
                    split_date = [int(val) for val in player_dict['birthdate'].split('/')]
                    player.birthdate = datetime.date(
                        year=split_date[2],
                        month=split_date[1],
                        day=split_date[0]
                    )
                    if not player.birthdate <= datetime.date.today():
                        raise ValueError()
                except ValueError:
                    no_error = False
                    error = f'"{options["birthdate"]} {player_dict["birthdate"]}" est invalide !'
            player_dict['gender'] = player_dict['gender'].replace(' ', '')
            if no_error and (player_dict['gender'] == 'M' or player_dict['gender'] == 'F'):
                player.gender = player_dict['gender']
            else:
                no_error = False
                error = f'"{options["gender"]} {player_dict["gender"]}" est invalide !'
            if no_error:
                try:
                    player.rank = int(player_dict['rank'])
                except ValueError:
                    no_error = False
                    error = f'"{options["rank"]} {player_dict["rank"]}" est invalide !'
            if no_error:
                break
            else:
                player_dict = view.form(
                    header=error,
                    fields=options
                )
        while True:
            result = view.menu(
                header='',
                items=[
                    'Enregistrer le nouveau joueur',
                    'Ne pas enregistrer'
                ]
            )
            if result.replace(' ', '') == '1':
                player.save()
                return player
            elif result.replace(' ', '') == '2':
                return None

    def list_player(self, view: ViewsInterface):
        all_player = Models.Player.get_all(key=None, value=None)
        header = f'Choisissez un joueur pour avoir plus d\'information'
        items_list = [
            *[f'{player.first_name} {player.last_name}' for player in all_player],
            'Retour au menu principal'
        ]
        option_key = view.menu(
            items=items_list,
            header=header,
            title='Liste des Joueurs'
        )
        while True:
            while not (option_key.isnumeric() and option_key != '0'):
                option_key = view.menu(header='Option invalide !', items=[])
            option_key = int(option_key)
            if option_key >= len(items_list):
                return None
            self.display_player(player=all_player[option_key - 1], view=view)
            option_key = view.menu(items=['Continuer', 'Retour au menu principal'])
            while not (option_key.isnumeric() and option_key != '0'):
                option_key = view.menu(header='Option invalide !', items=[])
            option_key = int(option_key)
            if option_key >= 2:
                return None

    def display_player(self, player: Models.Player, view: ViewsInterface):
        fields = {
            'Nom ': player.last_name,
            'Prénom ': player.first_name,
            'Date de naissance ': player.birthdate.strftime("%d/%m/%Y"),
            'Genre ': player.gender,
            'Rang ': player.rank
        }
        view.report(fields=fields, title=player.first_name)
        option_key = view.menu(
            items=[
                'Retour a la liste des joueur',
                'Modifier le joueur'
            ]
        )
        while True:
            if option_key.replace(' ', '') == '2':
                self.edit_player(view=view)
                return None
            elif option_key.replace(' ', '') == '1':
                return None
            else:
                option_key = view.menu(
                    items=[
                        'Retour a la liste des joueur',
                        'Modifier le joueur'
                    ],
                    header='Option invalide !'
                )

    def edit_player(self, player: Models.Player, view: ViewsInterface):
        pass
