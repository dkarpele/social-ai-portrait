import json
import logging

from aiogoogle import AuthError, HTTPError
from aiogoogle.auth import UserCreds, Oauth2Manager
from aiogoogle.auth.utils import create_secret
from aiohttp.web_response import Response

from auth_app.abstract import AbstractAuth
from db.abstract import AbstractCache
from settings.exceptions import signature_doesnt_match_exception, \
    BadUserCredsException
from helpers.encryption import verify_message, get_public_key, get_signature
from settings.config import client_creds

logger = logging.getLogger(__name__)


async def create_signature(cache: AbstractCache, chat_id: int):
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
    async def get_authorization_url(cache: AbstractCache, chat_id: int):
        logger.info('Creating authorization url')
        signature_content = await create_signature(cache, chat_id)

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
    async def init_auth(cache: AbstractCache, code, state):
        logger.info('User does initial authorization.')
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
            oauth2manager = Oauth2Manager()
            logger.info('Creating user credentials.')
            user_creds: UserCreds = UserCreds(
                **await oauth2manager.build_user_creds(
                    grant=code,
                    client_creds=client_creds

                ))
            # Redis key='creds.{chat_id}' stores the user's access and refresh
            # tokens and is created automatically when the authorization flow
            # completes for the first time.
            await cache.put_to_cache_by_id(f'creds.{chat_id}',
                                           json.dumps(user_creds))
        else:
            logger.warning("User tries to authenticate the second time "
                           "or use an old link or they are already "
                           "authenticated. Push user to generate a new link "
                           "using /auth command and try again.")
            raise signature_doesnt_match_exception

    @staticmethod
    async def refresh_user_creds(cache: AbstractCache,
                                 chat_id) -> UserCreds | BadUserCredsException:
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
                                                   json.dumps(user_creds))
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


auth_connector = GoogleAuth()
