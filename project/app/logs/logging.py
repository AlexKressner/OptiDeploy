# project/app/logging.py

import logging
import logging.config

ERROR_LOG_FILENAME = "./app/logs/optideploy_info.log"


def configure_loggin():
    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        # defining the format of messages
        "formatters": {
            "default": {
                "format": "[%(asctime)s] [%(process)d] [%(name)s: %(lineno)d] [%(levelname)s] %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        # defining how to handle the log messages
        "handlers": {
            "logfile": {  # handler name
                "formatter": "default",  # Refer to the formatter defined above
                "class": "logging.FileHandler",  # use a specific filehandler class
                "level": "INFO",  # FILTER: Only ERROR, CRITICAL and INFO logs, i.e. no DEBUG messages,
                "filename": ERROR_LOG_FILENAME,
            },
            "verbose": {
                "formatter": "default",  # Refer to the formatter defined above
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",  # stream to console
            },
        },
        # define the loggers
        "loggers": {
            "uvicorn.access": {
                "propagate": True,
            },
        },
        "root": {"handlers": ["verbose", "logfile"], "level": "DEBUG"},
    }

    logging.config.dictConfig(LOGGING_CONFIG)
