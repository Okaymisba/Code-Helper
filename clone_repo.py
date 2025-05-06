import subprocess
import shutil
import os


async def clone_repo(repo_url):
    """
    Clones a git repository from the specified URL into a directory named
    'cloned_repo'. If the directory already exists, it will be deleted
    before cloning.

    :param repo_url: The URL of the git repository to clone.
    :type repo_url: str
    :return: None
    :rtype: NoneType
    :raises Exception: If the cloning process fails or an error occurs during
        execution.
    """
    try:
        if os.path.exists("cloned_repo"):
            shutil.rmtree("cloned_repo")

        clone_command = f"git clone {repo_url} cloned_repo"
        result = subprocess.run(clone_command.split(), capture_output=True, text=True)

        if result.returncode != 0:
            raise Exception(f"Failed to clone repository: {result.stderr}")

    except Exception as e:
        raise Exception(f"Error cloning repository: {str(e)}")
