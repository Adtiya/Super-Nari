
from fastapi import APIRouter, Request
from pydantic import BaseModel
import json
import re
import requests

router = APIRouter()

class FeatureListInput(BaseModel):
    project: str
    stack: str
    methodology: str
    goal: str
    features: str

@router.post("/asi/generate-features")
async def generate_from_goal(input: FeatureListInput):
    lines = re.findall(r"\*\*(.*?)\*\*", input.features)
    project = input.project
    responses = []

    for feature in lines:
        payload = {
            "user": "asi_auto",
            "project": project,
            "feature": feature,
            "agents": ["planner", "dev", "test"],
            "methodology": input.methodology,
            "action": "add",
            "target": input.stack,
            "input_mode": "story"
        }
        try:
            res = requests.post("http://localhost:8000/agent/run", json=payload)
            result = res.json()
            responses.append({
                "feature": feature,
                "status": "success" if res.status_code == 200 else "error",
                "output": result
            })
        except Exception as e:
            responses.append({"feature": feature, "status": "failed", "error": str(e)})

    return {"goal": input.goal, "features_generated": responses}
