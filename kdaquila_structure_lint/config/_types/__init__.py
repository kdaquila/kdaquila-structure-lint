"""Configuration type definitions for structure-lint."""

from kdaquila_structure_lint.config._types.config import Config
from kdaquila_structure_lint.config._types.line_limits_config import LineLimitsConfig
from kdaquila_structure_lint.config._types.one_per_file_config import OnePerFileConfig
from kdaquila_structure_lint.config._types.structure_config import StructureConfig
from kdaquila_structure_lint.config._types.validator_toggles import ValidatorToggles

__all__ = [
    "Config",
    "LineLimitsConfig",
    "OnePerFileConfig",
    "StructureConfig",
    "ValidatorToggles",
]
