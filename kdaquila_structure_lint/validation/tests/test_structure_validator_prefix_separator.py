"""Tests for prefix separator configuration."""

from pathlib import Path

from _pytest.capture import CaptureFixture

from kdaquila_structure_lint.test_fixtures import build_structure, create_minimal_config
from kdaquila_structure_lint.validation.utils.validator_structure import validate_structure


class TestPrefixSeparatorConfiguration:
    """Tests for prefix separator configuration options."""

    def test_prefix_separator_configuration(self, tmp_path: Path) -> None:
        """Custom prefix separator should be used for validation."""
        config = create_minimal_config(tmp_path)
        config.structure.prefix_separator = "-"

        build_structure(
            tmp_path,
            {
                "src": {
                    "features": {
                        "auth": {
                            "auth-login": {  # Using dash separator
                                "types": {"user.py": "# user types"},
                            },
                        },
                    },
                },
            },
        )

        exit_code = validate_structure(config)
        assert exit_code == 0

    def test_wrong_separator_fails(
        self, tmp_path: Path, capsys: CaptureFixture[str]
    ) -> None:
        """Using wrong separator should fail validation."""
        config = create_minimal_config(tmp_path)
        config.structure.prefix_separator = "-"

        build_structure(
            tmp_path,
            {
                "src": {
                    "features": {
                        "auth": {
                            "auth_login": {  # Using underscore but config expects dash
                                "types": {"user.py": "# user types"},
                            },
                        },
                    },
                },
            },
        )

        exit_code = validate_structure(config)
        captured = capsys.readouterr()

        assert exit_code == 1
        assert "Feature folder must start with 'auth-'" in captured.out

    def test_empty_separator_valid(self, tmp_path: Path) -> None:
        """Empty separator should work (direct concatenation)."""
        config = create_minimal_config(tmp_path)
        config.structure.prefix_separator = ""

        build_structure(
            tmp_path,
            {
                "src": {
                    "features": {
                        "auth": {
                            "authlogin": {  # No separator
                                "types": {"user.py": "# user types"},
                            },
                        },
                    },
                },
            },
        )

        exit_code = validate_structure(config)
        assert exit_code == 0

    def test_multi_character_separator(self, tmp_path: Path) -> None:
        """Multi-character separator should work."""
        config = create_minimal_config(tmp_path)
        config.structure.prefix_separator = "__"

        build_structure(
            tmp_path,
            {
                "src": {
                    "features": {
                        "auth": {
                            "auth__login": {  # Double underscore separator
                                "types": {"user.py": "# user types"},
                            },
                        },
                    },
                },
            },
        )

        exit_code = validate_structure(config)
        assert exit_code == 0
