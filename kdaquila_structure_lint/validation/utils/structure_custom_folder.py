"""Validates custom folder structure."""

from pathlib import Path

from kdaquila_structure_lint.config import Config
from kdaquila_structure_lint.validation.utils.pattern_match import matches_any_pattern


def validate_custom_folder(path: Path, config: Config, depth: int) -> list[str]:
    """Validate custom folder in structured base.

    This function validates folders according to three rules:
    1. Standard folders cannot contain subdirectories
    2. Feature folders must be prefixed with parent's name + separator (except at depth 0)
    3. Only certain files are allowed outside standard folders

    Args:
        path: The folder path to validate.
        config: The configuration object.
        depth: Current depth level (0 = direct child of base folder).

    Returns:
        List of error messages, empty if validation passes.
    """
    errors: list[str] = []

    # Check disallowed files (Rule 3)
    py_files = [c.name for c in path.iterdir() if c.is_file() and c.suffix == ".py"]
    disallowed = [f for f in py_files if f not in config.structure.files_allowed_anywhere]
    if disallowed:
        errors.append(f"{path}: Disallowed files: {disallowed}")

    # Get children (excluding ignored folders)
    children = [
        c
        for c in path.iterdir()
        if c.is_dir() and not matches_any_pattern(c.name, config.structure.ignored_folders)
    ]

    # Validate each child
    for child in children:
        if child.name in config.structure.standard_folders:
            # Standard folder: validate no subdirs (Rule 1)
            subdirs = [
                c
                for c in child.iterdir()
                if c.is_dir()
                and not matches_any_pattern(c.name, config.structure.ignored_folders)
            ]
            if subdirs:
                errors.append(f"{child}: Standard folder cannot have subdirectories")
        else:
            # Feature folder
            # Check prefix (Rule 2) - but exempt if depth == 0 (parent is base folder)
            if depth > 0:
                expected_prefix = path.name + config.structure.prefix_separator
                if not child.name.startswith(expected_prefix):
                    errors.append(
                        f"{child}: Feature folder must start with '{expected_prefix}'"
                    )

            # Check depth limit
            if depth >= config.structure.folder_depth:
                errors.append(
                    f"{child}: Exceeds max depth of {config.structure.folder_depth}"
                )
            else:
                errors.extend(validate_custom_folder(child, config, depth + 1))

    return errors
