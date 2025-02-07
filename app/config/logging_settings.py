import sys

from config.log_filters import (
    DebugInfoLogFilter, WarningCriticalLogFilter, ErrorLogFilter
)

logging_config = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "default": {
            "format": "#%(levelname)-8s %(name)s:%(funcName)s - %(message)s"
        },
        "formatter_1": {
            "format": "[%(asctime)s] #%(levelname)-8s %(filename)s:"
                      "%(lineno)d - %(name)s:%(funcName)s - %(message)s"
        },
    },
    "filters": {
        "warning_critical_filter": {
            "()": WarningCriticalLogFilter,
        },
        "error_filter": {
            "()": ErrorLogFilter,
        },
        "debug_info_filter": {
            "()": DebugInfoLogFilter,
        }
    },
    "handlers": {
        "default": {
            "class": "logging.StreamHandler",
            "formatter": "default"
        },
        "stderr": {
            "class": "logging.StreamHandler",
            "level": "ERROR",
            "formatter": "formatter_1",
        },
        "stdout": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "filters": ["debug_info_filter", ],
            "stream": sys.stdout
        },
        "error_file": {
            "class": "logging.FileHandler",
            "filename": "error.log",
            "mode": "w",
            "level": "DEBUG",
            "formatter": "formatter_1",
            "filters": ["error_filter"]
        },
        "warning_file": {
            "class": "logging.FileHandler",
            "filename": "warning.log",
            "level": "WARNING",
            "mode": "w",
            "formatter": "formatter_1",
            "filters": ["warning_critical_filter"]
        }
    },
    "loggers": {
        "users.router": {
            "level": "INFO",
            "handlers": [
                "stdout", "stderr", "warning_file", "error_file"
            ]
        },
        "main": {
            "level": "INFO",
            "formatter": "default",
            "handlers": ["default"]
        }
    },
    # "root": {
    #     "formatter": "default",
    #     "handlers": ["default"]
    # }
}
