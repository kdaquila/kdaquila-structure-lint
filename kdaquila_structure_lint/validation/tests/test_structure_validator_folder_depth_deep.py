"""Tests for folder_depth configuration with depth 2 and 3."""

from pathlib import Path

from kdaquila_structure_lint.test_fixtures import build_structure, create_minimal_config
from kdaquila_structure_lint.validation.utils.validator_structure import validate_structure


class TestFolderDepthDeep:
    """Tests for folder_depth configuration with deeper nesting."""

    def test_folder_depth_2_allows_two_custom_layers(self, tmp_path: Path) -> None:
        """With folder_depth=2 (default), two layers of custom folders allowed."""
        config = create_minimal_config(tmp_path)
        # Default is 2, but let's be explicit
        config.structure.folder_depth = 2

        build_structure(
            tmp_path,
            {
                "src": {
                    "features": {
                        "domain": {
                            "domain_subdomain": {  # Properly prefixed
                                "types": {"module.py": ""},
                            },
                        },
                    },
                },
            },
        )

        exit_code = validate_structure(config)
        assert exit_code == 0

    def test_folder_depth_3_allows_three_custom_layers(self, tmp_path: Path) -> None:
        """With folder_depth=3, three layers of custom folders allowed."""
        config = create_minimal_config(tmp_path)
        config.structure.folder_depth = 3

        build_structure(
            tmp_path,
            {
                "src": {
                    "features": {
                        "level1": {
                            "level1_level2": {  # Properly prefixed
                                "level1_level2_level3": {  # Properly prefixed
                                    "types": {"module.py": ""},
                                },
                            },
                        },
                    },
                },
            },
        )

        exit_code = validate_structure(config)
        assert exit_code == 0
