"""Tests for custom structure configuration."""

from pathlib import Path

from _pytest.capture import CaptureFixture

from kdaquila_structure_lint.test_fixtures import build_structure, create_minimal_config
from kdaquila_structure_lint.validation.utils.validator_structure import validate_structure


class TestStructureValidatorCustomConfig:
    """Tests for custom structure configuration."""

    def test_custom_strict_format_roots(self, tmp_path: Path) -> None:
        """Should use custom strict_format_roots."""
        config = create_minimal_config(tmp_path)
        config.structure.strict_format_roots = {"lib"}

        build_structure(
            tmp_path,
            {
                "lib": {
                    "features": {
                        "my_feature": {
                            "types": {"module.py": ""},
                        },
                    },
                },
            },
        )

        exit_code = validate_structure(config)
        assert exit_code == 0

    def test_multiple_strict_format_roots(
        self, tmp_path: Path, capsys: CaptureFixture[str]
    ) -> None:
        """Should validate multiple strict_format_roots."""
        config = create_minimal_config(tmp_path)
        config.structure.strict_format_roots = {"src", "lib"}

        build_structure(
            tmp_path,
            {
                "src": {
                    "features": {
                        "my_feature": {
                            "types": {"module.py": ""},
                        },
                    },
                },
                "lib": {
                    "features": {
                        "my_feature": {
                            "types": {"module.py": ""},
                        },
                    },
                },
            },
        )

        exit_code = validate_structure(config)
        captured = capsys.readouterr()

        # Both roots should be validated
        assert "Validating src/" in captured.out
        assert "Validating lib/" in captured.out
        assert exit_code == 0

    def test_empty_strict_format_roots_fails(
        self, tmp_path: Path, capsys: CaptureFixture[str]
    ) -> None:
        """Should fail when strict_format_roots is empty."""
        config = create_minimal_config(tmp_path)
        config.structure.strict_format_roots = set()

        exit_code = validate_structure(config)
        captured = capsys.readouterr()

        assert "strict_format_roots is empty" in captured.out
        assert exit_code == 1

    def test_custom_files_allowed_anywhere(self, tmp_path: Path) -> None:
        """Should allow custom files like py.typed via files_allowed_anywhere."""
        config = create_minimal_config(tmp_path)
        config.structure.files_allowed_anywhere = {"__init__.py", "py.typed"}

        build_structure(
            tmp_path,
            {
                "src": {
                    "features": {
                        "my_feature": {
                            "types": {"module.py": ""},
                            "py.typed": "",  # Custom allowed file - should be allowed
                        },
                    },
                },
            },
        )

        exit_code = validate_structure(config)
        assert exit_code == 0

    def test_custom_ignored_folders(self, tmp_path: Path) -> None:
        """Should ignore custom folders like .venv, build via ignored_folders."""
        config = create_minimal_config(tmp_path)
        config.structure.ignored_folders = {
            "__pycache__",
            ".venv",
            "build",
            ".egg-info",
        }

        build_structure(
            tmp_path,
            {
                "src": {
                    "features": {
                        "my_feature": {
                            "types": {"module.py": ""},
                            ".venv": {  # Ignored directories
                                "lib": {},
                            },
                            "build": {
                                "output.txt": "",
                            },
                        },
                    },
                },
            },
        )

        exit_code = validate_structure(config)
        assert exit_code == 0
