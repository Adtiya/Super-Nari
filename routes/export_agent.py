
from fastapi import APIRouter
from pydantic import BaseModel
from zipfile import ZipFile
import os

router = APIRouter()

EXPORT_BASE = "./memory"

class ExportRequest(BaseModel):
    project: str
    feature: str

@router.post("/export")
def export_agent(req: ExportRequest):
    feature_path = os.path.join(EXPORT_BASE, req.project, f"{req.feature}.json")
    if not os.path.exists(feature_path):
        return {"status": "error", "message": "Feature not found"}
    zip_name = f"./exports/{req.project}_{req.feature}.zip"
    os.makedirs("./exports", exist_ok=True)
    with ZipFile(zip_name, 'w') as zipf:
        zipf.write(feature_path, arcname=f"{req.feature}.json")
    return {"status": "success", "zip": zip_name}
