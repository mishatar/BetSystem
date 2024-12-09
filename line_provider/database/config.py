import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class BaseSQLConfig:
    """
    :param port: Порт для подключения
    :param host: Адрес БД
    :param schema: Название схемы
    :param user: Пользователь БД
    :param password: Пароль от пользователя БД
    :param connector: Коннектор для подключения к БД
    """
    schema: str = os.getenv("POSTGRES_DB_NAME")
    host: str = os.getenv("POSTGRES_DB_HOST")
    port: int = os.getenv("POSTGRES_DB_HOST_PORT")
    user: str = os.getenv("POSTGRES_DB_USER")
    password: str = os.getenv("POSTGRES_DB_PASSWORD")
    connector: str = "postgresql+asyncpg"

db_config = BaseSQLConfig()
