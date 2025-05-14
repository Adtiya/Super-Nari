
from fastapi import APIRouter
from pydantic import BaseModel
import os
import json

router = APIRouter()

DATA_DIR = "./projects"

class AnnotateRequest(BaseModel):
    feature_name: str
    note: str

@router.get("/view")
def view_memory(project: str):
    path = os.path.join(DATA_DIR, project, "memory.json")
    if not os.path.exists(path):
        return {"features": []}
    with open(path, "r") as f:
        memory = json.load(f)
    return {"features": memory}

@router.post("/annotate")
def annotate_memory(req: AnnotateRequest):
    for project_name in os.listdir(DATA_DIR):
        project_path = os.path.join(DATA_DIR, project_name, "memory.json")
        if not os.path.exists(project_path):
            continue
        with open(project_path, "r") as f:
            data = json.load(f)
        updated = False
        for feature in data:
            if feature["feature_name"] == req.feature_name:
                feature["note"] = req.note
                updated = True
        if updated:
            with open(project_path, "w") as f:
                json.dump(data, f, indent=2)
            return {"status": "updated", "project": project_name}
    return {"status": "not_found"}
