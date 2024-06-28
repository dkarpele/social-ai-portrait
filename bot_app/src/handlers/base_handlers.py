import logging

logger = logging.getLogger(__name__)


async def start_handler(update, context) -> None:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="""
1. You need to login to your Youtube account with /auth command.
2. Use /describeme command to create your profile based on your Youtube \
liked and disliked videos.
    """,
        parse_mode="markdown",
    )
