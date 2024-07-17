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
async def redis_healthcheck(cache: CacheDep, ):
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
