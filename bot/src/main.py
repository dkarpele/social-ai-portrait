import logging

from aiogoogle.auth import Oauth2Manager
from aiohttp.web_response import Response
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, \
    CommandHandler

from settings.config import google_client_creds, bot_settings

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


# url = os.environ['URL']
# port = int(os.environ.get('PORT', 8443))


def authorize(chat_id: int):
    print(google_client_creds)
    if Oauth2Manager().is_ready(google_client_creds):
        uri = Oauth2Manager().authorization_url(
            client_creds=google_client_creds,
            # state=create_secret(),
            # TODO: decode with base64 https://auth0.com/docs/secure/attack-protection/state-parameters
            state=f'{{"chat_id":{chat_id}}}',
            access_type="offline",
            include_granted_scopes=True,
            prompt="select_account",
        )
        return uri
    else:
        return Response(text="Client doesn't have enough info for Oauth2",
                        status=500)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="""
1. You need to login to your Youtube account with /auth command
2. Use /describeme command to create your portrait based on your Youtube liked and disliked videos.
""",
        parse_mode="markdown",
    )


async def auth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(update)
    logging.info(context)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Login to Youtube by pressing the button below. After "
             "successful authentication you will be redirected back to "
             "telegram.",
        parse_mode="markdown",
        reply_markup={
            "inline_keyboard": [
                [
                    {
                        "text": "Connect my account 🎬",
                        "url": authorize(update.effective_chat.id,
                                         )
                    },
                ]
            ]
        })


if __name__ == '__main__':
    application = ApplicationBuilder().token(bot_settings.token).build()

    start_handler = CommandHandler('start', start)
    auth_handler = CommandHandler('auth', auth)

    application.add_handler(start_handler)
    application.add_handler(auth_handler)

    application.run_polling()
