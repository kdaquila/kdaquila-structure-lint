"""Tests for config dataclass defaults."""

from kdaquila_structure_lint.config import (
    LineLimitsConfig,
    StructureConfig,
    ValidatorToggles,
)


class TestConfigDataclasses:
    """Tests for config dataclass defaults."""

    def test_validator_toggles_defaults(self) -> None:
        """Should have correct default values."""
        toggles = ValidatorToggles()
        assert toggles.structure is False
        assert toggles.line_limits is True
        assert toggles.one_per_file is True

    def test_line_limits_config_defaults(self) -> None:
        """Should have correct default values."""
        config = LineLimitsConfig()
        assert config.max_lines == 150

    def test_structure_config_defaults(self) -> None:
        """Should have correct default values."""
        config = StructureConfig()
        assert config.folder_depth == 2
        assert config.standard_folders == {"types", "utils", "constants", "tests"}
        assert config.prefix_separator == "_"
        assert config.files_allowed_anywhere == {"__init__.py"}
        assert config.ignored_folders == {
            "__pycache__",
            ".mypy_cache",
            ".pytest_cache",
            ".ruff_cache",
            ".hypothesis",
            ".tox",
            ".coverage",
            "*.egg-info",
        }
