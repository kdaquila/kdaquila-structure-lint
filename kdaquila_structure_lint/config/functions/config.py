"""Configuration loading and management for structure-lint.

This module re-exports everything from the config package for backward compatibility.
"""

from kdaquila_structure_lint.config.types import (
    Config,
    LineLimitsConfig,
    OnePerFileConfig,
    StructureConfig,
    ValidatorToggles,
)
from kdaquila_structure_lint.config.functions.loader import load_config
from kdaquila_structure_lint.config.functions.project_root import find_project_root

__all__ = [
    "Config",
    "LineLimitsConfig",
    "OnePerFileConfig",
    "StructureConfig",
    "ValidatorToggles",
    "find_project_root",
    "load_config",
]
