"""Counts and validates top-level definitions in files."""

import ast
from pathlib import Path


def count_top_level_definitions(file_path: Path) -> tuple[int, list[str]] | None:
    """Count top-level functions and classes. Returns (count, names) or None on error."""
    try:
        with open(file_path, encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=str(file_path))
    except (OSError, SyntaxError, UnicodeDecodeError):
        return None

    definitions = []
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            definitions.append(node.name)

    return len(definitions), definitions


def validate_file_definitions(file_path: Path) -> str | None:
    """Check if file has more than one top-level definition. Returns error or None."""
    result = count_top_level_definitions(file_path)

    if result is None:
        return f"{file_path}: Error parsing file"

    count, names = result
    if count > 1:
        return f"{file_path}: {count} definitions (expected ≤1): {', '.join(names)}"

    return None
