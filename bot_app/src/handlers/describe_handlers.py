import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from auth_app.auth import auth_connector
from social_ai_profile_app.ai_portrait.profile import profile
from social_ai_profile_app.social_content.content import content

logger = logging.getLogger(__name__)


async def acquire_user_consent(update):

    prompt = """
To generate your Social AI Profile we need to share an information from your \
most recent 5 liked and disliked YouTube videos with \
[Gemini AI](https://gemini.google.com/) model provided \
by Google. If you agree with this click *YES* button, if not click *NO* \
button. Learn more: \
[Gemini Apps Privacy Hub](https://support.google.com/gemini/answer/13594961)
"""
    keyboard = [
        [
            InlineKeyboardButton("YES", callback_data='YES'),
            InlineKeyboardButton("NO", callback_data='NO'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(prompt,
                                    parse_mode="markdown",
                                    reply_markup=reply_markup)


async def describeme_consent_handler(update, context):
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user
    # is needed
    await query.answer()

    await query.edit_message_text(text=f"Selected option: {query.data}")

    chat_id = update.effective_chat.id
    if query.data == 'NO':
        await context.bot.send_message(
            chat_id=chat_id,
            text="You have explicitly refused to share data with "
            "third-party tools (Gemini AI). Thanks for using our Bot."
        )
    else:
        user_creds = await auth_connector.refresh_user_creds(chat_id)
        await context.bot.send_message(
            chat_id=chat_id,
            text="Please wait a couple of seconds. We will write to you "
                 "when the results are ready.")

        logger.debug('Trying to describe user.')
        input_: tuple = await content.get_videos_tags(user_creds)
        portrait = await profile.get_text_profile(input_)
        await context.bot.send_message(
            chat_id=chat_id,
            text=portrait
        )


async def describe_user_handler(update, context) -> None:
    chat_id = update.effective_chat.id
    if await auth_connector.refresh_user_creds(chat_id):
        await acquire_user_consent(update)
