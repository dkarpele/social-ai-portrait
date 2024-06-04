import logging.config

from gunicorn import glogging
from pydantic import Field

from settings.config import MainConf
from settings.logger import LOGGING


class AuthSettings(MainConf):
    host: str = Field(..., alias='HOST')
    port: int = Field(..., alias='PORT')


auth_settings = AuthSettings()


class GunicornLogger(glogging.Logger):
    def setup(self, cfg):
        super().setup(cfg)
        logging.config.dictConfig(LOGGING)
