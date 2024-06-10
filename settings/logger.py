import logging
import os
from functools import wraps

from telegram import Update

from settings.config import smtp_settings
from asgi_correlation_id import CorrelationIdFilter
from logging import Filter

LOG_FORMAT = ('{asctime} - {levelname} - {name} - {module}:{funcName}:{lineno}'
              ' - [{correlation_id}] - [{chat_id}] - {message}')
LOG_ENV = os.getenv('LOG_ENV', 'test')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'info')

log_level_condition = LOG_LEVEL.lower() == 'debug' and 'DEBUG' or 'INFO'


class ChatIdLogger(Filter):
    def __init__(self, chat_id: int):
        super().__init__()
        self.chat_id = chat_id

    def filter(self, record):
        record.chat_id = self.chat_id
        return True


def get_log_filename(log_env: str, log_level: str) -> str:
    def get_filename(suffix: str) -> str:
        return f'app_{suffix}.log'

    match log_env.lower(), log_level.lower():
        case ['test', 'info']:
            return get_filename('test_info')
        case ['test', 'debug']:
            return get_filename('test_debug')
        case ['prod', 'info']:
            return get_filename('prod_info')
        case ['prod', 'debug']:
            return get_filename('prod_debug')
        case _:
            raise Exception(f'Incorrect LOG_ENV={log_env} '
                            f'(must be `test` or `prod`)'
                            f' or LOG_LEVEL={log_level} '
                            f'(must be `debug` or `info`)'
                            )


def log_chat_id(logger_name: logging.Logger):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                if isinstance(args[0], Update):
                    chat_id = args[0].effective_chat.id
                else:
                    return
            except IndexError:
                try:
                    if isinstance(kwargs['state'], str):
                        chat_id = kwargs['state'].split('.')[0]
                    else:
                        return
                except KeyError:
                    return

            filter_ = ChatIdLogger(chat_id)

            [logging.getHandlerByName(handler).addFilter(
                filter_) and logger_name.addHandler(
                logging.getHandlerByName(handler))
             for handler in
             logging.getHandlerNames()]

            try:
                return await func(*args, **kwargs)
            finally:
                [logging.getHandlerByName(handler).removeFilter(
                    filter_) and logger_name.addHandler(
                    logging.getHandlerByName(handler))
                 for handler in
                 logging.getHandlerNames()]

        return wrapper

    return decorator


LOGGING_TEST = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'correlation_id': {
            '()': 'asgi_correlation_id.CorrelationIdFilter',
            'uuid_length': 8,
            'default_value': '-',
        },
        'chat_id': {
            '()': ChatIdLogger,
            'chat_id': '-'
        }
    },
    'formatters': {
        'verbose': {
            'format': LOG_FORMAT,
            'style': '{'
        },
    },
    'handlers': {
        "console": {
            'level': 'DEBUG',
            "class": "logging.StreamHandler",
            'filters': ['correlation_id', 'chat_id'],
            "formatter": "verbose",
            "stream": "ext://sys.stdout"
        },
        'file': {
            'level': log_level_condition,
            'filters': ['correlation_id', 'chat_id'],
            'formatter': 'verbose',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': f'{os.getcwd()}/logs/{get_log_filename(LOG_ENV,
                                                               LOG_LEVEL)}',
            'maxBytes': 1024 * 1024,
            'backupCount': 10,
        },
        'critical_mail_handler': {
            'level': 'CRITICAL',
            'filters': ['correlation_id', 'chat_id'],
            'formatter': 'verbose',
            'class': 'logging.handlers.SMTPHandler',
            'mailhost': (smtp_settings.mail_host, smtp_settings.mail_port),
            'credentials': (smtp_settings.username, smtp_settings.password),
            'fromaddr': smtp_settings.sender,
            'toaddrs': [smtp_settings.recipient, ],
            'subject': 'Critical error with application.'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file', 'critical_mail_handler'],
            'formatter': 'verbose',
            'level': 'DEBUG',
        },
        'uvicorn.error': {
            'handlers': ['console', 'file'],
            'level': log_level_condition,
            'propagate': False
        },
        'uvicorn.access': {
            'handlers': ['console', 'file'],
            'level': log_level_condition,
            'propagate': False
        },
        "gunicorn.error": {
            'handlers': ['console', 'file'],
            'level': log_level_condition,
            'propagate': False
        },
        "gunicorn.access": {
            'handlers': ['console', 'file'],
            'level': log_level_condition,
            'propagate': False
        },
        'httpcore': {
            'handlers': ['file'],
            'level': log_level_condition,
            'propagate': False
        },
        'httpx': {
            'handlers': ['file'],
            'level': log_level_condition,
            'propagate': False
        },
        'telegram': {
            'handlers': ['file'],
            'level': log_level_condition,
            'propagate': False
        },
    },
}

LOGGING_PROD = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'correlation_id': {
            '()': 'asgi_correlation_id.CorrelationIdFilter',
            'uuid_length': 8,
            'default_value': '-',
        },
        'chat_id': {
            '()': ChatIdLogger,
            'chat_id': '-'
        }
    },
    'formatters': {
        'verbose': {
            'format': LOG_FORMAT,
            'style': '{'
        },
    },
    'handlers': {
        "console": {
            'level': 'DEBUG',
            "class": "logging.StreamHandler",
            'filters': ['correlation_id', 'chat_id'],
            "formatter": "verbose",
            "stream": "ext://sys.stdout"
        },
        'file': {
            'level': log_level_condition,
            'filters': ['correlation_id', 'chat_id'],
            'formatter': 'verbose',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': f'{os.getcwd()}/logs/{get_log_filename(LOG_ENV,
                                                               LOG_LEVEL)}',
            'maxBytes': 1024 * 1024,
            'backupCount': 10,
        },
        'critical_mail_handler': {
            'level': 'CRITICAL',
            'filters': ['correlation_id', 'chat_id'],
            'formatter': 'verbose',
            'class': 'logging.handlers.SMTPHandler',
            'mailhost': (smtp_settings.mail_host, smtp_settings.mail_port),
            'credentials': (smtp_settings.username, smtp_settings.password),
            'fromaddr': smtp_settings.sender,
            'toaddrs': [smtp_settings.recipient, ],
            'subject': 'Critical error with application.'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file', 'critical_mail_handler'],
            'formatter': 'verbose',
            'level': 'DEBUG',
        },
        'uvicorn.error': {
            'handlers': ['console', 'file'],
            'level': log_level_condition,
            'propagate': False
        },
        'uvicorn.access': {
            'handlers': ['console', 'file'],
            'level': log_level_condition,
            'propagate': False
        },
        "gunicorn.error": {
            'handlers': ['console', 'file'],
            'level': log_level_condition,
            'propagate': False
        },
        "gunicorn.access": {
            'handlers': ['console', 'file'],
            'level': log_level_condition,
            'propagate': False
        },
        'httpcore': {
            'handlers': ['file'],
            'level': log_level_condition,
            'propagate': False
        },
        'httpx': {
            'handlers': ['console', 'file'],
            'level': log_level_condition,
            'propagate': False
        },
        'telegram': {
            'handlers': ['file'],
            'level': log_level_condition,
            'propagate': False
        },
    },
}

LOGGING = LOG_ENV.lower() == 'test' and LOGGING_TEST or LOGGING_PROD
