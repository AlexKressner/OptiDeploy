# project/app/models/solutions.py

from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class OptimizeResponseSchema(BaseModel):
    id: str = Field(..., alias="_id")
    linked_instance_id: str


class SolutionSchema(BaseModel):
    id: str = Field(..., alias="_id")
    linked_instance_id: str
    solve_started_at: datetime
    solved_at: Optional[datetime] = None
    status: Optional[str] = None
    scip_parameters: Optional[Dict] = None
    objective_function_value: Optional[float] = None
    solution_time: Optional[float] = None
    gap: Optional[float] = None
    decision_variables: Optional[Dict] = None


class DeleteResponseSchema(BaseModel):
    id: str = Field(..., alias="_id")
