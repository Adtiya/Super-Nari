
import requests
import subprocess
import time

# Backend Test for agent creation
def test_agent_creation():
    url = "http://localhost:8000/agent/run"
    payload = {
        "user": "test_user",
        "project": "test_project",
        "feature": "sample feature",
        "agents": ["planner", "dev", "test"],
        "methodology": "agile",
        "target": "python",
        "input_mode": "story"
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    print("Agent creation test passed")

# Backend Test for feature generation
def test_generate_features():
    url = "http://localhost:8000/asi/generate-features"
    payload = {
        "project": "test_project",
        "stack": "python",
        "methodology": "agile",
        "goal": "Build a smart agent",
        "features": "**Feature 1**\n**Feature 2**"
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    print("Feature generation test passed")

# Backend Test for agent export
def test_export_agent():
    url = "http://localhost:8000/agent/export"
    payload = {
        "project": "test_project",
        "feature": "sample feature"
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    print("Agent export test passed")

# Multi-runtime check for languages
def test_runtime_availability():
    languages = ["python", "node", "go", "bash", "swift", "java", "rust"]
    for lang in languages:
        result = subprocess.run([lang, "--version"], capture_output=True, text=True)
        assert result.returncode == 0
        print(f"{lang} runtime check passed")

# Frontend Test for agent creation (Using Flutter Driver)
def test_frontend_agent_creation():
    from flutter_driver import FlutterDriver
    driver = FlutterDriver.connect()

    # Submit a goal via ASI Dashboard and check for response
    goal_field = driver.find_element_by_value_key('goalField')
    generate_button = driver.find_element_by_value_key('generateAgentButton')
    output_text = driver.find_element_by_value_key('outputText')

    driver.enter_text(goal_field, 'Build a multi-agent system')
    driver.click(generate_button)
    driver.wait_for(output_text)

    output = driver.get_text(output_text)
    assert "Plan" in output and "Code" in output
    print("Frontend agent creation test passed")

# Run all tests
def run_tests():
    print("Starting backend tests...")
    test_agent_creation()
    test_generate_features()
    test_export_agent()
    test_runtime_availability()

    print("Starting frontend tests...")
    test_frontend_agent_creation()

    print("All tests passed!")

# Execute the tests
if __name__ == "__main__":
    run_tests()
