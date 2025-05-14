
from fastapi import APIRouter
from pydantic import BaseModel
import os, json

router = APIRouter()

class TagRequest(BaseModel):
    feature: str
    tag: str
    project: str

class BatchActionRequest(BaseModel):
    ids: List[str]
    action: str
    project: str

@router.post("/tag")
def tag_feature(req: TagRequest):
    path = f"./projects/{req.project}/tags.json"
    tags = {}
    if os.path.exists(path):
        with open(path) as f:
            tags = json.load(f)
    tags[req.feature] = req.tag
    with open(path, "w") as f:
        json.dump(tags, f)
    return {"status": "tagged", "feature": req.feature, "tag": req.tag}

@router.post("/batch_action")
def batch_action(req: BatchActionRequest):
    return {
        "status": "processed",
        "count": len(req.ids),
        "action": req.action,
        "timestamp": datetime.utcnow().isoformat()
    }
