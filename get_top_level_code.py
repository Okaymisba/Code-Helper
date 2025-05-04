import ast


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