import logging.config

from gunicorn import glogging
from pydantic import Field

from project_settings.config import MainConf
from project_settings.logger import LOGGING


class AuthSettings(MainConf):
    host: str = Field(..., alias='HOST')
    port: int = Field(..., alias='PORT')


auth_settings = AuthSettings()


class GunicornLogger(glogging.Logger):
    def setup(self, cfg):
        super().setup(cfg)
        logging.config.dictConfig(LOGGING)
