"""
Exception handling utilities for the Auth API.
"""

import logging

from helpers.utils import redirect

logger = logging.getLogger(__name__)

general_error_message = """
Something went wrong 🙁. Generate a new link using /auth command and try again.
"""


async def bot_exc_func(exc_level: str, exc_type: str, state: str, *args,
                       **kwargs):
    """
    Handles exceptions in the Auth API and logs them appropriately.

    This function takes an exception level (e.g., 'debug', 'info', 'warning',
    etc.), the exception type, and other details, logs the exception with the
    chat ID extracted from the state, and redirects the user with a generic
    error message.

    :param exc_level: The logging level to use for logging the exception.
    :param exc_type: The type of the exception that occurred.
    :param  state: The state parameter containing the chat ID.
    :param  *args: Additional arguments passed to the exception handler.
    :param  **kwargs: Additional keyword arguments passed to the exception handler.

    :returns: A redirect response containing a generic error message.
    """
    chat_id = state.split('.')[0]
    level = getattr(logger, exc_level)
    level(f'Exception {exc_type} occurred with {chat_id=}.',
          exc_info=False if exc_level in ('debug', 'info') else True)
    return await redirect.redirect_response([general_error_message], chat_id)


exc_func = bot_exc_func
