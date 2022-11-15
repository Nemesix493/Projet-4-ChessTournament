from Contollers.Main import main_controller
from views.terminalviews import TerminalViews


def main():
    view = TerminalViews()
    main_controller(view=view)


if __name__ == '__main__':
    main()

