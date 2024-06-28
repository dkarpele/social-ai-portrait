from functools import wraps

from fastapi.responses import RedirectResponse
from telegram import Bot

from helpers.exceptions import BadUserCredsException

from settings.config import bot_settings


def handle_bad_user(exc_func):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except BadUserCredsException:
                return await exc_func(*args, **kwargs)

        return wrapper
    return decorator


class RedirectToBot:
    def __init__(self):
        self.bot = Bot(bot_settings.token)
        self.url = bot_settings.url

    async def redirect_response(self, text_list: list, chat_id):
        async with self.bot:
            for text in text_list:
                await self.bot.send_message(text=text,
                                            chat_id=chat_id)
        # return Response(status_code=307,
        #                 content=content,
        #                 headers={'location': self.url})
        return RedirectResponse(url=self.url,
                                )


redirect = RedirectToBot()


async def generate_youtube_login_message(context, chat_id, url: str, ):
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
