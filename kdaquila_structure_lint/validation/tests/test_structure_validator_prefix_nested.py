"""Tests for nested prefix validation."""

from pathlib import Path

from _pytest.capture import CaptureFixture

from kdaquila_structure_lint.test_fixtures import build_structure, create_minimal_config
from kdaquila_structure_lint.validation.utils.validator_structure import validate_structure


class TestNestedPrefixValidation:
    """Tests for nested feature folder prefix requirements."""

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
