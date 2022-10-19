from Views.Main import ViewsInterface
from .Player import PlayerController
from .Tournament import TournamentController


def main_menu(view: ViewsInterface):
    options = [
        ('Nouveau tournoi', TournamentController().new_tournament, {'view': view}),
        ('Nouveau joueur', PlayerController().new_player, {'view': view}),
        ('Liste des joueur', PlayerController().list_player, {'view': view}),
        ('Liste des tournois', TournamentController().list_tournament, {'view': view}),
        ('Quitter', quit, {})
    ]
    option_key = view.menu(title="Menu principal", items=[option[0] for option in options])
    while True:
        option_key = option_key.replace(' ', '')
        try:
            option_key = int(option_key) - 1
            if option_key in range(len(options)):
                options[option_key][1](**options[option_key][2])
                option_key = view.menu(title="Menu principal", items=[option[0] for option in options])
            else:
                raise ValueError()
        except ValueError:
            option_key = view.menu(
                header='Option invalide veuiller rentrer une option valide !',
                items=[option[0] for option in options]
            )
