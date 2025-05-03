import ast
import requests
import os

def extract_functions_from_filed(file_path):
    with open(file_path, "r") as f:
        source = f.read()
        tree = ast.parse(source, filename=file_path)

    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_source = ast.get_source_segment(source, node)
            functions.append((node.name, node.lineno, func_source))

    return functions


def get_top_level_code(file_path):
    with open(file_path, "r") as f:
        source = f.read()
        tree = ast.parse(source, filename=file_path)

    top_level_code = []
    for node in tree.body:
        if not isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            code_segment = ast.get_source_segment(source, node)
            if code_segment:
                top_level_code.append(code_segment)
    return top_level_code


def summarize_function_with_lmstudio(code):
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "any-name",  # can be anything, LM Studio ignores it
        "messages": [
            {"role": "user",
             "content": f"Summarize this Python function briefly and return only the summary nothing else:\n{code}"}
        ],
        "temperature": 0.7
    }

    response = requests.post("http://localhost:1234/v1/chat/completions", headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]




def find_main_file(repo_path):
    candidate_files = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    if "__name__ == \"__main__\"" in content or "__name__ == '__main__'" in content:
                        return file_path  # Strong match

                    # Collect weaker candidates (based on name)
                    if file in ("main.py", "app.py", "run.py"):
                        candidate_files.append(file_path)

    return candidate_files[0] if candidate_files else None

def main():
    main_file = find_main_file("test")
    functions = extract_functions_from_file(main_file)
    print(functions)
    for name, lineno, code in functions:
        summary = summarize_function_with_lmstudio(code)
        print(f"Function {name} at line {lineno}:")
        print(summary)
        print()
    print(get_top_level_code(main_file))

if __name__ == "__main__":
    main()