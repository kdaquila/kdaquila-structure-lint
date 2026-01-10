"""Configuration type definitions for structure-lint."""

from kdaquila_structure_lint.config.types.config import Config
from kdaquila_structure_lint.config.types.line_limits_config import LineLimitsConfig
from kdaquila_structure_lint.config.types.one_per_file_config import OnePerFileConfig
from kdaquila_structure_lint.config.types.structure_config import StructureConfig
from kdaquila_structure_lint.config.types.validator_toggles import ValidatorToggles

__all__ = [
    "Config",
    "LineLimitsConfig",
    "OnePerFileConfig",
    "StructureConfig",
    "ValidatorToggles",
]
