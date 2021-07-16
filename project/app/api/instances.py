# project/app/api/routes.py

from typing import List

from app.crud import instances as crud
from db.mongodb import AsyncIOMotorDatabase, get_database
from fastapi import APIRouter, Depends, HTTPException

from app.models.instances import (  # isort:skip
    CreateResponseSchema,
    GetResponseSchema,
    InstanceSchema,
    DeleteResponseSchema,
)


router = APIRouter()


@router.post("/", status_code=201, response_model=CreateResponseSchema)
async def create_instance(
    payload: InstanceSchema, db: AsyncIOMotorDatabase = Depends(get_database)
) -> CreateResponseSchema:
    _id = await crud.post(payload, db)
    return {"_id": _id}


@router.get("/{instance_id}/", response_model=GetResponseSchema)
async def get_instance(
    instance_id: str, db: AsyncIOMotorDatabase = Depends(get_database)
) -> GetResponseSchema:
    instance = await crud.get(instance_id, db)
    if not instance:
        raise HTTPException(status_code=404, detail="Instance not found")
    return instance


@router.get("/", response_model=List[GetResponseSchema])
async def get_all_instances(
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> List[GetResponseSchema]:
    instances = await crud.get_all(db)
    if not instances:
        raise HTTPException(
            status_code=404, detail="No instances found - database is empty!"
        )
    return instances


@router.delete("/{instance_id}/", response_model=DeleteResponseSchema)
async def delete_instance(
    instance_id: str, db: AsyncIOMotorDatabase = Depends(get_database)
) -> DeleteResponseSchema:
    _id = await crud.delete(instance_id, db)
    if not _id:
        raise HTTPException(
            status_code=404, detail=f"Instance with id={_id} not found!"
        )
    return {"_id": _id}
