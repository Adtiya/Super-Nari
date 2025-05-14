
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import json, os

router = APIRouter()

@router.get("/logs")
def get_deploy_logs(project: str):
    path = f"./projects/{project}/deploy_logs.json"
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return json.load(f)

class DeployToggle(BaseModel):
    project: str
    auto: bool

@router.post("/auto")
def toggle_auto_deploy(data: DeployToggle):
    path = f"./projects/{data.project}/deploy_config.json"
    config = {"auto": data.auto}
    with open(path, "w") as f:
        json.dump(config, f)
    return config
