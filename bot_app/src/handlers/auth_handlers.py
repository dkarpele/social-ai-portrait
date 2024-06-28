import logging

from auth_app.auth import auth_connector
from helpers.exceptions import UserAlreadyLoggedInException
from helpers.utils import generate_youtube_login_message

logger = logging.getLogger(__name__)


async def auth_user_handler(update, context) -> None:
    try:
        await auth_connector.auth_user(update.effective_chat.id, context)
    except UserAlreadyLoggedInException:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='You are already logged in! '
                                            'To login again you need to '
                                            '/logout first.')


async def logout_user_handler(update, context) -> None:
    await auth_connector.logout_user(update.effective_chat.id)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="You have logged out successfully. /auth again!",
    )


async def revoke_user_creds_handler(update, context) -> None:
    await auth_connector.revoke_user_creds(update.effective_chat.id, context)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="The bot's access to your YouTube account has been revoked. "
             "To recheck your permissions visit "
             "https://myaccount.google.com/permissions.",
    )


async def bot_exc_func(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text='Your credentials are not '
                                        'valid.')
    await generate_youtube_login_message(
        context,
        update.effective_chat.id,
        await auth_connector.get_authorization_url(update.effective_chat.id)
    )
