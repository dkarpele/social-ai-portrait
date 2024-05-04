from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

import os

token = os.environ['TOKEN']
url = os.environ['URL']
port = int(os.environ.get('PORT', 5000))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="I'm a bot, please talk to me!")


if __name__ == '__main__':
    application = ApplicationBuilder().token(token).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    application.run_webhook(listen='0.0.0.0',
                            port=port,
                            secret_token=token,
                            webhook_url=url + token)

