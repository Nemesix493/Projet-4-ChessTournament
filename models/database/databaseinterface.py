import abc


class DatabaseInterface(abc.ABC):
    @abc.abstractmethod
    def insert(self, cls: type, serialized_obj: dict) -> int:
        """
        Insert object in db and return its id/primary_key
        :param cls: type
        :param serialized_obj: dict
        :return: int
        """
        pass

    @abc.abstractmethod
    def update(self, cls: type, serialized_obj: dict, pk: int) -> None:
        """
        Update object in db
        :param cls: type
        :param serialized_obj: dict
        :param pk: int
        :return: None
        """
        pass

    @abc.abstractmethod
    def get(self, cls: type, key_name: str, value) -> dict | None:
        """
        Return the first serialized object filter by key_name = value
        :param cls: type
        :param key_name: str
        :param value:
        :return: dict | None
        """
        pass

    @abc.abstractmethod
    def get_all(self, cls: type, key_name: str | None, value) -> list[dict]:
        """
        Return all the serialized object filter by key_name = value
        :param cls: type
        :param key_name: str
        :param value:
        :return: list[dict]
        """
        pass

    @abc.abstractmethod
    def remove(self, cls: type, pk: int) -> None:
        """
        Remove the object corresponding to this id
        :param cls: type
        :param pk: int
        :return: None
        """
        pass
