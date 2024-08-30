import logging

from bot_app.src.dependencies.db_dep import get_db_service
from db.pg_models.users import User

logger = logging.getLogger(__name__)
db = get_db_service()


async def start_handler(update, context) -> None:
    chat_id = update.effective_chat.id
    first_name = update.effective_chat.first_name
    last_name = update.effective_chat.last_name
    user = User(tg_chat_id=chat_id,
                tg_first_name=first_name,
                tg_last_name=last_name)
    if not await db.exists(User,
                           User.tg_chat_id,
                           chat_id):
        await db.add(user)
    else:
        await db.update(User,
                        User.tg_chat_id,
                        chat_id,
                        dict(tg_first_name=first_name,
                             tg_last_name=last_name))
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"""
Hello{' ' + first_name if first_name else ''}{' ' + last_name if last_name else ''}!
1. You need to login to your Youtube account with /auth command.
2. Use /describeme command to create your profile based on your Youtube \
liked and disliked videos.
    """,
        parse_mode="markdown",
    )
