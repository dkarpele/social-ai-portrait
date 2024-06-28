import logging

from telegram import Update
from telegram.ext import ContextTypes

from settings.logger import log_chat_id
from bot_app.src.handlers.describe_handlers import (describe_user_handler,
                                                    describeme_consent_handler)
from bot_app.src.handlers.base_handlers import start_handler
from helpers.utils import handle_bad_user
from bot_app.src.handlers.auth_handlers import (auth_user_handler,
                                                logout_user_handler,
                                                revoke_user_creds_handler,
                                                bot_exc_func)
logger = logging.getLogger(__name__)


@log_chat_id(logger)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.debug('start handler')
    await start_handler(update, context)


@log_chat_id(logger)
@handle_bad_user(bot_exc_func)
async def auth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.debug('auth handler')
    await auth_user_handler(update, context)


@log_chat_id(logger)
async def logout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.debug('logout handler')
    await logout_user_handler(update, context)


@log_chat_id(logger)
@handle_bad_user(bot_exc_func)
async def describeme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.debug('describeme handler')
    await describe_user_handler(update, context)


@log_chat_id(logger)
@handle_bad_user(bot_exc_func)
async def describeme_consent(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    logger.debug('describeme_consent handler')
    await describeme_consent_handler(update, context)


@log_chat_id(logger)
@handle_bad_user(bot_exc_func)
async def revoke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.debug('revoke handler')
    await revoke_user_creds_handler(update, context)

