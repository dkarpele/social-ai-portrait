import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class MainConf(BaseSettings):
    model_config = SettingsConfigDict(env_file=os.getenv('ENV_FILENAME'),
                                      env_file_encoding='utf-8',
                                      extra='allow')


class Settings(MainConf):
    redis_host: str = Field(..., alias='REDIS_HOST')
    redis_port: int = Field(..., alias='REDIS_PORT')
    cache_expire_in_seconds: int = Field(..., alias='CACHE_EXPIRE_IN_SECONDS')
    auth_url: str = Field('http://127.0.0.1:8000/api/v1/oauth', alias='AUTH_URL')
    bot_url: str = Field(..., alias='BOT_URL')


settings = Settings()
