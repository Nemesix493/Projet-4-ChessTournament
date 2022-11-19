import math
import os


from .viewsinterface import ViewsInterface


class TerminalViews(ViewsInterface):
    """
    Class to display the app in a terminal
    """
    @staticmethod
    def title(title: str) -> None:
        """
        Display Title
        :param title: str
        :return:
        """
        title_width = 100
        try:
            title_width = math.floor(os.get_terminal_size().columns / 2)
        except OSError:
            title_width = 100
        finally:
            print(
                f'+{title_width * "-"}+\n'
                f'|{math.ceil((title_width - len(title)) / 2) * " "}'
                f'{title}'
                f'{math.floor((title_width - len(title)) / 2) * " "}|\n'
                f'+{title_width * "-"}+'
            )

    def menu(self, items: list, title: str = None, header: str = None,
             footer: str = None, submit: str = None) -> str:
        """
        Display a menu in terminal and return the selected option
        :param items: list
        :param title: str
        :param header: str
        :param footer: str
        :param submit: str
        :return: str
        """
        if title:
            self.title(title)
            print('')
        if header:
            self.header(text=header + '\n')
        key_length = len(str(len(items)))
        for i in range(len(items)):
            print(
                f'{i+1}{(key_length - len(str(i+1))) * " "} {items[i]}',
            )
        print('')
        if footer:
            print(
                footer + '\n',
            )
        if submit:
            return input(submit)
        return input('Votre choix: ').replace(' ', '')

    def form(self, fields: dict, title: str = None, header: str = None,
             footer: str = None) -> dict:
        """
        Display a form and return the user inputs in a dict
        :param fields: dict
        :param title: str
        :param header: str
        :param footer: str
        :return: dict
        """
        if title:
            self.title(title)
            print('')
        if header:
            self.header(text=header + '\n')
        result = {key: input(val) for key, val in fields.items()}
        print('')
        if footer:
            print(
                footer + '\n',
            )
        return result

    def header(self, text: str):
        print(text)
