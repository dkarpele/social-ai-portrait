import logging

from auth_app.auth import auth_connector
from helpers.exceptions import BadUserCredsException
from helpers.utils import generate_youtube_login_message

logger = logging.getLogger(__name__)


async def start_handler(update, context) -> None:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="""
1. You need to login to your Youtube account with /auth command.
2. Use /describeme command to create your profile based on your Youtube \
liked and disliked videos.
    """,
        parse_mode="markdown",
    )


def handle_bad_user(func):
    async def wrapper(update, context):
        try:
            await func(update, context)
        except BadUserCredsException:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text='Your credentials are not '
                                                'valid.')
            await generate_youtube_login_message(
                context,
                update.effective_chat.id,
                await auth_connector.get_authorization_url(update.effective_chat.id)
            )

    return wrapper
