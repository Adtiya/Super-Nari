
from fastapi import APIRouter
from pydantic import BaseModel
from core.current_context import get_focus_from_feature
from core.heuristic_patterns import log_pattern

router = APIRouter()

class FocusRequest(BaseModel):
    prompt: str

class LogRequest(BaseModel):
    project: str
    feature: str

@router.post("/consciousness/current")
def get_focus_info(data: FocusRequest):
    focus = get_focus_from_feature(data.prompt)
    return {"focus": focus}

@router.post("/subconsciousness/log")
def log_user_action(data: LogRequest):
    log_pattern(data.project, data.feature)
    return {"status": "logged"}
