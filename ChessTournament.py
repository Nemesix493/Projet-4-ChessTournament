from Contollers.Main import main_menu
from Views.Main import TerminalViews


def main():
    view = TerminalViews()
    main_menu(view=view)


if __name__ == '__main__':
    main()
