import logging

from helpers.utils import redirect

logger = logging.getLogger(__name__)


general_error_message = """
Generate a new link using /auth command and try again.
"""


async def bot_exc_func(state: str,
                       *args,
                       **kwargs
                       ):
    chat_id = state.split('.')[0]
    logger.warning(f'Error happened with {chat_id=}.')
    return await redirect.redirect_response([general_error_message], chat_id)


exc_func = bot_exc_func
