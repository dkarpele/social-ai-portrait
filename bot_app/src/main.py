from logging import config

from telegram.ext import ApplicationBuilder, CommandHandler

from bot_app.src.handlers.main import start, auth, logout, describeme, revoke
from settings.config import bot_settings
from settings.logger import LOGGING

config.dictConfig(LOGGING)

if __name__ == '__main__':
    application = ApplicationBuilder().token(bot_settings.token).build()

    start_handler = CommandHandler('start', start)
    auth_handler = CommandHandler('auth', auth)
    logout_handler = CommandHandler('logout', logout)
    describeme_handler = CommandHandler('describeme', describeme)
    revoke = CommandHandler('revoke',revoke)

    application.add_handler(start_handler)
    application.add_handler(auth_handler)
    application.add_handler(logout_handler)
    application.add_handler(describeme_handler)
    application.add_handler(revoke)

    application.run_polling()
