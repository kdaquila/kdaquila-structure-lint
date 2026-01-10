"""Validates that Python files contain at most one top-level function or class.

Encourages focused, single-responsibility modules.
"""

import sys

from kdaquila_structure_lint.config import Config
from kdaquila_structure_lint.validation.utils.definition_counter_validator import (
    validate_file_definitions,
)
from kdaquila_structure_lint.validation.utils.file_finder import find_python_files


def validate_one_per_file(config: Config) -> int:
    """Run validation and return exit code."""
    project_root = config.project_root
    search_paths = config.search_paths
    errors = []

    print("🔍 Checking for one function/class per file...\n")

    for search_path in search_paths:
        path = project_root / search_path
        if not path.exists():
            print(f"⚠️  Warning: {search_path}/ not found, skipping")
            continue

        print(f"  Scanning {search_path}/...")
        python_files = find_python_files(path)

        for file_path in python_files:
            # Make path relative to project root for cleaner error messages
            try:
                relative_path = file_path.relative_to(project_root)
            except ValueError:
                relative_path = file_path

            error = validate_file_definitions(file_path)
            if error:
                # Replace absolute path with relative path in error message
                error = error.replace(str(file_path), str(relative_path))
                errors.append(error)

    if errors:
        print(f"\n❌ Found {len(errors)} file(s) with multiple definitions:\n")
        for error in errors:
            print(f"  • {error}")
        print("\n💡 Consider splitting into separate files for better modularity.")
        return 1

    print("\n✅ All files have at most one top-level function or class!")
    return 0


if __name__ == "__main__":
    from kdaquila_structure_lint.config import load_config

    config = load_config()
    sys.exit(validate_one_per_file(config))
