# project/app/celery_utils.py

from app.config import settings
from celery import current_app as current_celery_app


def create_celery():
    celery_app = current_celery_app
    celery_app.config_from_object(settings, namespace="CELERY")

    return celery_app
