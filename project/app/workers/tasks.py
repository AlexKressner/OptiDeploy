# project/app/celery/tasks.py

from datetime import datetime

from app.config import settings
from app.models.data import ProblemData
from app.optimizer.solver import Solver
from app.optimizer.solver_parameters import SolverParameters
from bson.objectid import ObjectId
from celery import shared_task
from pymongo import MongoClient


@shared_task
def optimization(instance_id: str, data: ProblemData, payload: SolverParameters):
    solver = Solver(**data)
    solver.build_model()
    solver.set_solver_parameters(payload)
    start_solve = datetime.utcnow()
    solver.solve_instance()
    solution = solver.get_solution_status()
    solution["linked_instance_id"] = ObjectId(instance_id)
    solution["solve_started_at"] = start_solve
    solution["solved_at"] = datetime.utcnow()
    client = MongoClient(settings.CONNECTION)
    database = client[settings.DATABASE_URL]
    solution = database["solution_collection"].insert_one(solution)
    client.close()
    return {"_id": str(solution.inserted_id)}
