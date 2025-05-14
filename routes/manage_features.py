
from fastapi import APIRouter, HTTPException
import os
import json

router = APIRouter()

BASE_PATH = "./projects"

@router.get("/features/{project}")
def list_features(project: str):
    memory_file = f"memory_store/{project}.json"
    if not os.path.exists(memory_file):
        return []
    with open(memory_file, "r") as f:
        memory = json.load(f)
    return list(memory.keys())

@router.delete("/features/{project}/{feature}")
def delete_feature(project: str, feature: str):
    # Delete from memory
    memory_file = f"memory_store/{project}.json"
    if os.path.exists(memory_file):
        with open(memory_file, "r") as f:
            memory = json.load(f)
        memory.pop(feature, None)
        with open(memory_file, "w") as f:
            json.dump(memory, f, indent=2)

    # Delete files
    fname = feature.replace(" ", "_").lower()
    paths = [
        f"{BASE_PATH}/{project}/lib/components/{fname}.dart",
        f"{BASE_PATH}/{project}/test/widgets/{fname}_test.dart",
        f"{BASE_PATH}/{project}/docs/{fname}_notes.txt"
    ]
    for path in paths:
        if os.path.exists(path):
            os.remove(path)

    return {"status": "deleted", "feature": feature}

@router.put("/features/{project}/{feature}")
def modify_feature(project: str, feature: str, payload: dict):
    # Replace memory
    memory_file = f"memory_store/{project}.json"
    memory = {}
    if os.path.exists(memory_file):
        with open(memory_file, "r") as f:
            memory = json.load(f)
    memory[feature] = payload.get("output", {})
    with open(memory_file, "w") as f:
        json.dump(memory, f, indent=2)

    # Replace files
    fname = feature.replace(" ", "_").lower()
    with open(f"{BASE_PATH}/{project}/lib/components/{fname}.dart", "w") as f:
        f.write(payload.get("output", {}).get("code", ""))

    with open(f"{BASE_PATH}/{project}/test/widgets/{fname}_test.dart", "w") as f:
        f.write(payload.get("output", {}).get("test", ""))

    with open(f"{BASE_PATH}/{project}/docs/{fname}_notes.txt", "w") as f:
        f.write(payload.get("output", {}).get("plan", ""))

    return {"status": "updated", "feature": feature}
