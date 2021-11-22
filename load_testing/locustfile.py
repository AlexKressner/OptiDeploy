# load_testing/locust.py

from locust import HttpUser, between, task

from data import ProblemInstance


class OptiDeployUser(HttpUser):
    wait_time = between(0.5, 1.5)

    @task
    def solve_instance(self):
        instance = ProblemInstance(
            num_customers=250,
            num_facilities=15,
            average_facility_utilization=0.5,
        )
        response = self.client.post("/instances", json=instance.generate_instance())
        instance_id = response.json()["_id"]
        self.client.post(f"/solutions/{instance_id}/", name="/solutions")
