from fastapi import APIRouter, Request
from deploy_to_github import auto_push_to_github

router = APIRouter()

@router.post("/deploy-auto")
async def deploy_to_github(request: Request):
    data = await request.json()
    project = data["project"]
    commit_msg = data["commit_message"]
    repo_url = data["repo_url"]
    token = data["token"]

    result = auto_push_to_github(
        project_path=f"./projects/{project}",
        commit_message=commit_msg,
        github_repo_url=repo_url,
        token=token
    )
    return result
