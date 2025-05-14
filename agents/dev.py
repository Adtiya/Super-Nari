
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def develop(data):
    feature = data.get("feature", "")
    stack = data.get("target", "python")

    prompts = {
        "python": f"Write a complete Python agent to: {feature}",
        "node": f"Write a complete Node.js (JavaScript) agent using async/await to: {feature}",
        "go": f"Write a Go program that implements an agent to: {feature}",
        "java": f"Write a full Java class implementing an agent that can: {feature}",
        "rust": f"Write a Rust module with struct and impl to build an agent that: {feature}",
        "bash": f"Write a Bash script that performs this task: {feature}",
        "swift": f"Write a Swift agent using Foundation to: {feature}",
    }

    prompt = prompts.get(stack, prompts["python"])

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a multilingual AI agent developer."},
                {"role": "user", "content": prompt}
            ]
        )
        return {"code": response.choices[0].message.content.strip()}
    except Exception as e:
        return {"code": f"Error generating code: {str(e)}"}
