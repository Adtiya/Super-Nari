
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class GoalPrompt(BaseModel):
    goal: str

@router.post("/asi/breakdown")
def breakdown(goal: GoalPrompt):
    return {
        "goal": goal.goal,
        "features": [
            {"name": "PDFParser", "prompt": "Extract text from PDFs"},
            {"name": "Summarizer", "prompt": "Summarize extracted text"},
            {"name": "Uploader", "prompt": "Upload summaries to Airtable"}
        ]
    }

@router.post("/asi/create_features")
def create_from_list(items: list[dict]):
    return {"status": "created", "count": len(items)}
