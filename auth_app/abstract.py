from abc import ABC, abstractmethod

from aiogoogle.auth import UserCreds

from helpers.exceptions import BadUserCredsException


class AbstractAuth(ABC):
    """
    Defines the interface for interacting with an authentication provider.

    This abstract class outlines the methods that concrete authentication
    implementations (e.g., GoogleAuth) must implement to provide
    functionality like generating authorization URLs, initializing
    authentication flows, refreshing user credentials, and revoking
    user credentials.
    """

    @staticmethod
    @abstractmethod
    async def get_authorization_url(chat_id: str) -> str:
        """
        Generates an authorization URL for the specified chat ID.

        This method is responsible for generating the URL that the user
        needs to visit to initiate the authentication flow with the
        specific provider.
        :param chat_id: The chat ID of the user for whom the authorization URL
        is being generated.
        :return: A string containing the generated authorization URL.
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def init_auth(code: int | str | None, state: str) -> tuple[
        bool, str]:
        """
        Initializes the authentication flow based on the provided code and state.

        This method is responsible for completing the authentication flow
        using the authorization code and state received from the redirect
        after the user interacts with the authorization URL.

        :param code: The authorization code received from the redirect URL.
        :param state: The state parameter passed during the authorization flow.
        :return: A tuple containing a boolean indicating success and a string
            containing an error message if unsuccessful.
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def refresh_user_creds(
            chat_id: str) -> UserCreds | BadUserCredsException:
        """
        Refreshes the user credentials for the specified chat ID.

        This method is responsible for obtaining fresh user credentials
        (e.g., access and refresh tokens) for the specified chat ID.

        :param chat_id: The chat ID of the user for whom the credentials need
                to be refreshed.
        :return: An instance of `aiogoogle.auth.UserCreds` containing the
            refreshed user credentials upon success, or raises a
            `helpers.exceptions.BadUserCredsException` if an error occurs.
        """
        raise NotImplementedError

    @abstractmethod
    async def revoke_user_creds(self, chat_id: str, context) -> None:
        """
        Revokes the user credentials for the specified chat ID.

        This method is responsible for revoking the user's access using
        the specified context (e.g., authorization code, refresh token).

        :param chat_id: The chat ID of the user for whom the credentials need
                to be refreshed.
        :param context: The context (e.g., authorization code, refresh token)
                required to revoke the user's access.
        :return:
        """
        raise NotImplementedError
