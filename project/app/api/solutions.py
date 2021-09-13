# project/app/api/solutions.py

from typing import List

from app.crud import solutions as crud
from app.crud.instances import get as instance_crud_get
from app.optimizer.solver_parameters import SolverParameters
from app.workers.tasks import optimization
from celery.result import AsyncResult
from db.mongodb import AsyncIOMotorDatabase, get_database
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.encoders import jsonable_encoder

from app.models.solutions import (  # isort:skip
    TaskResponseSchema,
    SolutionSchema,
    DeleteResponseSchema,
    OptimizeResponseSchema,
)

router = APIRouter()


@router.post("/{instance_id}/", status_code=202, response_model=TaskResponseSchema)
async def solve_instance(
    instance_id: str,
    background_tasks: BackgroundTasks,
    payload: SolverParameters = None,
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> TaskResponseSchema:
    instance = await instance_crud_get(instance_id, db)
    if not instance:
        raise HTTPException(
            status_code=404,
            detail=f"No problem instance found with _id {instance_id} !",
        )

    data = {
        key: instance[key]
        for key in instance
        if key not in ["_id", "created_at", "instance_name", "comment"]
    }
    optimization_task = optimization.delay(
        instance_id=instance_id, data=data, payload=jsonable_encoder(payload)
    )
    return {"task_id": optimization_task.id}


@router.get("/tasks/{task_id}", response_model=OptimizeResponseSchema)
def get_status(task_id) -> OptimizeResponseSchema:
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result,
    }
    return result


@router.get("/by_solution_id/{solution_id}/", response_model=SolutionSchema)
async def get_by_solution_id(
    solution_id: str, db: AsyncIOMotorDatabase = Depends(get_database)
) -> SolutionSchema:
    solution = await crud.get_solution_by_solution_id(solution_id, db)
    if not solution:
        raise HTTPException(
            status_code=404, detail=f"No solution found with _id {solution_id} !"
        )
    return solution


@router.get("/by_instance_id/{instance_id}/", response_model=List[SolutionSchema])
async def get_by_instance_id(
    instance_id: str, db: AsyncIOMotorDatabase = Depends(get_database)
) -> List[SolutionSchema]:
    solutions = await crud.get_solutions_by_instance_id(instance_id, db)
    if not solutions:
        raise HTTPException(
            status_code=404,
            detail=f"No solutions found for instance with _id {instance_id} !",
        )
    return solutions


@router.get("/", response_model=List[SolutionSchema])
async def get_all_solutions(
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> List[SolutionSchema]:
    solutions = await crud.get_all(db)
    if not solutions:
        raise HTTPException(
            status_code=404, detail="No solutions found - database is empty!"
        )
    return solutions


@router.delete("/{solution_id}/", response_model=DeleteResponseSchema)
async def delete_solution(
    solution_id: str, db: AsyncIOMotorDatabase = Depends(get_database)
) -> DeleteResponseSchema:
    _id = await crud.delete(solution_id, db)
    if not _id:
        raise HTTPException(
            status_code=404, detail=f"Solution with id {_id} not found!"
        )
    return {"_id": _id}
