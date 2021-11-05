# project/app/config.py

import multiprocessing
import os

# I do not recommend pydantic BaseSettings here because it might cause Celery to raise [ERROR/MainProcess] pidbox
# command error: KeyError('__signature__') error when we launch Flower


# Gunicorn config to be loaded in docker file
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count()
graceful_timeout = 120
timeout = 120
keepalive = 5


class Settings:
    # mongodb settings
    CONNECTION: str = os.environ.get("CONNECTION")
    DATABASE: str = os.environ.get("DATABASE")

    # celery settings
    CELERY_BROKER_URL: str = os.environ.get("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND: str = os.environ.get("CELERY_RESULT_BACKEND")
    CELERY_TASK_TIME_LIMIT: float = os.environ.get("CELERY_TASK_TIME_LIMIT")


settings = Settings()
