# project/app/celery/tasks.py

from datetime import datetime

from app.config import settings
from app.optimizer.model import OptimizationModel, ProblemData
from app.optimizer.solver import SCIPParameters, Solver
from bson.objectid import ObjectId
from celery import shared_task
from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient


@shared_task
def optimization(instance_id: str, data: ProblemData, payload: SCIPParameters):
    instance = OptimizationModel(**data)
    model = instance.generate_model()
    solver = Solver(model)
    solver.setParams(payload)
    start_solve = datetime.utcnow()
    solver.run()
    solution = {
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
    client = MongoClient(settings.CONNECTION)
    database = client[settings.DATABASE_URL]
    solution = database["solution_collection"].insert_one(solution)
    client.close()
    return {"_id": str(solution.inserted_id)}
