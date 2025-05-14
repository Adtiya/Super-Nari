
from fastapi import APIRouter
import shutil

router = APIRouter()

RUNTIMES = {
    "python": "python",
    "node": "node",
    "go": "go",
    "bash": "bash",
    "java": "javac",
    "rust": "rustc",
    "swift": "swift"
}

@router.get("/runtime/check")
def check_runtimes():
    availability = {lang: bool(shutil.which(cmd)) for lang, cmd in RUNTIMES.items()}
    return {"runtimes": availability}
