import os

from extract_functions_from_file import extract_functions_from_file
from get_top_level_code import get_top_level_code


def main():
    repo_path = "test"
    functions = []
    main_file = ""
    candidate = []
    for root, _, files in os.walk(repo_path):
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
    print(top_level_code)
    print(functions)
    for function in functions:
        print(function)


if __name__ == "__main__":
    main()
