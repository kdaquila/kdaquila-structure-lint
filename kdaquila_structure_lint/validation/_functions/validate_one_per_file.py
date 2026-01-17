"""Validates that source files contain at most one top-level function or class.

Encourages focused, single-responsibility modules. Applies folder-aware rules
based on which standard folder the file is in.
"""

import sys

from kdaquila_structure_lint.config import Config
from kdaquila_structure_lint.definition_counter import count_top_level_definitions
from kdaquila_structure_lint.validation._functions.file_finder import find_source_files
from kdaquila_structure_lint.validation._functions.folder_detector import (
    get_standard_folder,
)
from kdaquila_structure_lint.validation._functions.validate_filename_matches_definition import (
    validate_filename_matches_definition,
)
from kdaquila_structure_lint.validation._functions.validator_one_per_file_exclusion import (
    is_excluded,
)
from kdaquila_structure_lint.validation._functions.validator_one_per_file_rule import (
    get_rule_for_file,
)


def validate_one_per_file(config: Config) -> int:
    """Run validation and return exit code."""
    project_root = config.project_root
    search_paths = config.search_paths
    standard_folders = config.structure.standard_folders
    excluded_patterns = config.one_per_file.excluded_patterns
    errors = []
    name_errors = []  # For filename mismatch errors

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
                construct_type = "classes" if folder in {"_classes"} else "functions"

                names_str = ", ".join(names)
                error = (
                    f"{relative_path}: {count} {construct_type} in {folder} folder "
                    f"(max 1): {names_str}"
                )
                errors.append(error)
            elif count == 1:
                name_error = validate_filename_matches_definition(file_path, names)
                if name_error:
                    name_errors.append(f"{relative_path}: {name_error}")

    errors_found = False

    if errors:
        errors_found = True
        print(f"\n❌ Found {len(errors)} file(s) with multiple definitions:\n")
        for error in errors:
            print(f"  • {error}")
        print("\n💡 Consider splitting into separate files for better modularity.")

    if name_errors:
        errors_found = True
        print(f"\n❌ Found {len(name_errors)} file(s) with mismatched filenames:\n")
        for error in name_errors:
            print(f"  • {error}")
        print("\n💡 Rename the file to match the definition, or vice versa.")

    if errors_found:
        return 1

    print("\n✅ All files have at most one top-level function or class!")
    return 0


if __name__ == "__main__":
    from kdaquila_structure_lint.config import load_config

    config = load_config()
    sys.exit(validate_one_per_file(config))
