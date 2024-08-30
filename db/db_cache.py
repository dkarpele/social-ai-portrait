import logging
from typing import Optional

from redis.asyncio import Redis as AsyncRedis
from db.abstract import AbstractCache
from project_settings.config import redis_settings

logger = logging.getLogger(__name__)


class Redis(AbstractCache):
    def __init__(self, **params):
        self.session = AsyncRedis(**params)

    async def close(self):
        ...

    async def get_from_cache_by_id(self, _id: str) -> Optional:
        logger.info(f'Getting entity by id: `{_id}` from cache')
        data = await self.session.get(_id)
        if not data:
            return None

        return data

    async def put_to_cache_by_id(self, _id, entity, expire=None):
        logger.info(f'Putting entity by id: `{_id}` to cache')
        await self.session.set(_id,
                               entity,
                               expire)

    async def delete_from_cache_by_id(self, _id):
        logger.info(f'Deleting entity by id: `{_id}` from cache')
        await self.session.delete(_id)

    async def get_from_cache_by_key(self,
                                    key: str = None,
                                    sort: str = None) -> dict | None:
        logger.info(f'Getting entity by key: `{key}` from cache')
        data = await self.session.hgetall(key)
        if not data:
            return None

        return data

    async def put_to_cache_by_key(self,
                                  key: str = None,
                                  entities: dict = None):
        logger.info(f'Putting entity by key: `{key}` to cache')
        await self.session.hset(name=key,
                                mapping=entities)
        await self.session.expire(name=key,
                                  time=redis_settings.cache_expire_in_seconds)

    async def get_pipeline(self):
        return self.session.pipeline()

    async def get_keys_by_pattern(self,
                                  pattern: str = None,):
        logger.info(f'Getting entity by pattern: `{pattern}` from cache')
        data = self.session.scan_iter(pattern)
        return data

    async def ping(self):
        await self.session.ping()


redis: Redis | None = None


async def get_cache() -> Redis:
    return redis
