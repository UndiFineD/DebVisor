import ast

file_path = "opt/monitoring/enhanced.py"


def check_type_hints(func: ast.FunctionDef) -> None:
    has_return = func.returns is not None
    args = func.args.args
    if not args:
        has_args = True
    else:
        missing_arg_annotation = False
        for arg in args:
            if arg.arg in ('sel', 'cls'):
                continue
            if arg.annotation is None:
                missing_arg_annotation = True
                break
        has_args = not missing_arg_annotation
    return has_args, has_return


with open(file_path, "r", encoding="utf-8") as f:
    tree = ast.parse(f.read(), filename=file_path)

functions = []
for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef):
        functions.append(node)

print(f"Found {len(functions)} functions")
for func in functions:
    has_args, has_return = check_type_hints(func)
    print(f"Function: {func.name}, Args: {has_args}, Return: {has_return}")
