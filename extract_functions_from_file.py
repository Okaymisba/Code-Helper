import ast


def extract_functions_from_file(file_path):
    """
    Extracts all function definitions from a given Python source file, including their
    names, line numbers, source code, arguments, and the file path.

    :param file_path: The path to the Python source file from which functions will
        be extracted.
    :type file_path: str
    :return: A list of dictionaries, each containing information about a function
        extracted from the file. Each dictionary includes the function name, line
        number, source code, arguments, and file path of the function.
    :rtype: list
    """
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
