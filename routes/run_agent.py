from fastapi import APIRouter, Request
from utils.flutter_feature_formatter import save_flutter_feature
from utils.agent_logic_saver import save_agent_logic
from utils.code_generator import generate_code
from firebase_utils import save_feature_to_firestore, upload_agent_file
from datetime import datetime

router = APIRouter()

@router.post("/run")
async def run_agents(request: Request):
    try:
        body = await request.json()
        project = body.get("project")
        feature = body.get("feature")
        agents = body.get("agents", [])
        methodology = body.get("methodology")
        target = body.get("target", "python")
        input_mode = body.get("input_mode")
        screen_code = body.get("screen_code")
        test_code = body.get("test_code", f"// Test for: {feature}")

        if not (project and feature):
            return {"status": "error", "message": "Missing required fields 'project' or 'feature'"}

        # Generate code if not supplied
        if not screen_code:
            screen_code = generate_code(feature, target)

        # Save Flutter UI + logic files locally
        save_flutter_feature(project, feature, screen_code, test_code)
        logic_path = save_agent_logic(project, feature, screen_code, target)

        # Save feature metadata to Firestore
        save_feature_to_firestore(project, {
            "feature_name": feature,
            "prompt": feature,  # reusing feature name as prompt
            "code": screen_code,
            "created_at": datetime.utcnow().isoformat(),
            "status": "success"
        })

        # Upload agent code to Cloud Storage
        upload_agent_file(project, f"{feature}.py", screen_code)

        return {
            "status": "success",
            "project": project,
            "feature": feature,
            "generated_code": screen_code[:1000],
            "saved_logic_path": logic_path,
            "agents": agents,
            "methodology": methodology,
            "target": target,
            "input_mode": input_mode
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
