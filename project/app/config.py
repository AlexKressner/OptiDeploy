# project/app/config.py

import os
from functools import lru_cache
import multiprocessing


class BaseConfig:
    CONNECTION: str = os.environ.get("CONNECTION")
    DATABASE_URL: str = os.environ.get("DATABASE")
    DATABASE_CONNECT_DICT: dict = {}

    CELERY_BROKER_URL: str = os.environ.get("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND: str = os.environ.get("CELERY_RESULT_BACKEND")

    #gunicorn config
    bind = "0.0.0.0:8000"
    workers = multiprocessing.cpu_count()
    graceful_timeout = 120
    timeout = 120
    keepalive = 5


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    DATABASE_URL: str = "web_test"


@lru_cache()
def get_settings():
    config_cls_dict = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig,
    }

    config_name = os.environ.get("APP_CONFIG", "development")
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()
