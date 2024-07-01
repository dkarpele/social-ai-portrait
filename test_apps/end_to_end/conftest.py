import asyncio

import pytest_asyncio

pytest_plugins = ("test_apps.end_to_end.fixtures.setup_redis",)


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
