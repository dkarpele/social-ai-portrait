import os
import smtplib

from settings.config import smtp_settings

LOG_FORMAT = '{asctime} - {levelname} - {name} - {module}:{funcName}:{lineno} - {message}'
LOG_ENV = os.getenv('LOG_ENV', 'test')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'info')

log_level_condition = LOG_LEVEL.lower() == 'debug' and 'DEBUG' or 'INFO'


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


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': LOG_FORMAT,
            'style': '{'
        },
    },
    'handlers': {
        "console": {
            'level': 'INFO',
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "stream": "ext://sys.stdout"
        },
        'file': {
            'level': log_level_condition,
            'formatter': 'verbose',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': f'{os.getcwd()}/logs/{get_log_filename(LOG_ENV,
                                                               LOG_LEVEL)}',
            'maxBytes': 1024 * 1024,
            'backupCount': 10,
        },
        'critical_mail_handler': {
            'level': 'CRITICAL',
            'formatter': 'verbose',
            'class': 'logging.handlers.SMTPHandler',
            'mailhost': (smtp_settings.mail_host, smtp_settings.mail_port),
            'credentials': (smtp_settings.username,smtp_settings.password),
            'fromaddr': smtp_settings.sender,
            'toaddrs': [smtp_settings.recipient,],
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
    },
}
