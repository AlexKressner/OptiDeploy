# project/app/api/solutions.py

from datetime import datetime
from typing import List

from app.crud import solutions as crud
from app.crud.instances import get as instance_crud_get
from app.optimizer.model import OptimizationModel, ProblemData
from app.optimizer.solver import SCIPParameters, Solver
from bson.objectid import ObjectId
from db.mongodb import AsyncIOMotorDatabase, get_database
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.encoders import jsonable_encoder

from app.models.solutions import (  # isort:skip
    OptimizeResponseSchema,
    SolutionSchema,
    DeleteResponseSchema,
)


router = APIRouter()


# function to build and optimize model instance and save to db as background task
async def optimization(
    solution_id: str,
    instance_id: str,
    data: ProblemData,
    payload: SCIPParameters,
    db: AsyncIOMotorDatabase,
) -> SolutionSchema:
    instance = OptimizationModel(**data)
    model = instance.generate_model()
    solver = Solver(model)
    solver.setParams(payload)
    start_solve = datetime.utcnow()
    solver.run()
    solution = {
        "_id": ObjectId(solution_id),
        "linked_instance_id": ObjectId(instance_id),
        "solve_started_at": start_solve,
        "solved_at": datetime.utcnow(),
        "status": solver.model.getStatus(),
        "scip_parameters": jsonable_encoder(payload) if payload is not None else None,
        "objective_function_value": solver.model.getObjVal(),
        "solution_time": solver.model.getSolvingTime(),
        "gap": solver.model.getGap(),
        "decision_variables": {
            var.name: solver.model.getVal(var) for var in solver.model.getVars()
        },
    }
    await db["solution_collection"].replace_one(
        {"_id": ObjectId(solution_id)}, solution, True
    )


@router.post("/{instance_id}/", status_code=202, response_model=OptimizeResponseSchema)
async def solve_instance(
    instance_id: str,
    background_tasks: BackgroundTasks,
    payload: SCIPParameters = None,
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> OptimizeResponseSchema:
    instance = await instance_crud_get(instance_id, db)
    if not instance:
        raise HTTPException(
            status_code=404, detail=f"No problem instance found with _id={instance_id}!"
        )

    data = {
        key: instance[key]
        for key in instance
        if key not in ["_id", "created_at", "instance_name", "comment"]
    }
    solution_id = await crud.post(instance_id, db)
    background_tasks.add_task(
        optimization,
        solution_id=solution_id,
        instance_id=instance_id,
        data=data,
        payload=payload,
        db=db,
    )
    return {"_id": solution_id, "linked_instance_id": instance_id}


@router.get("/by_solution_id/{solution_id}/", response_model=SolutionSchema)
async def get_by_solution_id(
    solution_id: str, db: AsyncIOMotorDatabase = Depends(get_database)
) -> SolutionSchema:
    solution = await crud.get_solution_by_solution_id(solution_id, db)
    if not solution:
        raise HTTPException(
            status_code=404, detail=f"No solution found with _id={solution_id}!"
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
            detail=f"No solutions found for instance with _id={instance_id}!",
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
            status_code=404, detail=f"Solution with id={_id} not found!"
        )
    return {"_id": _id}
