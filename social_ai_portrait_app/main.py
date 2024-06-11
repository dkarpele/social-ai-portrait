import logging

from social_ai_portrait_app.social_content.content import content
from social_ai_portrait_app.ai_portrait.profile import profile

logger = logging.getLogger(__name__)


async def describe_user(user_creds) -> str:
    logger.debug('Trying to describe user.')
    input_: tuple = await content.get_videos_tags(user_creds)
    return await profile.get_text_profile(input_)
