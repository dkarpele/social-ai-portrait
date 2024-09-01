"""
This module provides utility functions for error handling, bot redirection, and
YouTube login message generation.
"""

from functools import wraps

from fastapi.responses import RedirectResponse
from redis.exceptions import ConnectionError
from telegram import Bot

from helpers.exceptions import BadUserCredsException

from project_settings.config import bot_settings


def handle_exception(exc_func):
    """
    Decorator for exception handling in asynchronous functions.

    This decorator wraps a function and catches specific exceptions. It calls
    the provided `exc_func` with appropriate information for handling the exception
    within the context (e.g., sending an error message to the user).

    :param exc_func: The function to be called for exception handling. It should
                     accept arguments like 'severity' (str), 'error_message' (str),
                     and additional arguments passed to the decorated function.

    :return: A decorator function.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except BadUserCredsException:
                return await exc_func('info', str(BadUserCredsException),
                                      *args, **kwargs)
            except ConnectionError:
                return await exc_func('critical', str(ConnectionError), *args,
                                      **kwargs)

        return wrapper
    return decorator


class RedirectToBot:
    """
    Class for handling redirects to the Telegram bot.

    This class initializes a Telegram bot object using the bot token from
    configuration and stores the bot URL. It provides a method to send a series
    of messages to a chat and redirect the user to the bot URL.
    """
    def __init__(self):
        self.bot = Bot(bot_settings.token)
        self.url = bot_settings.url

    async def redirect_response(self, text_list: list, chat_id):
        """
        Sends a series of messages to a chat and redirects the user to the Telegram bot.

        This method iterates over a list of text messages and sends them to the
        specified chat using the bot object. It then returns a `RedirectResponse`
        object directing the user to the bot URL.

        :param text_list: A list of text messages to be sent to the chat.
        :param chat_id: The Telegram chat ID of the user.
        :return: A `RedirectResponse` object for redirecting the user.
        """
        async with self.bot:
            for text in text_list:
                await self.bot.send_message(text=text,
                                            chat_id=chat_id)
        # return Response(status_code=307,
        #                 content=content,
        #                 headers={'location': self.url})
        return RedirectResponse(url=self.url)


redirect = RedirectToBot()


async def generate_youtube_login_message(context, chat_id: str, url: str, ):
    """
    Generates a message prompting the user to login to YouTube.

    This function constructs a message with instructions and a button for the user
    to log in to YouTube. It includes links to the Privacy Policy and YouTube Terms
    of Service. The message is sent to the specified chat with an inline keyboard
    containing the login button.

    :param context: The Telegram update context object.
    :param chat_id: The Telegram chat ID of the user.
    :param url: The URL for YouTube login.
    """
    prompt = """
Login to Youtube by pressing the button below. By clicking this button you \
agree with [Privacy Policy](https://socialaiprofile.top/privacy/) \
and [YouTube Terms of Service](https://www.youtube.com/t/terms). After \
successful authentication you will be redirected back to telegram. 
"""
    button_text: str = "Connect to YouTube account 🎬"
    await context.bot.send_message(
        chat_id=chat_id,
        text=prompt,
        parse_mode="markdown",
        reply_markup={
            "inline_keyboard": [
                [
                    {
                        "text": button_text,
                        "url": url
                    },
                ]
            ]
        }
    )
