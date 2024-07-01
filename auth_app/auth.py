import json
import logging

from aiogoogle import AuthError, HTTPError
from aiogoogle.auth import UserCreds, Oauth2Manager
from aiogoogle.auth.utils import create_secret
from aiohttp.web_response import Response

from auth_app.abstract import AbstractAuth
from auth_app.dependencies.redis import get_cache_service
from db.abstract import AbstractCache
from helpers.encryption import verify_message, get_public_key, get_signature
from helpers.exceptions import (BadUserCredsException,
                                UserAlreadyLoggedInException)
from helpers.utils import generate_youtube_login_message
from project_settings.config import client_creds

logger = logging.getLogger(__name__)
cache: AbstractCache = get_cache_service()


async def create_signature(chat_id: str):
    logger.info('Creating authorization signature.')
    signature_content: bytes = \
        str(chat_id).encode('utf-8') + \
        ".".encode('utf-8') + \
        create_secret().encode('utf-8')
    await cache.put_to_cache_by_id(f'signature.{chat_id}',
                                   get_signature(signature_content),
                                   3600)
    return signature_content


class GoogleAuth(AbstractAuth):
    @staticmethod
    async def get_authorization_url(chat_id: str) -> str | Response:
        logger.info('Creating authorization url')
        signature_content = await create_signature(chat_id)

        if Oauth2Manager().is_ready(client_creds):
            return Oauth2Manager().authorization_url(
                client_creds=client_creds,
                state=signature_content.decode(),
                access_type="offline",
                include_granted_scopes=True,
                prompt="select_account",
            )
        else:
            error_message = "Client doesn't have enough info for Oauth2"
            logger.warning(error_message)
            return Response(text=error_message,
                            status=500)

    @staticmethod
    async def verify_signature(state, func):
        chat_id = state.split('.')[0]
        random_text = state.split('.')[1]
        signature = await cache.get_from_cache_by_id(f'signature.{chat_id}')
        if verify_message(
                chat_id.encode() + ".".encode() + random_text.encode(),
                signature,
                get_public_key()):
            logger.info(f'Signature for telegram chat-id={chat_id} was '
                        f'verified')
            await cache.delete_from_cache_by_id(f'signature.{chat_id}')
            logger.info(f'Signature for telegram chat-id={chat_id} was '
                        f'deleted.')
            return await func(chat_id)
        else:
            logger.warning("User tries to authenticate the second time "
                           "or use an old link or they are already "
                           "authenticated. Push user to generate a new link "
                           "and try again.")
            error_message = """
You are probably trying to authenticate the second time 
or you are using an old link or you are already 
authenticated.
"""
            return False, error_message

    async def init_auth(self, code: str, state: str):
        logger.info('User does initial authorization.')

        async def inner(chat_id):
            logger.info('Creating user credentials.')
            try:
                buc = await Oauth2Manager().build_user_creds(
                        grant=code,
                        client_creds=client_creds
                    )
                user_creds: UserCreds = UserCreds(**buc)
            except HTTPError:
                logger.warning(f'Failed to build user creds',
                               exc_info=True)
                raise BadUserCredsException

            # Redis key='creds.{chat_id}' stores the user's access and refresh
            # tokens and is created automatically when the authorization flow
            # completes for the first time. It expires after 24 hours.
            await cache.put_to_cache_by_id(f'creds.{chat_id}',
                                           json.dumps(user_creds),
                                           86400)
            return (True,)

        return await self.verify_signature(state, inner)

    async def error_auth(self, error: str, state: str):
        logger.info(f'Authorization failed with error:{error}.')

        async def inner(chat_id=None):
            error_message = "You have probably canceled authentication."
            return False, error_message

        return await self.verify_signature(state, inner)

    @staticmethod
    async def refresh_user_creds(
            chat_id: int | str) -> UserCreds | BadUserCredsException:
        logger.info('Refreshing user creds')
        user_creds: UserCreds | None = None
        oauth2manager = Oauth2Manager()
        creds_chat_id = await cache.get_from_cache_by_id(f'creds.{chat_id}')

        # If the access token available, return creds.
        if creds_chat_id:
            logger.info('Access token is available, getting user creds.')
            user_creds = UserCreds(**json.loads(creds_chat_id))

        if not user_creds or oauth2manager.is_expired(user_creds):
            if user_creds and user_creds.refresh_token:
                try:
                    logger.info('User creds are valid and refresh token is '
                                'available. Refreshing creds.')
                    _, user_creds = await oauth2manager.refresh(
                        user_creds=user_creds,
                        client_creds=client_creds)
                    # Save the credentials for the next run
                    await cache.put_to_cache_by_id(f'creds.{chat_id}',
                                                   json.dumps(user_creds),
                                                   86400)
                # if refresh token has expired create new user creds.
                except (AuthError, HTTPError):
                    logger.warning(f'Refresh token for user {chat_id} has '
                                   'expired. Push user to create new '
                                   'credentials.')
                    raise BadUserCredsException
            else:
                logger.warning(f'User {chat_id} tried to do actions without '
                               f'auth. Push user to create new credentials.')
                raise BadUserCredsException

        return user_creds

    @staticmethod
    async def get_user_creds(chat_id: str) -> str | None:
        logger.info('Getting user creds')
        return await cache.get_from_cache_by_id(f'creds.{chat_id}')

    async def auth_user(self, chat_id: str, context):
        if await cache.get_from_cache_by_id(f'creds.{chat_id}'):
            raise UserAlreadyLoggedInException
        else:
            await generate_youtube_login_message(
                context,
                chat_id,
                await self.get_authorization_url(chat_id)
            )

    @staticmethod
    async def logout_user(chat_id: int | str) -> None:
        logger.info('Logging out from user account.')
        await cache.delete_from_cache_by_id(f'creds.{chat_id}')

    async def revoke_user_creds(self, chat_id: int | str, context) -> None:
        logger.info('Revoking user creds.')
        oauth2manager = Oauth2Manager()
        user_creds = await self.refresh_user_creds(chat_id)
        await self.logout_user(chat_id)
        await oauth2manager.revoke(user_creds=user_creds)
        logger.info('User creds has been revoked.')


auth_connector = GoogleAuth()
