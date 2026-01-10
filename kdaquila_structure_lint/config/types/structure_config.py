"""Structure validation configuration."""

from dataclasses import dataclass, field


@dataclass
class StructureConfig:
    """Configuration for structure validator."""

    folder_depth: int = 2
    standard_folders: set[str] = field(
        default_factory=lambda: {"types", "utils", "constants", "tests"}
    )
    prefix_separator: str = "_"
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
