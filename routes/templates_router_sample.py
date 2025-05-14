
from fastapi import APIRouter
from pydantic import BaseModel
import json
import os
import requests

router = APIRouter()

TEMPLATES_FILE = "./templates.json"
AGENT_RUN_URL = "http://localhost:8000/agent/run"

class TemplateUseRequest(BaseModel):
    project: str
    feature: str
    prompt: str
    runtime: str

@router.get("/list")
def list_templates():
    if not os.path.exists(TEMPLATES_FILE):
        return []
    with open(TEMPLATES_FILE, "r") as f:
        return json.load(f)

@router.post("/use")
def use_template(data: TemplateUseRequest):
    response = requests.post(AGENT_RUN_URL, json={
        "project": data.project,
        "feature": data.feature,
        "prompt": data.prompt,
        "runtime": data.runtime
    })
    return {
        "status": "launched",
        "response": response.json()
    }
