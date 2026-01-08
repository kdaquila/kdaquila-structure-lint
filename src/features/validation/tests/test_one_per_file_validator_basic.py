"""Basic tests for one-per-file validation."""


from features.validation.utils.validator_one_per_file import validate_one_per_file


class TestOnePerFileValidatorBasic:
    """Basic tests for validate_one_per_file function."""

    def test_files_with_single_definition_pass(self, minimal_config, python_file_factory):
        """Should pass when files have single definition."""
        config = minimal_config
        (config.project_root / "src").mkdir()

        # Create files with single definitions
        python_file_factory("src/func.py", "def hello():\n    pass\n", config.project_root)
        python_file_factory("src/cls.py", "class MyClass:\n    pass\n", config.project_root)

        exit_code = validate_one_per_file(config)
        assert exit_code == 0

    def test_file_with_multiple_functions_fails(self, minimal_config, python_file_factory):
        """Should fail when file has multiple functions."""
        config = minimal_config
        (config.project_root / "src").mkdir()

        content = """def func1():
    pass

def func2():
    pass
"""
        python_file_factory("src/multi.py", content, config.project_root)

        exit_code = validate_one_per_file(config)
        assert exit_code == 1

    def test_file_with_multiple_classes_fails(self, minimal_config, python_file_factory):
        """Should fail when file has multiple classes."""
        config = minimal_config
        (config.project_root / "src").mkdir()

        content = """class Class1:
    pass

class Class2:
    pass
"""
        python_file_factory("src/multi.py", content, config.project_root)

        exit_code = validate_one_per_file(config)
        assert exit_code == 1

    def test_file_with_function_and_class_fails(self, minimal_config, python_file_factory):
        """Should fail when file has both function and class."""
        config = minimal_config
        (config.project_root / "src").mkdir()

        content = """def my_func():
    pass

class MyClass:
    pass
"""
        python_file_factory("src/mixed.py", content, config.project_root)

        exit_code = validate_one_per_file(config)
        assert exit_code == 1

    def test_empty_file_passes(self, minimal_config, python_file_factory):
        """Should pass for empty files (0 definitions)."""
        config = minimal_config
        (config.project_root / "src").mkdir()

        python_file_factory("src/empty.py", "", config.project_root)

        exit_code = validate_one_per_file(config)
        assert exit_code == 0

    def test_file_with_only_imports_passes(self, minimal_config, python_file_factory):
        """Should pass for files with only imports (0 top-level definitions)."""
        config = minimal_config
        (config.project_root / "src").mkdir()

        content = """import os
import sys
from pathlib import Path
"""
        python_file_factory("src/imports.py", content, config.project_root)

        exit_code = validate_one_per_file(config)
        assert exit_code == 0

    def test_file_with_constants_and_function_passes(self, minimal_config, python_file_factory):
        """Should pass when file has constants plus one function (constants don't count)."""
        config = minimal_config
        (config.project_root / "src").mkdir()

        content = """MAX_SIZE = 100
DEFAULT_NAME = "test"

def process():
    pass
"""
        python_file_factory("src/module.py", content, config.project_root)

        exit_code = validate_one_per_file(config)
        assert exit_code == 0

    def test_async_function_counted(self, minimal_config, python_file_factory):
        """Should count async functions as definitions."""
        config = minimal_config
        (config.project_root / "src").mkdir()

        content = """async def async_func():
    pass

def sync_func():
    pass
"""
        python_file_factory("src/async.py", content, config.project_root)

        exit_code = validate_one_per_file(config)
        assert exit_code == 1
