import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from auth_api.src.api.v1 import oauth
from auth_api.src.core.config import auth_settings
from settings.logger import LOGGING
from db import db_redis

from settings.config import redis_settings


logger = logging.getLogger('auth_api')


async def startup():
    logger.debug('startup debug')
    logger.info('startup info')
    db_redis.redis = db_redis.Redis(host=redis_settings.redis_host,
                                    port=redis_settings.redis_port,
                                    ssl=False)


async def shutdown():
    pass


@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup()
    yield
    await shutdown()


app = FastAPI(
    title="Auth API implements OAuth2.",
    description="Auth API implements OAuth2.",
    version="1.0.0",
    docs_url='/api/openapi-auth',
    openapi_url='/api/openapi-auth.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
    # dependencies=[Depends(rate_limit)]
)

app.include_router(oauth.router, prefix='/api/v1/oauth', tags=['oauth'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=auth_settings.host,
        port=auth_settings.port,
        log_config=LOGGING,
        log_level=logging.DEBUG
    )
