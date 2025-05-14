
from fastapi import APIRouter
from pydantic import BaseModel
import datetime

router = APIRouter()

class TestRun(BaseModel):
    feature: str
    project: str
    input_text: str

class ChainConfig(BaseModel):
    source: str
    target: str
    project: str

@router.post("/test_case/run")
def run_test_case(data: TestRun):
    return {
        "feature": data.feature,
        "input": data.input_text,
        "output": f"Simulated output from {data.feature}",
        "status": "passed"
    }

@router.post("/chain/configure")
def configure_chain(cfg: ChainConfig):
    return {
        "status": "linked",
        "from": cfg.source,
        "to": cfg.target,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
