"""Detect extra top-level definitions in Python files."""

import ast
from pathlib import Path


def _is_dunder_name(name: str) -> bool:
    """Check if name is a dunder (e.g., __all__, __version__)."""
    return name.startswith("__") and name.endswith("__")


def _is_type_checking_guard(node: ast.If) -> bool:
    """Check if an If node is a TYPE_CHECKING guard."""
    test = node.test
    # Handle: if TYPE_CHECKING:
    if isinstance(test, ast.Name) and test.id == "TYPE_CHECKING":
        return True
    # Handle: if typing.TYPE_CHECKING:
    return isinstance(test, ast.Attribute) and test.attr == "TYPE_CHECKING"


def _is_main_guard(node: ast.If) -> bool:
    """Check if an If node is an if __name__ == '__main__': guard."""
    test = node.test
    if not isinstance(test, ast.Compare):
        return False
    if len(test.ops) != 1 or not isinstance(test.ops[0], ast.Eq):
        return False
    if len(test.comparators) != 1:
        return False

    # Check for __name__ == "__main__" or "__main__" == __name__
    left = test.left
    right = test.comparators[0]

    def is_name_dunder(n: ast.expr) -> bool:
        return isinstance(n, ast.Name) and n.id == "__name__"

    def is_main_str(n: ast.expr) -> bool:
        return isinstance(n, ast.Constant) and n.value == "__main__"

    return (is_name_dunder(left) and is_main_str(right)) or (
        is_main_str(left) and is_name_dunder(right)
    )


def _get_assigned_names(node: ast.Assign | ast.AnnAssign) -> list[str]:
    """Extract assigned variable names from an assignment node."""
    names: list[str] = []

    if isinstance(node, ast.AnnAssign):
        # Annotated assignment: x: int = 5
        if isinstance(node.target, ast.Name):
            names.append(node.target.id)
    else:
        # Regular assignment: x = 5 or x, y = 1, 2
        for target in node.targets:
            if isinstance(target, ast.Name):
                names.append(target.id)
            elif isinstance(target, ast.Tuple | ast.List):
                for elt in target.elts:
                    if isinstance(elt, ast.Name):
                        names.append(elt.id)

    return names


def detect_python_extra_definitions(file_path: Path) -> list[str] | None:
    """Detect extra top-level definitions that aren't functions/classes.

    Returns list of extra definition names, or None on parse error.
    """
    try:
        with file_path.open(encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=str(file_path))
    except (OSError, SyntaxError, UnicodeDecodeError):
        return None

    extras: list[str] = []

    for node in ast.iter_child_nodes(tree):
        # Skip imports
        if isinstance(node, ast.Import | ast.ImportFrom):
            continue

        # Skip function and class definitions
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            continue

        # Skip TYPE_CHECKING and __name__ == "__main__" guards
        if isinstance(node, ast.If) and (_is_type_checking_guard(node) or _is_main_guard(node)):
            continue

        # Check assignments for extra definitions
        if isinstance(node, ast.Assign | ast.AnnAssign):
            names = _get_assigned_names(node)
            for name in names:
                # Allow dunder names like __all__, __version__
                if not _is_dunder_name(name):
                    extras.append(name)

    return extras
