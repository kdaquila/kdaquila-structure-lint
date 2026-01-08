"""Validates structured base folder (features)."""

from pathlib import Path

from features.config import Config
from features.validation.utils.structure.custom_folder import validate_custom_folder


def validate_base_folder(base_path: Path, config: Config) -> list[str]:
    """Validate features base folder structure."""
    errors: list[str] = []

    # Check for files in base folder (not allowed)
    files = [c.name for c in base_path.iterdir() if c.is_file()]
    if files:
        errors.append(f"{base_path}: Files not allowed in root: {files}")

    # Validate subdirectories
    for custom in base_path.iterdir():
        if custom.is_dir() and custom.name != "__pycache__":
            errors.extend(validate_custom_folder(custom, config, depth=1))
    return errors
