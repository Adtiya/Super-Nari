
from fastapi import APIRouter
from pydantic import BaseModel
import subprocess
import tempfile

router = APIRouter()

class RunRequest(BaseModel):
    language: str
    code: str

@router.post("/run-script")
def run_script(request: RunRequest):
    ext_map = {"python": ".py", "node": ".js", "bash": ".sh"}
    ext = ext_map.get(request.language, ".txt")
    with tempfile.NamedTemporaryFile(mode="w+", suffix=ext, delete=False) as f:
        f.write(request.code)
        f.flush()
        try:
            cmd = {
                "python": ["python", f.name],
                "node": ["node", f.name],
                "bash": ["bash", f.name]
            }.get(request.language, ["cat", f.name])
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            return {"output": result.stdout, "error": result.stderr}
        except Exception as e:
            return {"error": str(e)}
