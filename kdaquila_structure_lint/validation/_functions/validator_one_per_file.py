"""Validates that source files contain at most one top-level function or class.

Encourages focused, single-responsibility modules. Applies folder-aware rules
based on which standard folder the file is in.
"""

import sys
from fnmatch import fnmatch
from pathlib import Path

from kdaquila_structure_lint.config import Config
from kdaquila_structure_lint.validation._functions.definition_counter_counter import (
    count_top_level_definitions,
)
from kdaquila_structure_lint.validation._functions.file_finder import find_source_files
from kdaquila_structure_lint.validation._functions.folder_detector import (
    get_standard_folder,
)


def get_rule_for_file(file_path: Path, folder: str | None, config: Config) -> bool | None:
    """
    Get the applicable rule for a file based on its folder and language.

    Returns True if rule is enabled, False if disabled, None if no rule applies.
    """
    if folder is None:
        return None  # File not in a standard folder - no validation

    lang = "ts" if file_path.suffix in {".ts", ".tsx"} else "py"

    # Map folder to rule
    rule_map = {
        ("ts", "_functions"): config.one_per_file.ts_fun_in_functions,
        ("ts", "_components"): config.one_per_file.ts_fun_in_components,
        ("ts", "_hooks"): config.one_per_file.ts_fun_in_hooks,
        ("ts", "_classes"): config.one_per_file.ts_cls_in_classes,
        ("py", "_functions"): config.one_per_file.py_fun_in_functions,
        ("py", "_classes"): config.one_per_file.py_cls_in_classes,
    }

    return rule_map.get((lang, folder))  # Returns None for _types, _constants, etc.


def is_excluded(file_path: Path, excluded_patterns: list[str]) -> bool:
    """Check if file matches any excluded pattern."""
    file_name = file_path.name
    for pattern in excluded_patterns:
        if fnmatch(file_name, pattern):
            return True
    return False


def validate_one_per_file(config: Config) -> int:
    """Run validation and return exit code."""
    project_root = config.project_root
    search_paths = config.search_paths
    standard_folders = config.structure.standard_folders
    excluded_patterns = config.one_per_file.excluded_patterns
    errors = []

    print("🔍 Checking for one function/class per file...\n")

    for search_path in search_paths:
        path = project_root / search_path
        if not path.exists():
            print(f"⚠️  Warning: {search_path}/ not found, skipping")
            continue

        print(f"  Scanning {search_path}/...")
        source_files = find_source_files(path)

        for file_path in source_files:
            # Make path relative to project root for cleaner error messages
            try:
                relative_path = file_path.relative_to(project_root)
            except ValueError:
                relative_path = file_path

            # Check if file is excluded
            if is_excluded(file_path, excluded_patterns):
                continue

            # Detect which standard folder the file is in
            folder = get_standard_folder(file_path, standard_folders)

            # Get the applicable rule for this file
            rule = get_rule_for_file(file_path, folder, config)

            # Skip if no rule applies (file not in a standard folder or folder has no rule)
            if rule is None:
                continue

            # Skip if rule is disabled
            if not rule:
                continue

            # Count definitions and validate
            result = count_top_level_definitions(file_path)

            if result is None:
                errors.append(f"{relative_path}: Error parsing file")
                continue

            count, names = result
            if count > 1:
                # Determine construct type based on folder
                if folder in {"_classes"}:
                    construct_type = "classes"
                else:
                    construct_type = "functions"

                error = f"{relative_path}: {count} {construct_type} in {folder} folder (max 1): {', '.join(names)}"
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
