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

    def test_prefix_separator_configuration(
        self, tmp_path: Path, capsys: CaptureFixture[str]
    ) -> None:
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

    def test_nested_prefix_validation(
        self, tmp_path: Path, capsys: CaptureFixture[str]
    ) -> None:
        """Nested feature folders should each require their parent's prefix."""
        config = create_minimal_config(tmp_path)
        config.structure.folder_depth = 3

        build_structure(
            tmp_path,
            {
                "src": {
                    "features": {
                        "auth": {
                            "auth_oauth": {
                                # Should be prefixed with auth_oauth_
                                "providers": {
                                    "types": {"token.py": "# types"},
                                },
                            },
                        },
                    },
                },
            },
        )

        exit_code = validate_structure(config)
        captured = capsys.readouterr()

        assert exit_code == 1
        assert "Feature folder must start with 'auth_oauth_'" in captured.out

    def test_valid_nested_prefix(self, tmp_path: Path) -> None:
        """Correctly prefixed nested folders should pass."""
        config = create_minimal_config(tmp_path)
        config.structure.folder_depth = 3

        build_structure(
            tmp_path,
            {
                "src": {
                    "features": {
                        "auth": {
                            "auth_oauth": {
                                "auth_oauth_google": {
                                    "types": {"token.py": "# types"},
                                },
                            },
                        },
                    },
                },
            },
        )

        exit_code = validate_structure(config)
        assert exit_code == 0
