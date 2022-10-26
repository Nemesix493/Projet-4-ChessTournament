import math
import os


from .ViewsInterface import ViewsInterface


class TerminalViews(ViewsInterface):
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
                f'+{title_width * "-"}+'
            )

    def menu(self, items: list, title: str = None, header: str = None, footer: str = None, submit: str = None) -> str:
        if title:
            self.title(title)
        if header:
            print(
                header,
            )
        key_length = len(str(len(items)))
        for i in range(len(items)):
            print(
                f'{i+1}{(key_length - len(str(i+1))) * " "} {items[i]}',
            )
        if footer:
            print(
                footer,
            )
        if submit:
            return input(submit)
        return input('Votre choix: ').replace(' ', '')

    def form(self, fields: dict, title: str = None, header: str = None, footer: str = None) -> dict:
        if title:
            self.title(title)
        if header:
            print(
                header,
            )
        result = {key: input(val) for key, val in fields.items()}
        if footer:
            print(
                footer,
            )
        return result
