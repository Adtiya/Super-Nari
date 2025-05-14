
def run_tests(data):
    feature = data.get("feature", "").replace(" ", "_").lower()
    return {"test": f"def test_{feature}():\n    assert True"}
