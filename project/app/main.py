# project/app/main.py

from app.logs.logging import configure_loggin

configure_loggin()

from app.api import instances, solutions  # noqa: E402
from app.workers.celery_utils import create_celery  # noqa: E402
from db.mongodb_utils import close_mongo_connection, init_mongo  # noqa: E402
from fastapi import FastAPI  # noqa: E402


def create_application() -> FastAPI:
    application = FastAPI()
    application.celery_app = create_celery()
    application.include_router(
        instances.router, prefix="/instances", tags=["instances"]
    )
    application.include_router(
        solutions.router, prefix="/solutions", tags=["solutions"]
    )
    return application


app = create_application()
celery = app.celery_app


app.add_event_handler("startup", init_mongo)
app.add_event_handler("shutdown", close_mongo_connection)
