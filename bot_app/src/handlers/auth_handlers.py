"""
This module defines handler functions for Telegram bot commands related to user authentication.

It provides handlers for the following commands:

- /auth: Initiates the user authentication process.
- /logout: Logs out the user and revokes their credentials.
- /revoke: Revokes the bot's access to the user's YouTube account.
"""


import logging

from telegram import Update
from telegram.ext import ContextTypes

from auth_app.auth import auth_connector
from helpers.exceptions import UserAlreadyLoggedInException
from helpers.utils import generate_youtube_login_message

logger = logging.getLogger(__name__)


async def auth_user_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler function for the '/auth' command.

    This function attempts to authenticate the user through the `auth_connector`.
    If successful, it doesn't send any message as the authentication flow is
    handled within the connector. If a `UserAlreadyLoggedInException` occurs,
    it informs the user that they are already logged in and need to logout
    first.

    :param update: The Telegram update object containing information about the
    user's message.
    :param context: The Telegram context object providing access to bot
    functionalities.
    """
    try:
        await auth_connector.auth_user(update.effective_chat.id, context)
    except UserAlreadyLoggedInException:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='You are already logged in! '
                                            'To login again you need to '
                                            '/logout first.')


async def logout_user_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler function for the '/logout' command.

    This function calls the `logout_user` method on the `auth_connector` to log
     out the user. It then sends a confirmation message to the user informing
     them of successful logout.

    :param update: The Telegram update object containing information about the
     user's message.
    :param context: The Telegram context object providing access to bot
    functionalities.
    """
    await auth_connector.logout_user(update.effective_chat.id)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="You have logged out successfully. /auth again!",
    )


async def revoke_user_creds_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler function for the '/revoke' command.

    This function calls the `revoke_user_creds` method on the `auth_connector`
    to revoke the bot's access to the user's YouTube account. It then sends a
    message informing the user that their access has been revoked and provides
    a link to manage their Google permissions.

    :param update: The Telegram update object containing information about the
    user's message.
    :param context: The Telegram context object providing access to bot
    functionalities.
    """
    await auth_connector.revoke_user_creds(update.effective_chat.id, context)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="The bot's access to your YouTube account has been revoked. "
             "To recheck your permissions visit "
             "https://myaccount.google.com/permissions.",
    )


async def bot_exc_func(exc_level: str, exc_type: str, update: Update,
                       context: ContextTypes.DEFAULT_TYPE):
    """
    Exception handler function for unexpected errors during authentication
    commands.

    This function logs the occurred exception with the chat ID and sends a
    generic message to the user informing them that their credentials might be
    invalid. It then attempts to generate a new YouTube login message for the user.

    :param exc_level: The logging level (e.g., 'error', 'warning') for the
    exception.
    :param exc_type: The type of exception that occurred.
    :param update: The Telegram update object containing information about the
    user's message.
    :param context: The Telegram context object providing access to bot
    functionalities.
    """

    chat_id = update.effective_chat.id
    level = getattr(logger, exc_level)
    level(f'Exception {exc_type} occurred with {chat_id=}.',
          exc_info=False if exc_level in ('debug', 'info') else True)

    await context.bot.send_message(chat_id=chat_id,
                                   text='Your credentials are not '
                                        'valid.')
    await generate_youtube_login_message(
        context,
        update.effective_chat.id,
        await auth_connector.get_authorization_url(chat_id)
    )
