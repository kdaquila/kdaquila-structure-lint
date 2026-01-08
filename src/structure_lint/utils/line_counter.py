"""Counts and validates lines in files."""

from pathlib import Path


def count_file_lines(file_path: Path) -> int:
    """Count the number of lines in a file."""
    try:
        with open(file_path, encoding="utf-8") as f:
            return sum(1 for _ in f)
    except (OSError, UnicodeDecodeError):
        # Return -1 to indicate error
        return -1


def validate_file_lines(file_path: Path, max_lines: int) -> str | None:
    """Check if file exceeds line limit. Returns error message or None."""
    line_count = count_file_lines(file_path)

    if line_count == -1:
        return f"{file_path}: Error reading file"

    if line_count > max_lines:
        excess = line_count - max_lines
        return f"{file_path}: {line_count} lines (exceeds limit by {excess})"

    return None
