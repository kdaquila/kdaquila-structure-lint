"""Helper function for creating a Config object with custom settings."""

from pathlib import Path

from kdaquila_structure_lint.config import (
    Config,
    LineLimitsConfig,
    OnePerFileConfig,
    StructureConfig,
    ValidatorToggles,
)


def create_custom_config(tmp_path: Path) -> Config:
    """Create a Config object with custom settings.

    Args:
        tmp_path: The temporary path to use as project root.

    Returns:
        A Config object with custom validator and path settings.
    """
    return Config(
        enabled=True,
        project_root=tmp_path,
        search_paths=["src", "lib"],
        validators=ValidatorToggles(
            structure=True,
            line_limits=True,
            one_per_file=True,
        ),
        line_limits=LineLimitsConfig(
            max_lines=100,
        ),
        one_per_file=OnePerFileConfig(),
        structure=StructureConfig(
            folder_depth=3,
            standard_folders={"types", "utils", "helpers"},
            prefix_separator="_",
            files_allowed_anywhere={"README.md", "NOTES.md"},
        ),
    )
