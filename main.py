import os

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from clone_repo import clone_repo
from extract_functions_from_file import extract_functions_from_file
from get_top_level_code import get_top_level_code
from typing import Dict
from fastapi import HTTPException

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/")
async def read_github_url(data: Dict[str, str]):
    """
    Asynchronously processes a dictionary containing a GitHub repository URL, validates the
    URL, clones the repository, extracts function definitions from Python files within the
    repository, and attempts to identify and analyze the main entry point file based on certain
    criteria.

    :param data: A dictionary containing a single key-value pair where the key is 'repoUrl' and
        the value is the GitHub repository URL to be processed.
    :type data: Dict[str, str]
    :return: A dictionary with two keys - 'topLevelCode', containing the top-level code
        extracted from the identified main file, and 'message', indicating the success of the
        operation.
    :rtype: Dict[str, str]
    :raises HTTPException: If 'repoUrl' is missing, is not a valid GitHub repository URL, or if
        any other issue arises during the processing of the repository.
    """
    try:
        repo_url = data.get("repoUrl")
        if not repo_url:
            raise HTTPException(status_code=400, detail="Repository URL is required")

        if not repo_url.startswith("https://github.com/"):
            raise HTTPException(status_code=400, detail="Invalid GitHub repository URL")

        await clone_repo(repo_url)
        functions = []
        main_file = ""
        candidate = []

        for root, _, files in os.walk("cloned_repo"):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    for function in extract_functions_from_file(file_path):
                        functions.append(function)
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()

                        if "__name__ == \"__main__\"" in content or "__name__ == '__main__'" in content:
                            main_file = file_path

                        if "main.py" in file or "app.py" in file or "run.py" in file:
                            candidate.append(file_path)
            if not main_file:
                main_file = candidate[0]

        top_level_code = get_top_level_code(main_file)

        return {"topLevelCode": top_level_code, "message": "Success"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
