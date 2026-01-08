"""Tests for configuration and path handling in line limits validation."""


from features.validation.utils.validator_line_limits import validate_line_limits


class TestLineLimitsValidatorConfig:
    """Tests for configuration and path handling."""

    def test_custom_search_paths(self, minimal_config, python_file_factory):
        """Should check custom search paths."""
        config = minimal_config
        config.line_limits.search_paths = ["lib", "app"]
        config.line_limits.max_lines = 5

        (config.project_root / "lib").mkdir()
        (config.project_root / "app").mkdir()

        # Create file in lib
        long_content = "\n".join([f"# Line {i}" for i in range(1, 10)])
        python_file_factory("lib/module.py", long_content, config.project_root)

        exit_code = validate_line_limits(config)
        assert exit_code == 1

    def test_missing_search_path(self, minimal_config, capsys):
        """Should warn about missing search paths and continue."""
        config = minimal_config
        config.line_limits.search_paths = ["nonexistent", "src"]

        # Create valid file in src
        (config.project_root / "src").mkdir()
        (config.project_root / "src" / "module.py").write_text("pass\n")

        exit_code = validate_line_limits(config)
        captured = capsys.readouterr()

        # Should warn about nonexistent
        assert "Warning" in captured.out or "not found" in captured.out
        # Should still succeed
        assert exit_code == 0

    def test_all_search_paths_missing(self, minimal_config, capsys):
        """Should handle all search paths missing gracefully."""
        config = minimal_config
        config.line_limits.search_paths = ["nonexistent1", "nonexistent2"]

        exit_code = validate_line_limits(config)
        captured = capsys.readouterr()

        # Should warn
        assert "Warning" in captured.out or "not found" in captured.out
        # Should succeed (no files to check)
        assert exit_code == 0

    def test_nested_directories(self, minimal_config, python_file_factory):
        """Should check files in nested directories."""
        config = minimal_config
        config.line_limits.max_lines = 5
        (config.project_root / "src" / "sub" / "deep").mkdir(parents=True)

        # Create file in nested directory
        long_content = "\n".join([f"# Line {i}" for i in range(1, 10)])
        python_file_factory("src/sub/deep/module.py", long_content, config.project_root)

        exit_code = validate_line_limits(config)
        assert exit_code == 1

    def test_excludes_venv_directory(self, minimal_config, python_file_factory):
        """Should exclude .venv and venv directories."""
        config = minimal_config
        config.line_limits.max_lines = 5

        (config.project_root / "src").mkdir()
        (config.project_root / "src" / ".venv").mkdir()
        (config.project_root / "src" / "venv").mkdir()

        # Create long files in excluded directories
        long_content = "\n".join([f"# Line {i}" for i in range(1, 100)])
        python_file_factory("src/.venv/lib.py", long_content, config.project_root)
        python_file_factory("src/venv/lib.py", long_content, config.project_root)

        # Should pass because excluded directories are ignored
        exit_code = validate_line_limits(config)
        assert exit_code == 0

    def test_excludes_pycache_directory(self, minimal_config, python_file_factory):
        """Should exclude __pycache__ directories."""
        config = minimal_config
        config.line_limits.max_lines = 5

        (config.project_root / "src" / "__pycache__").mkdir(parents=True)

        # Create long file in __pycache__
        long_content = "\n".join([f"# Line {i}" for i in range(1, 100)])
        python_file_factory("src/__pycache__/module.py", long_content, config.project_root)

        # Should pass because __pycache__ is excluded
        exit_code = validate_line_limits(config)
        assert exit_code == 0

    def test_excludes_git_directory(self, minimal_config, python_file_factory):
        """Should exclude .git directories."""
        config = minimal_config
        config.line_limits.max_lines = 5

        (config.project_root / "src" / ".git").mkdir(parents=True)

        # Create long file in .git
        long_content = "\n".join([f"# Line {i}" for i in range(1, 100)])
        python_file_factory("src/.git/hooks.py", long_content, config.project_root)

        # Should pass because .git is excluded
        exit_code = validate_line_limits(config)
        assert exit_code == 0

    def test_max_lines_configuration_respected(self, minimal_config, python_file_factory):
        """Should respect configured max_lines value."""
        config = minimal_config
        config.line_limits.max_lines = 3
        (config.project_root / "src").mkdir()

        # Create file with 4 lines
        python_file_factory("src/module.py", "line1\nline2\nline3\nline4\n", config.project_root)

        exit_code = validate_line_limits(config)
        assert exit_code == 1
