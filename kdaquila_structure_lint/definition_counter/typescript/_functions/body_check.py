"""Check if a function has a body."""

from tree_sitter import Node


def _has_function_body(node: Node) -> bool:
    """Check if a function declaration has a body (not just an overload signature)."""
    for child in node.children:
        if child.type == "statement_block":
            return True
    return False
