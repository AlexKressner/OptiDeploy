# load_testing/data.py

from dataclasses import dataclass
from random import randrange


@dataclass
class ProblemInstance:
    """Problem instance of the facility location problem"""

    num_customers: int
    num_facilities: int
    average_facility_utilization: float
    instance_name: str = "Facility Location"
    instance_comment: str = (
        "Optimization of facility locations for new logistics network"
    )

    def generate_instance(self):
        customers = [f"c{i}" for i in range(self.num_customers)]
        facilities = [f"f{i}" for i in range(self.num_facilities)]
        transportation_cost = {
            i: {j: randrange(500) for j in facilities} for i in customers
        }
        facility_installation_cost = {i: randrange(7500, 15000) for i in facilities}
        demand = {i: randrange(1000) for i in customers}
        facility_capacity = {
            i: sum(demand.values())
            / self.average_facility_utilization
            / self.num_facilities
            for i in facilities
        }

        return {
            "instance_name": self.instance_name,
            "comment": self.instance_comment,
            "customers": customers,
            "facilities": facilities,
            "transportation_cost": transportation_cost,
            "facility_capacity": facility_capacity,
            "facility_installation_cost": facility_installation_cost,
            "demand": demand,
        }
