"""Tests for error handling and reporting in one-per-file validation."""


from features.validation.utils.validator_one_per_file import validate_one_per_file


class TestOnePerFileValidatorErrors:
    """Tests for error handling and reporting."""

    def test_syntax_error_reported_as_failure(self, minimal_config, python_file_factory, capsys):
        """Should report files with syntax errors."""
        config = minimal_config
        (config.project_root / "src").mkdir()

        # Create file with syntax error
        content = "def broken(\n    # Missing closing paren\n"
        python_file_factory("src/broken.py", content, config.project_root)

        exit_code = validate_one_per_file(config)
        captured = capsys.readouterr()

        # Should report error
        assert "Error parsing file" in captured.out or "broken.py" in captured.out
        assert exit_code == 1

    def test_error_messages_use_relative_paths(self, minimal_config, python_file_factory, capsys):
        """Should use relative paths in error messages."""
        config = minimal_config
        (config.project_root / "src").mkdir()

        # Create violating file
        content = "def func1():\n    pass\n\ndef func2():\n    pass\n"
        python_file_factory("src/multi.py", content, config.project_root)

        exit_code = validate_one_per_file(config)
        captured = capsys.readouterr()

        # Error message should use relative path
        assert (
            "src" in captured.out
            or "src\\multi.py" in captured.out
            or "src/multi.py" in captured.out
        )
        assert exit_code == 1

    def test_multiple_violations_all_reported(self, minimal_config, python_file_factory, capsys):
        """Should report all violations, not just first one."""
        config = minimal_config
        (config.project_root / "src").mkdir()

        # Create multiple violating files
        content = "def func1():\n    pass\n\ndef func2():\n    pass\n"
        python_file_factory("src/file1.py", content, config.project_root)
        python_file_factory("src/file2.py", content, config.project_root)
        python_file_factory("src/file3.py", content, config.project_root)

        exit_code = validate_one_per_file(config)
        captured = capsys.readouterr()

        # Should mention all files
        assert "file1.py" in captured.out
        assert "file2.py" in captured.out
        assert "file3.py" in captured.out
        assert exit_code == 1

    def test_error_message_shows_definition_names(
        self, minimal_config, python_file_factory, capsys
    ):
        """Should show names of definitions in error message."""
        config = minimal_config
        (config.project_root / "src").mkdir()

        content = """def hello():
    pass

def world():
    pass

class Greeting:
    pass
"""
        python_file_factory("src/multi.py", content, config.project_root)

        exit_code = validate_one_per_file(config)
        captured = capsys.readouterr()

        # Should mention definition names
        assert "hello" in captured.out
        assert "world" in captured.out
        assert "Greeting" in captured.out
        assert exit_code == 1

    def test_unicode_in_definition_names(self, minimal_config, python_file_factory):
        """Should handle Unicode in definition names."""
        config = minimal_config
        (config.project_root / "src").mkdir()

        # Python allows Unicode identifiers
        content = """def функция():
    pass

def 函数():
    pass
"""
        python_file_factory("src/unicode.py", content, config.project_root)

        exit_code = validate_one_per_file(config)
        assert exit_code == 1
