# project/app/worker.py

import os

from celery import Celery

from app.optimizer.model import OptimizationModel, ProblemData
from app.optimizer.solver import SCIPParameters, Solver

from datetime import datetime
from bson.objectid import ObjectId
from fastapi.encoders import jsonable_encoder

from pymongo import MongoClient

from app.models.solutions import OptimizeResponseSchema



celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")


@celery.task(name="optimization")
def optimization(
    instance_id: str,
    data: ProblemData,
    payload: SCIPParameters
):
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
    client = MongoClient(os.environ.get("CONNECTION"))
    database = client[os.environ.get("DATABASE")]
    solution = database["solution_collection"].insert_one(solution)
    client.close()
    return {"_id": str(solution.inserted_id)}