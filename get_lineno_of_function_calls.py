import ast


def extract_function_call_lines_from_code(code):
    """
    Extract function call names and their locations in the given Python code.

    This function analyzes the provided Python code as a string, parses it into an
    Abstract Syntax Tree (AST), and iterates through the tree to locate all
    function calls. Each function call's name and the corresponding line number
    are extracted and returned as a list of tuples. Function calls are identified
    only if they directly use identifiers (`id` attribute) and not complex call
    structures like attribute accesses.

    :param code: The Python source code to analyze, given as a string.
    :type code: str
    :return: A list of tuples, each containing the name of a called function and
        the line number where the call is made.
    :rtype: list[tuple[str, int]]
    """
    tree = ast.parse(code)
    function_calls = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and hasattr(node.func, 'id'):
            function_calls.append((node.func.id, node.lineno))

    return function_calls
