import math
import os
import sys


class ViewsInterface:

    def menu(self, items: list, title: str = None, header: str = None, footer: str = None) -> str:
        pass

    def form(self, fields: dict, title: str = None, header: str = None, footer: str = None) -> dict:
        pass

    def title(self, title: str) -> None:
        pass


class TerminalViews(ViewsInterface):
    def __init__(self, file=sys.stdout):
        self.file = file

    def title(self, title: str) -> None:
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
                f'+{title_width * "-"}+',
                file=self.file
            )

    def menu(self, items: list, title: str = None, header: str = None, footer: str = None, submit: str = None) -> str:
        if title:
            self.title(title)
        if header:
            print(
                header,
                file=self.file
            )
        key_length = len(str(len(items)))
        for i in range(len(items)):
            print(
                f'{i+1}{(key_length - len(str(i+1))) * " "} {items[i]}',
                file=self.file
            )
        if footer:
            print(
                footer,
                file=self.file
            )
        if submit:
            return input(submit)
        return input('Votre choix: ')

    def form(self, fields: dict, title: str = None, header: str = None, footer: str = None) -> dict:
        if title:
            self.title(title)
        if header:
            print(
                header,
                file=self.file
            )
        result = {key: input(val) for key, val in fields.items()}
        if footer:
            print(
                footer,
                file=self.file
            )
        return result
