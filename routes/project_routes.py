
from fastapi import APIRouter
from pydantic import BaseModel
import os, json

router = APIRouter()

class ProjectCreate(BaseModel):
    name: str
    tags: list[str]

class ProjectSeed(BaseModel):
    name: str
    templates: list[str]

@router.post("/project/create")
def create_project(data: ProjectCreate):
    path = f"./projects/{data.name}"
    os.makedirs(path, exist_ok=True)
    return {"status": "created", "project": data.name, "tags": data.tags}

@router.post("/project/seed_from_templates")
def seed_templates(data: ProjectSeed):
    return {"status": "seeded", "project": data.name, "templates_used": data.templates}
