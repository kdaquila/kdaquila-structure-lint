"""Extract definitions from lexical declarations."""

from tree_sitter import Node

from kdaquila_structure_lint.definition_counter.typescript._functions.function_check import (
    _is_function_assignment,
)
from kdaquila_structure_lint.definition_counter.typescript._functions.variable_name import (
    _get_variable_name,
)


def _extract_definitions_from_lexical_declaration(node: Node) -> list[str]:
    """Extract function definitions from const declarations.

    Only counts const declarations that assign arrow functions or function expressions.
    Does not count let/var assignments.
    """
    definitions: list[str] = []

    # Check if this is a const declaration
    is_const = False
    for child in node.children:
        if child.type == "const":
            is_const = True
            break

    if not is_const:
        return definitions

    # Look for variable_declarator children
    for child in node.children:
        if child.type == "variable_declarator":
            if _is_function_assignment(child):
                name = _get_variable_name(child)
                if name:
                    definitions.append(name)

    return definitions
