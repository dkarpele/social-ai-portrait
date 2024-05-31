from abc import ABC, abstractmethod

from aiogoogle.auth import UserCreds

from db.abstract import AbstractCache
from settings.exceptions import BadUserCredsException


class AbstractAuth(ABC):
    @staticmethod
    @abstractmethod
    async def get_authorization_url(cache: AbstractCache, chat_id: int):
        pass

    @staticmethod
    @abstractmethod
    async def init_auth(cache: AbstractCache, code, state):
        pass

    @staticmethod
    @abstractmethod
    async def refresh_user_creds(cache: AbstractCache,
                                 chat_id) -> UserCreds | BadUserCredsException:
        pass
