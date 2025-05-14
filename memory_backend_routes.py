
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import json
import os

app = FastAPI()

# CORS middleware for frontend calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = "./projects"  # Root directory where memory is stored

class AnnotateRequest(BaseModel):
    feature_name: str
    note: str

@app.get("/memory/view")
def view_memory(project: str):
    path = os.path.join(DATA_DIR, project, "memory.json")
    if not os.path.exists(path):
        return {"features": []}
    with open(path, "r") as f:
        memory = json.load(f)
    return {"features": memory}

@app.post("/memory/annotate")
def annotate_memory(req: AnnotateRequest):
    # Find and update the matching feature
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
