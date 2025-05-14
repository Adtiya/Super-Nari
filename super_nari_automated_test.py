
import requests
import json

BASE_URL = "http://localhost:8000"

def run_agent_test():
    print("▶️ Running /agent/run test...")
    payload = {
        "project_name": "TestProject",
        "feature_name": "AutoTestFeature",
        "prompt": "Write a Python function that adds two numbers.",
        "runtime": "python"
    }
    response = requests.post(f"{BASE_URL}/agent/run", json=payload)
    print("Status:", response.status_code)
    print("Response:", response.json())

def view_memory_test():
    print("\n📚 Running /memory/view test...")
    response = requests.get(f"{BASE_URL}/memory/view?project=TestProject")
    print("Status:", response.status_code)
    try:
        data = response.json()
        print("Features:", json.dumps(data.get("features", []), indent=2))
    except Exception as e:
        print("Failed to parse memory data:", e)

def annotate_memory_test():
    print("\n📝 Running /memory/annotate test...")
    payload = {
        "feature_name": "AutoTestFeature",
        "note": "This was auto-tested and works fine."
    }
    response = requests.post(f"{BASE_URL}/memory/annotate", json=payload)
    print("Status:", response.status_code)
    print("Response:", response.json())

def list_templates_test():
    print("\n📦 Running /templates/list test...")
    response = requests.get(f"{BASE_URL}/templates/list")
    print("Status:", response.status_code)
    try:
        templates = response.json()
        for t in templates:
            print("-", t["title"])
    except Exception as e:
        print("Error:", e)

def use_template_test():
    print("\n🧠 Running /templates/use test...")
    payload = {
        "project_name": "TemplateTestProject",
        "feature_name": "SummarizerTest",
        "prompt": "Summarize the following text: 'Flutter is great.'",
        "runtime": "python"
    }
    response = requests.post(f"{BASE_URL}/templates/use", json=payload)
    print("Status:", response.status_code)
    print("Response:", response.json())

if __name__ == "__main__":
    run_agent_test()
    view_memory_test()
    annotate_memory_test()
    list_templates_test()
    use_template_test()
