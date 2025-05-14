
import os
import re

EXTENSIONS = {
    "python": ".py",
    "node": ".js",
    "go": ".go",
    "java": ".java",
    "rust": ".rs",
    "bash": ".sh"
}

def sanitize_filename(name, max_length=50):
    cleaned = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    return cleaned[:max_length]

def save_agent_logic(project, feature_name, code, target="python"):
    ext = EXTENSIONS.get(target.lower(), ".txt")
    safe_name = sanitize_filename(feature_name)
    base_path = f"../projects/{project}/agents"
    os.makedirs(base_path, exist_ok=True)
    file_path = os.path.join(base_path, f"{safe_name}{ext}")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code.strip())
    return file_path
