from abc import abstractmethod
from typing import Dict, Type, AsyncGenerator
from database.config import BaseSQLConfig


class Singleton(type):
    _instances: Dict[Type, Dict[str, object]] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = {}
        key = str(args) + str(kwargs)
        if key not in cls._instances[cls]:
            cls._instances[cls][key] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls][key]


class DbDriverABC(metaclass=Singleton):
    @abstractmethod
    async def get_session(self) -> AsyncGenerator:
        """Not Implemented"""

    @staticmethod
    @abstractmethod
    def __prepare_connection_data(config: BaseSQLConfig):
        """Not Implemented"""

