"""Main configuration object."""

from dataclasses import dataclass
from pathlib import Path

from kdaquila_structure_lint.config.types.line_limits_config import LineLimitsConfig
from kdaquila_structure_lint.config.types.one_per_file_config import OnePerFileConfig
from kdaquila_structure_lint.config.types.structure_config import StructureConfig
from kdaquila_structure_lint.config.types.validator_toggles import ValidatorToggles


@dataclass
class Config:
    """Master configuration object."""
    enabled: bool
    project_root: Path
    search_paths: list[str]
    validators: ValidatorToggles
    line_limits: LineLimitsConfig
    one_per_file: OnePerFileConfig
    structure: StructureConfig
