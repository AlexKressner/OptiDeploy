# project/app/config.py

import os
from functools import lru_cache
from motor.motor_asyncio import AsyncIOMotorClient


class BaseConfig:
    CONNECTION: AsyncIOMotorClient = AsyncIOMotorClient(os.environ.get("CONNECTION"))
    DATABASE_URL: str = os.environ.get("DATABASE")
    DATABASE_CONNECT_DICT: dict = {}

    CELERY_BROKER_URL: str = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
    CELERY_RESULT_BACKEND: str = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    pass


@lru_cache()
def get_settings():
    config_cls_dict = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig
    }

    config_name = os.environ.get("APP_CONFIG", "development")
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()