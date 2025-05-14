
from fastapi import APIRouter, Request
from agents.self_healer import self_healing_agent

router = APIRouter()

@router.post("/self-heal")
async def run_self_healer(request: Request):
    try:
        data = await request.json()
        prompt = data.get("prompt")
        if not prompt:
            return {"status": "error", "message": "Missing 'prompt'"}

        result = self_healing_agent(prompt)
        return result

    except Exception as e:
        return {"status": "error", "message": str(e)}
