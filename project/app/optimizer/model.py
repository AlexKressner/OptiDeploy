# project/app/optimizer/model.py

from typing import Dict, List

from pydantic import BaseModel
from pyscipopt import Model, quicksum

################################################################
# definition of pydantic model for data of a problem instance
# example: facility location problem
################################################################


class ProblemData(BaseModel):
    customers: List[str]
    facilities: List[str]
    transportation_cost: Dict[str, Dict[str, int]]
    facility_capacity: Dict[str, int]
    facility_installation_cost: Dict[str, int]
    demand: Dict[str, int]


# Example for problem data to show in openapi doc
def get_schema_extra() -> ProblemData:
    return {
        "customers": ["c1", "c2", "c3", "c4", "c5"],
        "facilities": ["f1", "f2", "f3"],
        "transportation_cost": {
            "c1": {"f1": 4, "f2": 6, "f3": 9},
            "c2": {"f1": 5, "f2": 4, "f3": 7},
            "c3": {"f1": 6, "f2": 3, "f3": 4},
            "c4": {"f1": 8, "f2": 5, "f3": 3},
            "c5": {"f1": 10, "f2": 8, "f3": 4},
        },
        "facility_capacity": {"f1": 500, "f2": 500, "f3": 500},
        "facility_installation_cost": {"f1": 1000, "f2": 1000, "f3": 1000},
        "demand": {"c1": 80, "c2": 270, "c3": 250, "c4": 160, "c5": 180},
    }


###########################################################
# definition of the SCIP optimization model
# example: facility location problem
###########################################################


class OptimizationModel(ProblemData):
    def generate_model(self):
        model = Model("flp")

        # Define decision variables
        x, y = {}, {}
        for j in self.facilities:
            y[j] = model.addVar(vtype="B", name=f"y_{j}")
            for i in self.customers:
                x[i, j] = model.addVar(vtype="C", name=f"x_{i,j}")

        # Define constraint set
        for i in self.customers:
            model.addCons(
                quicksum(x[i, j] for j in self.facilities) == self.demand[i],
                f"Demand_{i}",
            )
        for j in self.facilities:
            model.addCons(
                quicksum(x[i, j] for i in self.customers)
                <= self.facility_capacity[j] * y[j],
                f"Capacity_{j}",
            )
        for (i, j) in x:
            model.addCons(x[i, j] <= self.demand[i] * y[j], f"Strong_{i,j}")

        # Define objective function
        model.setObjective(
            quicksum(self.facility_installation_cost[j] * y[j] for j in self.facilities)
            + quicksum(
                self.transportation_cost[i][j] * x[i, j]
                for i in self.customers
                for j in self.facilities
            ),
            "minimize",
        )
        return model
