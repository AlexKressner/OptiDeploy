# load_testing/locust.py

from locust import HttpUser, between, task

payload = {
    "instance_name": "Facility Location",
    "comment": "Optimization of facility locations for new logistics network",
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


class OptiDeployUser(HttpUser):
    wait_time = between(0.5, 1.5)

    @task
    def solve_instance(self):
        response = self.client.post("/instances", json=payload)
        instance_id = response.json()["_id"]
        self.client.post(f"/solutions/{instance_id}/", name="/solutions")
