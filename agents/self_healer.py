
from openai import OpenAI
import subprocess
import os
import re

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def remove_unicode_emoji(text):
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F700-\U0001F77F"
        "\U0001F780-\U0001F7FF"
        "\U0001F800-\U0001F8FF"
        "\U0001F900-\U0001F9FF"
        "\U0001FA00-\U0001FA6F"
        "\U0001FA70-\U0001FAFF"
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub('', text)

def extract_code_block(text):
    match = re.search(r"```(?:python)?\n(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    # fallback: use only potential print lines or defs
    lines = text.splitlines()
    return "\n".join([line for line in lines if 'print(' in line or line.strip().startswith('def ')])

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
    import tempfile
    filename = os.path.join(tempfile.gettempdir(), "temp_agent.py")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(code)

    result = subprocess.run(["python", filename], capture_output=True, text=True)
    os.remove(filename)
    return result

def self_healing_agent(prompt, max_retries=3):
    attempt = 0
    error = None
    healing_steps = []
    while attempt < max_retries:
        raw_code = generate_code(prompt, previous_error=error)
        cleaned_code = remove_unicode_emoji(extract_code_block(raw_code))
        healing_steps.append({
            "attempt": attempt + 1,
            "code": cleaned_code[:1000],
        })
        result = run_code(cleaned_code)
        if result.returncode == 0:
            healing_steps[-1]["success"] = True
            healing_steps[-1]["output"] = result.stdout
            return {"status": "success", "steps": healing_steps}
        else:
            healing_steps[-1]["success"] = False
            healing_steps[-1]["error"] = result.stderr
            error = result.stderr
        attempt += 1

    return {"status": "failed", "steps": healing_steps, "final_error": error}
