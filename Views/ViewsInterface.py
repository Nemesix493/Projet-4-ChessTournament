class ViewsInterface:

    def menu(self, items: list, title: str = None, header: str = None, footer: str = None, submit: str = None) -> str:
        pass

    def form(self, fields: dict, title: str = None, header: str = None, footer: str = None) -> dict:
        pass

    def title(self, title: str) -> None:
        pass

    def report(self, fields: dict, title: str = None, header: str = None, footer: str = None) -> None:
        pass
