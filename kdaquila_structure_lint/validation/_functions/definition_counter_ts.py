"""Count top-level definitions in TypeScript files using tree-sitter."""

from pathlib import Path

from tree_sitter import Language, Parser
from tree_sitter_typescript import language_tsx, language_typescript


def get_parser(file_path: Path) -> Parser:
    """Create a tree-sitter parser for the appropriate TypeScript dialect."""
    parser = Parser()
    if file_path.suffix.lower() == ".tsx":
        parser.language = Language(language_tsx())
    else:
        parser.language = Language(language_typescript())
    return parser


def _get_variable_name(node):  # type: ignore[no-untyped-def]
    """Extract variable name from a variable_declarator node."""
    for child in node.children:
        if child.type == "identifier":
            return child.text.decode("utf-8") if child.text else None
    return None


def _is_function_assignment(node):  # type: ignore[no-untyped-def]
    """Check if a variable_declarator assigns a function/arrow function."""
    for child in node.children:
        if child.type in {"arrow_function", "function_expression", "function"}:
            return True
    return False


def _has_function_body(node):  # type: ignore[no-untyped-def]
    """Check if a function declaration has a body (not just an overload signature)."""
    for child in node.children:
        if child.type == "statement_block":
            return True
    return False


def _extract_definitions_from_lexical_declaration(node):  # type: ignore[no-untyped-def]
    """Extract function definitions from const declarations.

    Only counts const declarations that assign arrow functions or function expressions.
    Does not count let/var assignments.
    """
    definitions = []

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


def _extract_definitions_from_export_statement(node):  # type: ignore[no-untyped-def]
    """Extract definitions from export statements.

    Handles:
    - export default function() {}
    - export default function name() {}
    - export default () => {}
    - export default class {}
    - export default class Name {}
    - export function name() {}
    - export class Name {}
    """
    definitions = []

    is_default = any(child.type == "default" for child in node.children)

    for child in node.children:
        if child.type == "function_declaration":
            if _has_function_body(child):
                name = None
                for subchild in child.children:
                    if subchild.type == "identifier":
                        name = subchild.text.decode("utf-8") if subchild.text else None
                        break
                definitions.append(name if name else "<default>")

        elif child.type == "class_declaration":
            name = None
            for subchild in child.children:
                if subchild.type == "type_identifier":
                    name = subchild.text.decode("utf-8") if subchild.text else None
                    break
            definitions.append(name if name else "<default>")

        elif child.type == "abstract_class_declaration":
            name = None
            for subchild in child.children:
                if subchild.type == "type_identifier":
                    name = subchild.text.decode("utf-8") if subchild.text else None
                    break
            definitions.append(name if name else "<default>")

        elif child.type in {"arrow_function", "function_expression", "function"} and is_default:
            # export default () => {} or export default function() {}
            definitions.append("<default>")

        elif child.type == "class" and is_default:
            # export default class {}
            definitions.append("<default>")

        elif child.type == "lexical_declaration":
            # export const foo = () => {}
            definitions.extend(_extract_definitions_from_lexical_declaration(child))

    return definitions


def count_typescript_definitions(file_path: Path) -> tuple[int, list[str]] | None:
    """Count top-level function and class definitions in TypeScript files.

    Counts:
    - function declarations (with bodies, not overload signatures)
    - async function declarations
    - class declarations
    - abstract class declarations
    - const assignments to arrow functions or function expressions
    - export default functions/classes (named or anonymous)

    Does not count:
    - type aliases, interfaces, enums, namespaces
    - let/var assignments
    - function overload signatures (no body)
    - functions inside objects or as callbacks

    Returns (count, names) or None on error.
    """
    try:
        content = file_path.read_bytes()
    except OSError:
        return None

    try:
        parser = get_parser(file_path)
        tree = parser.parse(content)
    except Exception:  # noqa: BLE001
        return None

    definitions: list[str] = []
    root = tree.root_node

    # Iterate over top-level nodes only
    for node in root.children:
        if node.type == "function_declaration":
            # Regular function or async function declaration
            if _has_function_body(node):
                for child in node.children:
                    if child.type == "identifier":
                        name = child.text.decode("utf-8") if child.text else None
                        if name:
                            definitions.append(name)
                        break

        elif node.type == "class_declaration":
            for child in node.children:
                if child.type == "type_identifier":
                    name = child.text.decode("utf-8") if child.text else None
                    if name:
                        definitions.append(name)
                    break

        elif node.type == "abstract_class_declaration":
            for child in node.children:
                if child.type == "type_identifier":
                    name = child.text.decode("utf-8") if child.text else None
                    if name:
                        definitions.append(name)
                    break

        elif node.type == "lexical_declaration":
            definitions.extend(_extract_definitions_from_lexical_declaration(node))

        elif node.type == "export_statement":
            definitions.extend(_extract_definitions_from_export_statement(node))

    return len(definitions), definitions
