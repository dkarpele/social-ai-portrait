from functools import lru_cache

from db import db_sql
from db.abstract import AbstractStorage
from project_settings.config import database_dsn


@lru_cache()
def get_db_service() -> AbstractStorage:
    url = f'postgresql+asyncpg://' \
          f'{database_dsn.user}:{database_dsn.password}@' \
          f'{database_dsn.host}:{database_dsn.port}/' \
          f'{database_dsn.dbname}'
    return db_sql.Postgres(url=url)
