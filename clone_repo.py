import subprocess
import shutil
import os


async def clone_repo(repo_url):
    try:
        if os.path.exists("cloned_repo"):
            shutil.rmtree("cloned_repo")

        clone_command = f"git clone {repo_url} cloned_repo"
        result = subprocess.run(clone_command.split(), capture_output=True, text=True)

        if result.returncode != 0:
            raise Exception(f"Failed to clone repository: {result.stderr}")

    except Exception as e:
        raise Exception(f"Error cloning repository: {str(e)}")
