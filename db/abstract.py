from abc import ABC, abstractmethod
from typing import Optional


class AbstractCache(ABC):
    """
    This abstract class defines the interface for a cache service.

    It provides methods for common cache operations like getting, putting,
    deleting data by ID or key, searching by pattern, and managing pipelines.

    Concrete cache implementations should inherit from this class and provide
    actual functionality for these methods.
    """
    @abstractmethod
    async def close(self) -> None:
        """
        Closes the connection to the cache service.

        This method should be called when the cache object is no longer needed.
        """
        ...

    @abstractmethod
    async def get_from_cache_by_id(self, _id: str) -> Optional:
        """
        Retrieves a single item from the cache by its unique identifier.

        :param _id: The unique identifier of the item to retrieve.

        :return: The cached data associated with the ID, or None if not found.
        """
        ...

    @abstractmethod
    async def put_to_cache_by_id(self, _id: str, entity, expire: int | None = None):
        """
        Stores an item in the cache with an optional expiration time.

        :param _id: The unique identifier for the item.
        :param entity: The data object to be cached.
        :param expire: The time in seconds for the item to stay in the cache, or None for no expiration.
        """
        ...

    @abstractmethod
    async def delete_from_cache_by_id(self, _id: str):
        """
        Deletes an item from the cache by its unique identifier.

        :param _id: The unique identifier of the item to delete.
        """
        ...

    @abstractmethod
    async def get_from_cache_by_key(self,
                                    key: str = None,
                                    sort: str = None) -> dict | None:
        """
        Retrieves data from the cache using a key and optional sorting criteria.

        :param key: The key to search for (optional).
        :param sort: Sorting criteria for retrieving multiple items (optional).

        :return: A dictionary containing cached data associated with the key,
         or None if not found.
        """
        ...

    @abstractmethod
    async def put_to_cache_by_key(self,
                                  key: str = None,
                                  entities: dict = None):
        """
        Stores data in the cache under a specific key.

        :param key: The key to associate with the data.
        :param entities: A dictionary containing data to be cached.
        """
        ...

    @abstractmethod
    async def get_keys_by_pattern(self,
                                  pattern: str = None, ):
        """
        Searches for cache keys matching a specific pattern.

        :param pattern: A wildcard pattern to match keys (optional).
        :return: An asynchronous iterator yielding matching cache keys.
        """
        ...

    @abstractmethod
    async def get_pipeline(self):
        """
        Creates a pipeline for executing multiple cache operations atomically.

        :return: An object representing the cache pipeline.
        """
        ...

    @abstractmethod
    async def ping(self):
        """
        Checks if the cache service is available.

        :return: True if the cache is reachable, False otherwise.
        """
        ...


class AbstractStorage(ABC):
    """
    This abstract class defines the interface for a relational database storage
     service.

    It provides methods for common database operations like creating and purging
    databases, adding, updating, and checking the existence of data entries.

    Concrete database storage implementations should inherit from this class and
    provide actual functionality for these methods.
    """

    @abstractmethod
    async def close(self) -> None:
        """
        Closes the connection to the database.

        This method should be called when the storage object is no longer needed.
        """
        ...

    @abstractmethod
    async def create_database(self):
        """
        Asynchronously creates the database (if applicable).

        This method might not be relevant for all database types. Concrete
        implementations should handle creating the database schema if necessary.
        """
        ...

    @abstractmethod
    async def purge_database(self):
        """
        Asynchronously purges (drops) the entire database (if applicable).

        This method should be used with caution as it removes all data from the
        database. Concrete implementations should handle this operation carefully.
        """
        ...

    @abstractmethod
    async def add(self, instance) -> None:
        """
        Asynchronously adds a new data instance to the database.

        :param instance: The data object to be added.
        """
        ...

    @abstractmethod
    async def update(self, entity, filter_column, filter_value: str,
                     values: dict) -> None:
        """
        Asynchronously updates an existing data instance in the database.

        :param entity: The data entity type (e.g., table name).
        :param filter_column: The column name used for filtering.
        :param filter_value: The value to match in the filter column.
        :param values: A dictionary containing key-value pairs for the updated
        data.
        """
        ...

    @abstractmethod
    async def exists(self, entity, filter_column, filter_value: str) -> bool:
        """
        Asynchronously checks for the existence of a data instance in the
        database.

        :param entity: The data entity type (e.g., table name).
        :param filter_column: The column name used for filtering.
        :param filter_value: The value to match in the filter column.
        :return: True if the data instance exists, False otherwise.
        """
        ...
