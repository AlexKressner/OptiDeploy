# project/app/models/instances.py

from datetime import datetime
from typing import Optional

from app.optimizer.model import ProblemData, get_schema_extra
from pydantic import BaseModel, Field


class InstanceSchema(ProblemData):
    instance_name: str
    comment: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                **{
                    "instance_name": "Facility Location",
                    "comment": "Optimization of facility locations for new logistics network",
                },
                **get_schema_extra(),
            }
        }


class GetResponseSchema(InstanceSchema):
    id: str = Field(..., alias="_id")
    created_at: datetime


class CreateResponseSchema(BaseModel):
    id: str = Field(..., alias="_id")


class DeleteResponseSchema(BaseModel):
    id: str = Field(..., alias="_id")
