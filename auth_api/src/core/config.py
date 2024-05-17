from pydantic import Field

from settings.config import MainConf


class AuthSettings(MainConf):
    host: str = Field(..., alias='HOST')
    port: int = Field(..., alias='PORT')


auth_settings = AuthSettings()

