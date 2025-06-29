import logging

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,  # чтобы не отключать другие логгеры
    'formatters': {
        'base': {
            'format': '[%(asctime)s] [%(levelname)s] - [%(filename)s/%(funcName)s/%(lineno)s: %(message)s]',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'base',
            'level': 'DEBUG',
        },
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'base',
            'filename': 'base.log',
            'level': 'INFO',
        },
    },
    'loggers': {
        'base': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}
