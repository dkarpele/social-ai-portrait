from functools import lru_cache

from db import db_redis
from db.abstract import AbstractCache
from project_settings.config import redis_settings


@lru_cache()
def get_cache_service() -> AbstractCache:
    return db_redis.Redis(host=redis_settings.redis_host,
                          port=redis_settings.redis_port,
                          ssl=False)
