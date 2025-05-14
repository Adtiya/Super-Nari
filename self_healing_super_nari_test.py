
import requests
import json
import os

BASE_URL = "http://localhost:8000"
AGENT_PATH = "./agents"

def log_and_fix(agent_name, fix_text):
    print(f"[⚠️ FIXING] Agent: {agent_name}")
    agent_file = os.path.join(AGENT_PATH, f"{agent_name}.py")
    with open(agent_file, "w") as f:
        f.write(fix_text)
    print(f"[✅ FIXED] {agent_name}.py regenerated.")

def test_create_project():
    url = f"{BASE_URL}/agent/run"
    payload = {
        "user": "auto",
        "project": "auto_proj",
        "feature": "init",
        "agents": [],
        "methodology": "agile",
        "action": "add",
        "target": "flutter",
        "input_mode": "story"
    }
    try:
        res = requests.post(url, json=payload)
        print("\n[CREATE PROJECT]")
        print("Status:", res.status_code)
        print("Response:", res.json())
    except Exception as e:
        print("[ERROR] Create project failed:", e)

def test_build_feature_with_fix():
    url = f"{BASE_URL}/agent/run"
    payload = {
        "user": "auto",
        "project": "auto_proj",
        "feature": "automated login feature",
        "agents": ["planner", "dev", "test"],
        "methodology": "agile",
        "action": "add",
        "target": "flutter",
        "input_mode": "story"
    }

    print("\n[BUILD FEATURE]")
    try:
        res = requests.post(url, json=payload)
        print("Status:", res.status_code)
        data = res.json()
        print("Response:", data)

        # Fix missing or empty responses
        if 'plan' not in data or not data['plan']:
            log_and_fix("planner", 