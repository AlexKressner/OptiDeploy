# project/db/mongodb_utils.py

from app.config import settings
from db.mongodb import db
from motor.motor_asyncio import AsyncIOMotorClient


async def init_mongo() -> None:
    db.client = AsyncIOMotorClient(settings.CONNECTION)
    db.database = db.client[settings.DATABASE_URL]


async def close_mongo_connection() -> None:
    db.client.close()
