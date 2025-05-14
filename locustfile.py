
from locust import HttpUser, task, between

class AgentLoadTestUser(HttpUser):
    wait_time = between(1, 3)  # Simulates user think time

    @task
    def run_agent(self):
        payload = {
            "project_name": "StressTestProject",
            "feature_name": "ProcessWeatherData",
            "prompt": "Write a Python function to process weather JSON into a daily report",
            "runtime": "python"
        }
        self.client.post("/agent/run", json=payload)
