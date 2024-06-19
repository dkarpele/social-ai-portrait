import logging

from fastapi import APIRouter, status

from auth_app.auth import auth_connector
from helpers.utils import redirect
from settings.logger import log_chat_id

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get('/callback/aiogoogle',
            status_code=status.HTTP_200_OK,
            description="Redirect URI",
            response_description="code: code from redirection URL",
            include_in_schema=False
            )
@log_chat_id(logger)
async def callback(state: str,
                   code: int | str | None = None,
                   error: str | None = None,
                   ):
    logger.info('User redirected from authorization URL and will try to auth.')
    chat_id = state.split('.')[0]
    general_error_message = """
Generate a new link using /auth command and try again."""
    if error and not code:
        _, error_message = await auth_connector.error_auth(error, state)
        logger.warning(f'{error_message=}')
        return await redirect.redirect_response(
            [error_message, general_error_message],
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
        return await redirect.redirect_response([general_error_message], chat_id)
