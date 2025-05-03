import ast


def extract_functions_from_file(file_path):
    with open(file_path, "r") as f:
        source = f.read()
        tree = ast.parse(source, filename=file_path)

    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_source = ast.get_source_segment(source, node)
            functions.append(
                dict(name=node.name, lineno=node.lineno, source=func_source, args=[arg.arg for arg in node.args.args]
                     , filename=file_path))

    return functions
