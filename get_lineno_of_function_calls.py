import ast

from get_top_level_code import get_top_level_code


def extract_function_call_lines_from_code(code):
    tree = ast.parse(code)
    function_calls = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and hasattr(node.func, 'id'):
            function_calls.append((node.func.id, node.lineno))

    return function_calls
