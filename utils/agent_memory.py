
import os
import json

def save_agent_memory(project: str, feature: str, memory: dict):
    os.makedirs(f"./memory/{project}", exist_ok=True)
    with open(f"./memory/{project}/{feature}.json", "w") as f:
        json.dump(memory, f, indent=2)

def load_agent_memory(project: str, feature: str):
    path = f"./memory/{project}/{feature}.json"
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)
