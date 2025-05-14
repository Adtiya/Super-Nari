
from fastapi import APIRouter, Request
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

router = APIRouter()

class GoalInput(BaseModel):
    goal: str

@router.post("/asi/goal")
async def define_goal(input: GoalInput):
    prompt = f"""
You are Super NARI ASI. Break down the following high-level goal into a sequence of smart AI-driven features for an app or system.
Goal: "{input.goal}"
Provide it as a markdown list.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a strategic AGI engineer capable of intelligent feature planning."},
                {"role": "user", "content": prompt}
            ]
        )
        return {"goal": input.goal, "features": response.choices[0].message.content.strip()}
    except Exception as e:
        return {"error": str(e)}
