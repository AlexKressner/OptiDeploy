# project/app/config.py

import multiprocessing

from pydantic import BaseSettings

# Gunicorn config to be loaded in docker file
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count()
graceful_timeout = 120
timeout = 120
keepalive = 5


class Settings(BaseSettings):
    # mongodb settings
    CONNECTION: str
    DATABASE: str

    # celery settings
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    CELERY_TASK_TIME_LIMIT: float

    class Config:
        case_sensitive = True


settings = Settings()
