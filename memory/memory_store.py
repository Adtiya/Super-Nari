
import json
import os

def save_project_memory(project, feature, data):
    os.makedirs("memory_store", exist_ok=True)
    path = f"memory_store/{project}.json"
    memory = {}
    if os.path.exists(path):
        with open(path, "r") as f:
            memory = json.load(f)
    memory[feature] = data
    with open(path, "w") as f:
        json.dump(memory, f, indent=2)

def load_project_memory(project):
    path = f"memory_store/{project}.json"
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}
