
from fastapi import APIRouter
from typing import List
import json, os
from datetime import datetime

router = APIRouter()

@router.get("/logs")
def get_healing_logs(project: str, feature: str):
    path = f"./projects/{project}/healing_logs.json"
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return json.load(f)

@router.post("/retry")
def retry_healing(project: str, feature: str):
    # placeholder for re-run logic
    return {"status": "restarted", "project": project, "feature": feature, "timestamp": datetime.utcnow().isoformat()}
