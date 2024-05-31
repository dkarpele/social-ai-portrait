import logging

from telegram.ext import ApplicationBuilder, CommandHandler

from handlers import start, auth, logout, describeme
from settings.config import bot_settings

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if __name__ == '__main__':
    application = ApplicationBuilder().token(bot_settings.token).build()

    start_handler = CommandHandler('start', start)
    auth_handler = CommandHandler('auth', auth)
    logout_handler = CommandHandler('logout', logout)
    describeme_handler = CommandHandler('describeme',
                                        describeme)

    application.add_handler(start_handler)
    application.add_handler(auth_handler)
    application.add_handler(logout_handler)
    application.add_handler(describeme_handler)

    application.run_polling()
