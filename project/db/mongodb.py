# project/db/mongodb.py

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


class DataBase:
    client: AsyncIOMotorClient = None
    database: AsyncIOMotorDatabase = None


db = DataBase()


async def get_database() -> AsyncIOMotorClient:
    return db.database
