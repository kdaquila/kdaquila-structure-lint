"""Configuration loading and management for structure-lint.

This module re-exports everything from the config package for backward compatibility.
"""

from features.config.types import (
    Config,
    ValidatorToggles,
    LineLimitsConfig,
    OnePerFileConfig,
    StructureConfig,
)
from features.config.utils.project_root import find_project_root
from features.config.utils.loader import load_config

__all__ = [
    "Config",
    "ValidatorToggles",
    "LineLimitsConfig",
    "OnePerFileConfig",
    "StructureConfig",
    "find_project_root",
    "load_config",
]
