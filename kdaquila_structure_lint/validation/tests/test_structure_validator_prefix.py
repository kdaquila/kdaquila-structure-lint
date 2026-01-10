"""Tests for feature folder prefix naming validation."""

from pathlib import Path

from _pytest.capture import CaptureFixture

from kdaquila_structure_lint.test_fixtures import build_structure, create_minimal_config
from kdaquila_structure_lint.validation.utils.validator_structure import validate_structure


class TestPrefixValidation:
    """Tests for feature folder prefix naming rules."""

    def test_valid_prefix_passes(self, tmp_path: Path) -> None:
        """Feature folder with correct prefix should pass."""
        config = create_minimal_config(tmp_path)

        build_structure(
            tmp_path,
            {
                "src": {
                    "features": {
                        "auth": {
                            "auth_login": {
                                "types": {"user.py": "# user types"},
                            },
                            "auth_logout": {
                                "utils": {"helper.py": "# helper"},
                            },
                        },
                    },
                },
            },
        )

        exit_code = validate_structure(config)
        assert exit_code == 0

    def test_invalid_prefix_fails(
        self, tmp_path: Path, capsys: CaptureFixture[str]
    ) -> None:
        """Feature folder without correct prefix should fail."""
        config = create_minimal_config(tmp_path)

        build_structure(
            tmp_path,
            {
                "src": {
                    "features": {
                        "auth": {
                            "login": {  # Should be auth_login
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
        assert "Feature folder must start with 'auth_'" in captured.out

    def test_root_folder_children_exempt_from_prefix(self, tmp_path: Path) -> None:
        """Children of base folders (depth 0) are exempt from prefix rule."""
        config = create_minimal_config(tmp_path)

        build_structure(
            tmp_path,
            {
                "src": {
                    "features": {
                        # These are at depth 0, so no prefix required
                        "auth": {
                            "types": {"user.py": "# user types"},
                        },
                        "payments": {
                            "utils": {"helper.py": "# helper"},
                        },
                        "reports": {
                            "constants": {"config.py": "# config"},
                        },
                    },
                },
            },
        )

        exit_code = validate_structure(config)
        assert exit_code == 0

    def test_standard_and_feature_folders_coexist(self, tmp_path: Path) -> None:
        """Standard folders and feature folders can coexist at the same level."""
        config = create_minimal_config(tmp_path)

        build_structure(
            tmp_path,
            {
                "src": {
                    "features": {
                        "auth": {
                            # Standard folders
                            "types": {"user.py": "# user types"},
                            "utils": {"helper.py": "# helper"},
                            # Feature folder with correct prefix
                            "auth_oauth": {
                                "types": {"token.py": "# token types"},
                            },
                        },
                    },
                },
            },
        )

        exit_code = validate_structure(config)
        assert exit_code == 0
