# project/app/crud/solutions.py

from typing import Union, List
from db.mongodb import AsyncIOMotorDatabase
from bson.objectid import ObjectId
from app.models.solutions import (  # isort:skip
    SolutionSchema,
    DeleteResponseSchema,
)


async def post(instance_id:str, db) -> str:
    solution = await db["solution_collection"].insert_one({"linked_instance_id": ObjectId(instance_id)})
    return str(solution.inserted_id)


async def get_solution_by_solution_id(solution_id:str, db) -> Union[SolutionSchema,None]:
    solution = await db["solution_collection"].find_one({"_id": ObjectId(solution_id)})
    if solution:
        solution["_id"]=str(solution["_id"])
        solution["linked_instance_id"]=str(solution["linked_instance_id"])
        return solution 
    return None


async def get_solutions_by_instance_id(instance_id:str, db) -> Union[List[SolutionSchema],None]:
    cursor = db["solution_collection"].find({"linked_instance_id": ObjectId(instance_id)})
    solutions = await cursor.to_list(length=10000)
    if solutions:
        for solution in solutions:
            solution["_id"]=str(solution["_id"])
            solution["linked_instance_id"]=str(solution["linked_instance_id"])
        return solutions
    return None


async def get_all(db: AsyncIOMotorDatabase) -> Union[SolutionSchema,None]:
    cursor = db["solution_collection"].find()
    solutions = await cursor.to_list(length=10000)
    if solutions:
        for solution in solutions:
            solution["_id"]=str(solution["_id"])
            solution["linked_instance_id"]=str(solution["linked_instance_id"])
        return solutions
    return None


async def delete(solution_id:str, db: AsyncIOMotorDatabase) -> Union[DeleteResponseSchema,None]:
    solution = await db["solution_collection"].find_one_and_delete({"_id": ObjectId(solution_id)}, projection=["_id"])
    if solution: 
        _id = str(solution["_id"])
        return _id
    return None