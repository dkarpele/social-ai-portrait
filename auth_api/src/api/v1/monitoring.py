"""
This module provides functionalities for monitoring the health of the Redis
 cache used by the Auth API.

It defines a Prometheus Gauge metric named 'authapi_redis_healthcheck' to
track the number of errors encountered when interacting with Redis.

It also implements a health check endpoint `/authapi-redis-healthcheck` that
attempts to ping the Redis cache and returns a success message or raises a
custom exception (`helpers.exceptions.connection_error`) upon failure.
"""

import logging

from fastapi import APIRouter, status
from prometheus_client import Gauge
from redis.exceptions import ConnectionError

from auth_api.src.dependencies.redis import CacheDep
from helpers.exceptions import connection_error

router = APIRouter()
logger = logging.getLogger(__name__)

redis_errors = Gauge('authapi_redis_healthcheck',
                     'Number of errors interacting with Redis')


@router.get('/authapi-redis-healthcheck',
            response_model=None,
            status_code=status.HTTP_200_OK,
            include_in_schema=True,
            )
async def redis_healthcheck(cache: CacheDep):
    """
    Performs a health check on the Redis cache used by the Auth API.

    This function attempts to ping the Redis cache instance using the provided
    cache dependency object.

    :param cache: A dependency object providing access to the Redis cache.
    :return: A dictionary containing a success message upon successful
    connection.
    :raises helpers.exceptions.connection_error: If a connection error occurs while
        interacting with Redis.
    """
    try:
        logger.info('Trying to ping cache instance.')
        await cache.ping()
        logger.info(f'Connection to cache instance was successful.')
        return {'response':
                f'Connection to cache instance was successful.'}
    except ConnectionError:
        redis_errors.inc()
        logger.error(f'Connection to cache instance failed!', exc_info=True)
        raise connection_error
