import logging

from helpers.utils import redirect

logger = logging.getLogger(__name__)

general_error_message = """
Something went wrong 🙁. Generate a new link using /auth command and try again.
"""


async def bot_exc_func(exc_level, exc_type, state: str, *args, **kwargs):
    chat_id = state.split('.')[0]
    level = getattr(logger, exc_level)
    level(f'Exception {exc_type} occurred with {chat_id=}.',
          exc_info=False if exc_level in ('debug', 'info') else True)
    return await redirect.redirect_response([general_error_message], chat_id)


exc_func = bot_exc_func
