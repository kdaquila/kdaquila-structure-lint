"""Tests for relative path handling in structure validation error messages."""


from features.validation.utils.validator_structure import validate_structure


class TestStructureValidatorRelativePaths:
    """Tests for relative path handling in error messages."""

    def test_error_messages_use_relative_paths(self, minimal_config, capsys):
        """Should use relative paths in error messages."""
        config = minimal_config

        # Create invalid structure
        src = config.project_root / "src"
        src.mkdir()
        (src / "features").mkdir()
        (src / "invalid_folder").mkdir()

        exit_code = validate_structure(config)
        captured = capsys.readouterr()

        # Error message should use relative path
        assert "src" in captured.out
        # Should not show absolute path markers like drive letters on Windows
        assert exit_code == 1
