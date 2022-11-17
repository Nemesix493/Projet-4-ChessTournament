import abc


class ViewsInterface(abc.ABC):
    """
    Interface for views
    """

    @staticmethod
    @abc.abstractmethod
    def title(title: str) -> None:
        """
        Display Title
        :param title: str
        :return:
        """
        pass

    @abc.abstractmethod
    def menu(self, items: list, title: str = None, header: str = None, footer: str = None, submit: str = None) -> str:
        """
        Display a menu and return the selected option
        :param items: list
        :param title: str
        :param header: str
        :param footer: str
        :param submit: str
        :return: str
        """
        pass

    @abc.abstractmethod
    def form(self, fields: dict, title: str = None, header: str = None, footer: str = None) -> dict:
        """
        Display a form and return the user inputs in a dict
        :param fields: dict
        :param title: str
        :param header: str
        :param footer: str
        :return: dict
        """
        pass

    def header(self, text: str):
        pass
