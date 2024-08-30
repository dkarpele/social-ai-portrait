from abc import ABC, abstractmethod
from typing import Optional


class AbstractCache(ABC):
    """
    Abstract class to work with db cache.
    :get_from_cache_by_id
    :get_from_cache_by_key
    :put_to_cache_by_id
    :put_to_cache_by_key
    """

    @abstractmethod
    async def close(self):
        ...

    @abstractmethod
    async def get_from_cache_by_id(self, _id: str) -> Optional:
        ...

    @abstractmethod
    async def put_to_cache_by_id(self, _id, entity, expire=None):
        ...

    @abstractmethod
    async def delete_from_cache_by_id(self, _id):
        ...

    @abstractmethod
    async def get_from_cache_by_key(self,
                                    key: str = None,
                                    sort: str = None) -> dict | None:
        ...

    @abstractmethod
    async def put_to_cache_by_key(self,
                                  key: str = None,
                                  entities: dict = None):
        ...

    @abstractmethod
    async def get_keys_by_pattern(self,
                                  pattern: str = None, ):
        """
        Get cache keys using pattern
        :param pattern: str
        :return: AsyncIterator with keys
        """
        ...

    @abstractmethod
    async def get_pipeline(self):
        """
        Creates pipeline
        :return:
        """
        ...

    @abstractmethod
    async def ping(self):
        """
        Ping cache instance
        :return:
        """
        ...


class AbstractStorage(ABC):
    """
    Abstract class to work with relational db.
    """

    @abstractmethod
    async def close(self):
        ...

    @abstractmethod
    async def create_database(self):
        ...

    @abstractmethod
    async def purge_database(self):
        ...

    @abstractmethod
    async def add(self, instance) -> None:
        ...

    @abstractmethod
    async def update(self, entity, filter_column, filter_value: str, values: dict) -> None:
        ...

    @abstractmethod
    async def exists(self, entity, filter_column, filter_value: str) -> bool:
        ...
