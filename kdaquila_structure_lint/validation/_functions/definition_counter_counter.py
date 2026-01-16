"""Count top-level definitions in source files."""

import ast
from pathlib import Path


def count_top_level_definitions(file_path: Path) -> tuple[int, list[str]] | None:
    """Route to appropriate parser based on file extension.

    Returns (count, names) or None on error/unsupported file type.
    """
    suffix = file_path.suffix.lower()

    if suffix == ".py":
        return count_python_definitions(file_path)
    elif suffix in {".ts", ".tsx"}:
        from kdaquila_structure_lint.validation._functions.definition_counter_ts import (
            count_typescript_definitions,
        )

        return count_typescript_definitions(file_path)
    else:
        return None


def count_python_definitions(file_path: Path) -> tuple[int, list[str]] | None:
    """Count top-level functions and classes in Python files.

    Returns (count, names) or None on error.
    """
    try:
        with file_path.open(encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=str(file_path))
    except (OSError, SyntaxError, UnicodeDecodeError):
        return None

    definitions = []
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            definitions.append(node.name)

    return len(definitions), definitions
