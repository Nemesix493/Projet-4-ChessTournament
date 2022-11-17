from views.viewsinterface import ViewsInterface
from .player import PlayerController
from .tournament import TournamentController
from .checkers import check_menu


def main_controller(view: ViewsInterface) -> None:
    """
    Display the main menu, and manage the execution of submenus
    :param view: ViewsInterface
    :return: None
    """
    options = [
        (
            'Nouveau tournoi',
            TournamentController().new_tournament,
            {'view': view}
        ),
        (
            'Reprendre un tournoi',
            TournamentController().pick_up_tournament_again,
            {'view': view}
        ),
        (
            'Nouveau joueur',
            PlayerController().new_player,
            {'view': view}
        ),
        (
            'Editer le rang d\'un joueur',
            PlayerController.edit_player_rank,
            {'view': view, 'title': 'Editer le rang d\'un joueur'}
         ),
        (
            'Liste des joueurs',
            PlayerController().player_report,
            {'view': view}
        ),
        (
            'Rapport de tournois',
            TournamentController().tournament_report,
            {'view': view}
        ),
        (
            'Quitter', quit, {}
        )
    ]
    while True:
        option_index = check_menu(
            view=view,
            items=[option[0] for option in options],
            title='Menu principal'
        )
        options[option_index][1](**options[option_index][2])
