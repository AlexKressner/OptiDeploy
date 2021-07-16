# project/db/mongodb_utils.py

import os

from db.mongodb import db
from motor.motor_asyncio import AsyncIOMotorClient


async def init_mongo() -> None:
    db.client = AsyncIOMotorClient(os.environ.get("CONNECTION"))
    db.database = db.client[os.environ.get("DATABASE")]


async def close_mongo_connection() -> None:
    db.client.close()
