from functools import lru_cache
from typing import Annotated

from db.db_cache import Redis, get_cache
from db.abstract import AbstractCache
from fastapi import Depends


@lru_cache()
def get_cache_service(redis: Redis = Depends(get_cache)) -> AbstractCache:
    return redis


CacheDep = Annotated[AbstractCache, Depends(get_cache_service)]
