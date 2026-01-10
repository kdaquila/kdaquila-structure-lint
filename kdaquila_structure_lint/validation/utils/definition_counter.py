"""Counts and validates top-level definitions in files.

This module re-exports everything from the definition_counter modules for backward compatibility.
"""

from kdaquila_structure_lint.validation.utils.definition_counter_counter import (
    count_top_level_definitions,
)
from kdaquila_structure_lint.validation.utils.definition_counter_validator import (
    validate_file_definitions,
)

__all__ = [
    "count_top_level_definitions",
    "validate_file_definitions",
]
