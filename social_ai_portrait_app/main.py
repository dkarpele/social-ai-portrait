from social_ai_portrait_app.social_content.content import content
from social_ai_portrait_app.ai_portrait.portrait import portrait


async def describe_user(user_creds) -> str:
    input_: tuple = await content.get_videos_tags(user_creds)
    return await portrait.get_text_portrait(input_)
