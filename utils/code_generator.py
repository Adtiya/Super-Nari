from openai import OpenAI
import subprocess
import os
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_code(prompt, previous_error=None):
    messages = [{"role": "system", "content": "You are a helpful AI agent that self-heals broken code."}]
    messages.append({"role": "user", "content": prompt})
    if previous_error:
        messages.append({"role": "user", "content": f"The last version failed with this error:\n{previous_error}\nPlease fix it."})

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

def run_code(code):
    filename = "temp_agent.py"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(code)

    result = subprocess.run(["python", filename], capture_output=True, text=True)
    os.remove(filename)
    return result

def self_healing_agent(prompt, max_retries=3):
    attempt = 0
    error = None
    while attempt < max_retries:
        code = generate_code(prompt, previous_error=error)
        print(f"\n🧠 Attempt {attempt + 1}:\n{code[:200]}...\n")
        result = run_code(code)
        if result.returncode == 0:
            print("✅ Success:\n", result.stdout)
            return code
        else:
            print("❌ Failed:\n", result.stderr)
            error = result.stderr
        attempt += 1

    print("❗Max retries reached. Final error:\n", error)
    return None
