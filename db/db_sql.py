import os

from sqlalchemy import MetaData, select, update
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, \
    async_sessionmaker
from sqlalchemy.orm import declarative_base

from db.abstract import AbstractStorage

Base = declarative_base(metadata=MetaData(schema='content'))


class Postgres(AbstractStorage):
    """
    Concrete implementation of the AbstractStorage class for Postgresql. See
    docstrings for exact method in abstract class.
    """
    def __init__(self, url: str):
        echo = (os.getenv('ENGINE_ECHO', 'False') == 'True')
        self.engine = create_async_engine(url,
                                          echo=echo,
                                          future=True)

        self.async_session = async_sessionmaker(self.engine,
                                                class_=AsyncSession,
                                                expire_on_commit=False)

    async def close(self):
        ...

    async def create_database(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def purge_database(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    async def add(self, instance) -> None:
        async with self.async_session() as session:
            session.add(instance)
            await session.commit()
            await session.refresh(instance)

    async def exists(self, entity, filter_column, filter_value: str) -> bool:
        # filter_column = getattr(entity, column)
        async with self.async_session() as session:
            stm = select(entity.id).where(filter_column == filter_value)
            scalars = await session.scalars(stm)
            return bool(scalars.first())

    async def update(self, entity, filter_column, filter_value: str, values: dict) -> None:
        # filter_column = getattr(entity, column)
        async with self.async_session() as session:
            stm = update(entity). \
                  where(filter_column == filter_value). \
                  values(values)
            await session.execute(stm)
            await session.commit()


db_sql: Postgres | None = None


async def get_session() -> AsyncSession:
    async with db_sql.async_session() as session:
        return session
