from abc import ABC, abstractmethod

from aiogoogle.auth import UserCreds

from helpers.exceptions import BadUserCredsException


class AbstractAuth(ABC):
    @staticmethod
    @abstractmethod
    async def get_authorization_url(chat_id: str):
        pass

    @staticmethod
    @abstractmethod
    async def init_auth(code, state):
        pass

    @staticmethod
    @abstractmethod
    async def refresh_user_creds(chat_id) -> UserCreds | BadUserCredsException:
        pass

    @abstractmethod
    async def revoke_user_creds(self, chat_id, context) -> None:
        pass
