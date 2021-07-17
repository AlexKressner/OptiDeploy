# project/app/crud/instances.py

from datetime import datetime
from typing import Union

from app.models.instances import DeleteResponseSchema, InstanceSchema
from bson.objectid import ObjectId
from db.mongodb import AsyncIOMotorDatabase
from fastapi.encoders import jsonable_encoder


async def post(payload: InstanceSchema, db: AsyncIOMotorDatabase) -> str:
    payload = {**jsonable_encoder(payload), **{"created_at": datetime.utcnow()}}
    instance = await db["instance_collection"].insert_one(payload)
    return str(instance.inserted_id)


async def get_all(db: AsyncIOMotorDatabase) -> Union[list, None]:
    instances = []
    collection = db["instance_collection"].find()
    if collection:
        async for instance in collection:
            instance["_id"] = str(instance["_id"])
            instances.append(instance)
        return instances
    return None


async def get(instance_id: str, db: AsyncIOMotorDatabase) -> Union[dict, None]:
    instance = await db["instance_collection"].find_one({"_id": ObjectId(instance_id)})
    if instance:
        instance["_id"] = str(instance["_id"])
        return instance
    return None


async def delete(
    instance_id: str, db: AsyncIOMotorDatabase
) -> Union[DeleteResponseSchema, None]:
    instance = await db["instance_collection"].find_one_and_delete(
        {"_id": ObjectId(instance_id)}, projection=["_id"]
    )
    if instance:
        _id = str(instance["_id"])
        return _id
    return None
