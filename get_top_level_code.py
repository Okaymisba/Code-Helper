import ast


def get_top_level_code(file_path):
    with open(file_path, "r") as f:
        source = f.read()
        tree = ast.parse(source, filename=file_path)

    top_level_code = []
    last_end_lineno = 0

    for node in tree.body:
        if not isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
            start_lineno = node.lineno

            if last_end_lineno > 0:
                blank_lines = source.splitlines()[last_end_lineno:start_lineno - 1]
                top_level_code.extend(blank_lines)

            code_segment = ast.get_source_segment(source, node)
            if code_segment:
                top_level_code.append(code_segment)

            last_end_lineno = node.end_lineno

    return "\n".join(top_level_code)
