
def plan(data):
    feature = data.get("feature", "")
    return {"plan": f"Plan for {feature}\n1. Parse the feature.\n2. Define components.\n3. Code.\n4. Test."}
