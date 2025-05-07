import os

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from clone_repo import clone_repo
from typing import Dict
from fastapi import HTTPException

from language_detection import detect_language
from python.get_main_file_and_functions import get_top_level_code_and_functions

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
    Processes a GitHub repository URL from the input payload, validates it, clones the
    repository, extracts Python functions, identifies the main entry point file, retrieves
    top-level code from the identified file, and returns the results.

    :param data: A dictionary containing the input data. The dictionary must include a key `repoUrl`
                 associated with a string value, which specifies the URL of a GitHub repository
                 to process.
    :type data: Dict[str, str]

    :return: A dictionary containing the top-level code extracted from the identified main file,
             a list of extracted Python functions, and a success message. Example structure of
             return value:
             {
                 "topLevelCode": "<extracted top level code>",
                 "message": "Success",
                 "functions": [list of extracted functions]
             }
    :rtype: Dict[str, Union[str, List[str]]]

    :raises HTTPException: If the `repoUrl` is missing or not a valid GitHub repository URL, it
                            raises an error with a 400 status. In the case of other exceptions, it
                            raises an error with a 500 status containing the exception detail.
    """
    try:
        repo_url = data.get("repoUrl")
        if not repo_url:
            raise HTTPException(status_code=400, detail="Repository URL is required")

        if not repo_url.startswith("https://github.com/"):
            raise HTTPException(status_code=400, detail="Invalid GitHub repository URL")

        await clone_repo(repo_url)
        repo_language = detect_language("cloned_repo")

        if repo_language == "Python":
                main_file, functions = get_top_level_code_and_functions()
                return {
                    "topLevelCode": main_file,
                    "functions": functions
                }
        return None

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
