from auth_app.auth import auth_connector


async def bot_login_message(cache, context, update, text: str):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode="markdown",
        reply_markup={
            "inline_keyboard": [
                [
                    {
                        "text": "Connect my account 🎬",
                        "url": await auth_connector.get_authorization_url(
                            cache,
                            update.effective_chat.id)
                    },
                ]
            ]
        })
