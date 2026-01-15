"""Configuration types for structure-lint."""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Config:
    """Master configuration for structure-lint."""

    @dataclass
    class Validators:
        """Control which validators are enabled."""
        structure: bool = False      # Opt-in (too opinionated)
        line_limits: bool = True     # Enabled by default
        one_per_file: bool = True    # Enabled by default

    @dataclass
    class LineLimits:
        """Configuration for line limits validator."""
        max_lines: int = 150

    @dataclass
    class OnePerFile:
        """Configuration for one-per-file validator.

        Currently empty - reserved for future one_per_file specific settings.
        """
        pass  # Placeholder for future options

    @dataclass
    class Structure:
        """Configuration for structure validator."""
        folder_depth: int = 2
        standard_folders: set[str] = field(
            default_factory=lambda: {
                "_types", "_functions", "_constants", "_tests", "_errors", "_classes"
            }
        )
        files_allowed_anywhere: set[str] = field(default_factory=lambda: {"__init__.py"})
        ignored_folders: set[str] = field(
            default_factory=lambda: {
                "__pycache__",
                ".mypy_cache",
                ".pytest_cache",
                ".ruff_cache",
                ".hypothesis",
                ".tox",
                ".coverage",
                "*.egg-info",  # matches any .egg-info directory
            }
        )

    # Instance fields
    enabled: bool = True
    project_root: Path = field(default_factory=Path.cwd)
    search_paths: list[str] = field(default_factory=lambda: ["src"])
    validators: Validators = field(default_factory=Validators)
    line_limits: LineLimits = field(default_factory=LineLimits)
    one_per_file: OnePerFile = field(default_factory=OnePerFile)
    structure: Structure = field(default_factory=Structure)
