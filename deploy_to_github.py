
import os
import subprocess

def auto_push_to_github(project_path, commit_message, github_repo_url, branch="main", token=None):
    token = token or os.getenv("GITHUB_TOKEN")
    if not token:
        raise Exception("GitHub token is required")

    # Convert to absolute path and ensure directory exists
    project_path = os.path.abspath(project_path)
    if not os.path.exists(project_path):
        os.makedirs(project_path)
        print(f"📁 Created missing project directory: {project_path}")

    print(f"📁 Using project path: {project_path}")

    # Prepare secure repo URL with token
    secure_url = github_repo_url.replace("https://", f"https://{token}@")

    try:
        if not os.path.exists(os.path.join(project_path, ".git")):
            subprocess.run(["git", "init"], cwd=project_path, check=True)
            subprocess.run(["git", "remote", "add", "origin", secure_url], cwd=project_path, check=True)

        subprocess.run(["git", "add", "."], cwd=project_path, check=True)
        subprocess.run(["git", "commit", "-m", commit_message], cwd=project_path, check=True)
        subprocess.run(["git", "branch", "-M", branch], cwd=project_path, check=True)
        subprocess.run(["git", "push", "-u", "origin", branch], cwd=project_path, check=True)

        return {"status": "success", "message": "Code pushed to GitHub."}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": f"Git command failed: {e}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
