from telegram import Update
from telegram.ext import ContextTypes

from auth_app.auth import auth_connector
from dependencies.redis import get_cache_service
from messages import bot_login_message
from settings.exceptions import BadUserCredsException
from social_ai_portrait_app.main import describe_user

cache = get_cache_service()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="""
1. You need to login to your Youtube account with /auth command
2. Use /describeme command to create your portrait based on your Youtube \
liked and disliked videos.
""",
        parse_mode="markdown",
    )


async def auth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await cache.get_from_cache_by_id(f'creds.{update.effective_chat.id}'):
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='You are already logged in! '
                                            'To login again you need to '
                                            '/logout first.')
    else:
        text = """
Login to Youtube by pressing the button below. After successful \
authentication you will be redirected back to telegram.
"""
        await bot_login_message(cache, context, update, text)


async def logout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await cache.delete_from_cache_by_id(
        f'creds.{update.effective_chat.id}')
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="You have logged out successfully. /auth again!",
    )


async def describeme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_creds = await auth_connector.refresh_user_creds(
            cache,
            update.effective_chat.id)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Please wait a couple of seconds. We will write to you "
                 "when the results are ready.")
        portrait: str = await describe_user(user_creds)

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=portrait
        )
    except BadUserCredsException:
        text = """
Your credentials are not valid. Login to Youtube by pressing the button \
below. After successful authentication you will be redirected back to telegram.
"""
        await bot_login_message(cache, context, update, text)
