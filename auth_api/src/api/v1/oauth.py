"""
This module handles OAuth callback logic for the Auth API, specifically
for the Google AioGoogle provider.
"""

import logging

from fastapi import APIRouter, status

from auth_api.src.services.exceptions import exc_func, general_error_message
from auth_app.auth import auth_connector
from helpers.utils import redirect, handle_exception
from project_settings.logger import log_chat_id

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get('/callback/aiogoogle',
            status_code=status.HTTP_200_OK,
            description="Redirect URI",
            response_description="code: code from redirection URL",
            include_in_schema=False
            )
@log_chat_id(logger)
@handle_exception(exc_func)
async def callback(state: str,
                   code: int | str | None = None,
                   error: str | None = None,
                   ):
    """
    Handles OAuth callback for the Google AioGoogle provider.

    This function receives data from the Google authorization flow
    and attempts to authenticate the user.

    :param state: State parameter passed during the authorization flow.
    :param code: Authorization code received from Google (if successful).
    :param error: Error message received from Google (if any).
    :returns: A redirect response containing either a success message or an
        error message depending on the authentication outcome.
    :raises auth_api.src.services.exceptions.CustomException: If an unexpected
        error occurs during authentication.
    """
    logger.info('User redirected from authorization URL and will try to auth.')
    chat_id = state.split('.')[0]

    if error and not code:
        _, error_message = await auth_connector.error_auth(error, state)
        logger.warning(f'{error_message=}')
        return await redirect.redirect_response([error_message,
                                                 general_error_message],
                                                chat_id)
    elif code and not error:
        init_ = await auth_connector.init_auth(code, state)
        if not init_[0]:
            return await redirect.redirect_response([init_[1],
                                                     general_error_message],
                                                    chat_id)
        else:
            logger.info(f'User logged in with chat-id {chat_id}')
            return await redirect.redirect_response(
                ['You have logged in successfully! Now try to /describeme'],
                chat_id)

    else:
        logger.warning('Unknown error happened. Both error and code are None.')
        return await redirect.redirect_response(['Unknown error happened.',
                                                 general_error_message],
                                                chat_id)
        # TODO: http://lol.lol/api/v1/oauth/callback/aiogoogle?state=dddd
        # telegram.error.BadRequest: Chat not found
        # HTTP_401_UNAUTHORIZED
        # if state and not error or state and not code:
        # return HTTP_401_UNAUTHORIZED
