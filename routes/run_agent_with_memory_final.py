
from fastapi import APIRouter
from pydantic import BaseModel
import os
import json
from datetime import datetime

router = APIRouter()

class AgentRequest(BaseModel):
    project: str
    feature: str
    prompt: str
    runtime: str

def save_to_memory(project: str, feature: str, prompt: str, generated_code: str):
    memory_path = os.path.abspath(os.path.join("projects", project, "memory.json"))
    os.makedirs(os.path.dirname(memory_path), exist_ok=True)

    new_entry = {
        "feature_name": feature,
        "created_at": datetime.utcnow().isoformat(),
        "prompt": prompt,
        "code": generated_code,
        "status": "success"
    }

    memory_data = []
    if os.path.exists(memory_path):
        try:
            with open(memory_path, "r") as f:
                memory_data = json.load(f)
        except json.JSONDecodeError:
            print("⚠️ memory.json was malformed, resetting.")
            memory_data = []

    memory_data.append(new_entry)

    with open(memory_path, "w") as f:
        json.dump(memory_data, f, indent=2)

    print(f"✅ Memory saved to {memory_path}")
    print(f"🧠 Entries in memory: {len(memory_data)}")

@router.post("/run")
def run_agent(data: AgentRequest):
    # Simulated GPT logic generation
    generated_code = f"def add(a, b):\n    return a + b  # for feature: {data.feature}"

    # Create directories and save agent logic
    agent_dir = os.path.join("projects", data.project, "agents")
    os.makedirs(agent_dir, exist_ok=True)
    file_path = os.path.join(agent_dir, f"{data.feature}.py")

    with open(file_path, "w") as f:
        f.write(generated_code)

    print(f"📁 Code saved to: {file_path}")

    # Save memory
    save_to_memory(data.project, data.feature, data.prompt, generated_code)

    return {
        "status": "success",
        "project": data.project,
        "feature": data.feature,
        "generated_code": generated_code,
        "saved_logic_path": file_path
    }
