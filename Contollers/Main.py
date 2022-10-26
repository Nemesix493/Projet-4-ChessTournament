from Views.Main import ViewsInterface
from .Player import PlayerController
from .Tournament import TournamentController
from .Checkers import check_menu


def main_controller(view: ViewsInterface) -> None:
    """
    Display the main menu, and manage the execution of submenus
    :param view: ViewsInterface
    :return: None
    """
    options = [
        ('Nouveau tournoi', TournamentController().new_tournament, {'view': view}),
        ('Nouveau joueur', PlayerController().new_player, {'view': view}),
        ('Liste des joueur', PlayerController().list_player, {'view': view}),
        ('Liste des tournois', TournamentController().list_tournament, {'view': view}),
        ('Quitter', quit, {})
    ]
    while True:
        option_index = check_menu(
            view=view,
            items=[option[0] for option in options],
            title='Menu principal',
            invalid_header='Option invalide veuiller rentrer une option valide !'
        )
        options[option_index][1](**options[option_index][2])
