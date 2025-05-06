import ast


def get_top_level_code(file_path):
    """
    Extracts and returns the top-level executable code (not part of any function or
    class definition) from the Python source file at the specified file path.

    The function parses the input file using the Abstract Syntax Tree (AST) module
    to identify and ignore function or class definitions. It then collects
    top-level code and ensures that blank lines between the sections of the parsed
    code are also included.

    :param file_path: Path to the Python source file to analyze
    :type file_path: str
    :return: A string containing the top-level executable Python code present in
             the source file
    :rtype: str
    """
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
