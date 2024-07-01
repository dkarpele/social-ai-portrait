import os

from aiogoogle.auth.creds import ClientCreds
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class MainConf(BaseSettings):
    model_config = SettingsConfigDict(env_file=os.getenv('ENV_FILENAME'),
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
    project_id: str = Field(..., alias='GOOGLE_PROJECT_ID')
    gemini_api_key: str = Field(..., alias='GEMINI_API_KEY')


google_creds = GoogleCreds()
client_creds = ClientCreds(client_id=google_creds.id,
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
    url: str = Field(..., alias='BOT_URL')


bot_settings = BotSettings()


class SMTPLoggingSettings(MainConf):
    username: str = Field(..., alias='SMTP_USERNAME')
    password: str = Field(..., alias='SMTP_PASSWORD')
    mail_host: str = Field(..., alias='SMTP_MAIL_HOST')
    mail_port: str = Field(2525, alias='SMTP_PORT')
    sender: str = Field(..., alias='SMTP_SENDER')
    recipient: str = Field(..., alias='SMTP_RECIPIENT')


smtp_settings = SMTPLoggingSettings()
