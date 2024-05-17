import os

from aiogoogle.auth.creds import ClientCreds
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()


class MainConf(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env',
                                      env_file_encoding='utf-8',
                                      extra='allow')


class RedisSettings(MainConf):
    redis_host: str = Field(..., alias='REDIS_HOST')
    redis_port: int = Field(..., alias='REDIS_PORT')
    cache_expire_in_seconds: int = Field(..., alias='CACHE_EXPIRE_IN_SECONDS')


redis_settings = RedisSettings()


class GoogleCreds(MainConf):
    id: str = Field(..., alias='GOOGLE_CLIENT_ID')
    secret: str = Field(..., alias='GOOGLE_CLIENT_SECRET')
    scopes: str = Field(..., alias='GOOGLE_SCOPES')
    redirect_uri: str = Field(..., alias='GOOGLE_REDIRECT_URI')


google_creds = GoogleCreds()
google_client_creds = ClientCreds(client_id=google_creds.id,
                                  client_secret=google_creds.secret,
                                  scopes=[google_creds.scopes],
                                  redirect_uri=google_creds.redirect_uri)


class RateLimit(MainConf):
    request_limit_per_minute: int = Field(env="REQUEST_LIMIT_PER_MINUTE",
                                          default=20)
    is_rate_limit: bool = (os.getenv('IS_RATE_LIMIT', 'False') == 'True')


rl = RateLimit()


class BotSettings(MainConf):
    token: str = Field(..., alias='BOT_TOKEN')


bot_settings = BotSettings()
