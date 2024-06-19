from telegram import Bot
from fastapi.responses import RedirectResponse, Response
from settings.config import bot_settings


async def generate_youtube_login_message(context, chat_id, url: str, ):
    prompt = """
    Login to Youtube by pressing the button below. After successful \
    authentication you will be redirected back to telegram.
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
