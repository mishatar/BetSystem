"""
Base Database connection module.
GET OUT OF HERE!
"""
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

__all__ = ['CConnection']

from database.config import BaseSQLConfig, db_config
from .db_driver import DbDriverABC


class CConnection(DbDriverABC):
    """
    Base Database connection class.
    """

    def __init__(self):
        connection_data = self._prepare_connection_data(config=db_config)
        self._engine = create_async_engine(
            connection_data,
            hide_parameters=False,
            poolclass=NullPool,
            future=True
        )
        self._session = async_sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
            class_=AsyncSession
        )

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self._session() as session:
            try:
                yield session
                await session.commit()
            except Exception as err:
                await session.rollback()
                raise err
            finally:
                await session.close()

    @staticmethod
    def _prepare_connection_data(config: BaseSQLConfig) -> str:
        """
        Base hidden prepare connection type.
        """

        return f"{config.connector}://{config.user}:{config.password}@{config.host}:{config.port}/{config.schema}"
