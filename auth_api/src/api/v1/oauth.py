import logging

from fastapi import APIRouter, status
from fastapi.responses import RedirectResponse
from telegram import Bot

from auth_api.src.dependencies.redis import CacheDep
from auth_app.auth import auth_connector
from settings.config import bot_settings
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
async def callback(code: int | str,
                   state: str,
                   cache: CacheDep):
    logger.info('User redirected from authorization URL and will try to auth.')
    bot = Bot(bot_settings.token)
    chat_id = state.split('.')[0]
    await auth_connector.init_auth(cache, code, state)

    async with bot:
        logger.info(f'User logged in with chat-id {chat_id}')
        await bot.send_message(text='You have logged in successfully! Now try '
                                    'to /describeme',
                               chat_id=chat_id)
    return RedirectResponse(url='https://t.me/SocialAIPortraitBot')
