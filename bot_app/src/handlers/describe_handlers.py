import logging

from auth_app.auth import auth_connector
from social_ai_profile_app.ai_portrait.profile import profile
from social_ai_profile_app.social_content.content import content

logger = logging.getLogger(__name__)


async def describe_user_handler(update, context) -> None:
    user_creds = await auth_connector.refresh_user_creds(update.effective_chat.id)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Please wait a couple of seconds. We will write to you "
             "when the results are ready.")

    logger.debug('Trying to describe user.')
    input_: tuple = await content.get_videos_tags(user_creds)
    portrait = await profile.get_text_profile(input_)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=portrait
    )
