from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_sql import get_session


@lru_cache()
def get_db_service(db: AsyncSession = Depends(get_session)) -> AsyncSession:
    return db


DbDep = Annotated[AsyncSession, Depends(get_db_service)]
