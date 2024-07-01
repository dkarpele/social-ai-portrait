import pytest_asyncio
from test_apps.end_to_end.settings import settings
from redis.asyncio import Redis


redis_cli = Redis(host=settings.redis_host,
                  port=settings.redis_port)


@pytest_asyncio.fixture(scope='class')
async def redis_clear_data_before_after():
    await redis_cli.flushall()
    yield
    await redis_cli.flushall()


@pytest_asyncio.fixture(scope='class')
async def redis_clear_data_after():
    yield
    await redis_cli.flushall()


@pytest_asyncio.fixture(scope='class')
async def redis_clear_data_before():
    await redis_cli.flushall()
    yield
