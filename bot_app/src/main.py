"""
This script defines the entry point for the Telegram bot application.

It configures logging, builds the Telegram application object, defines command
handlers for various bot commands, and starts the polling loop to receive and
process updates from Telegram.
"""

from logging import config

from telegram.ext import ApplicationBuilder, CommandHandler, \
    CallbackQueryHandler
from telegram import Update

from bot_app.src.handlers.main import start, auth, logout, describeme, revoke, describeme_consent
from project_settings.config import bot_settings
from project_settings.logger import LOGGING

config.dictConfig(LOGGING)

if __name__ == '__main__':
    """
    Creates a Telegram application instance using the bot token from configuration.
    """
    application = ApplicationBuilder().token(bot_settings.token).build()

    """
    Defines command handlers for various bot commands:

    - start: Handles the '/start' command
    - auth: Handles the '/auth' command for user authentication
    - logout: Handles the '/logout' command for user logout
    - describeme: Handles the '/describeme' command to initiate the portrait 
    generation process
    - revoke: Handles the '/revoke' command to revoke user access
    - describeme_consent: Handles callback queries related to portrait 
    generation consent
    """

    start_handler = CommandHandler('start', start)
    auth_handler = CommandHandler('auth', auth)
    logout_handler = CommandHandler('logout', logout)
    describeme_handler = CommandHandler('describeme', describeme)
    describeme_consent_handler = CallbackQueryHandler(describeme_consent)
    revoke_handler = CommandHandler('revoke', revoke)

    """
    Adds all defined command handlers to the Telegram application.
    """

    application.add_handler(start_handler)
    application.add_handler(auth_handler)
    application.add_handler(logout_handler)
    application.add_handler(describeme_handler)
    application.add_handler(describeme_consent_handler)
    application.add_handler(revoke_handler)

    """
    Starts the polling loop to receive and process updates from Telegram.

    This loop waits for incoming updates from users and dispatches them to the
    appropriate handler functions based on the type of update (e.g., message,
    callback query).
    """

    application.run_polling(allowed_updates=Update.ALL_TYPES)