"""Tests for custom structure configuration."""

from pathlib import Path

from _pytest.capture import CaptureFixture

from features.test_fixtures import create_minimal_config
from features.validation.utils.validator_structure import validate_structure


class TestStructureValidatorCustomConfig:
    """Tests for custom structure configuration."""

    def test_custom_strict_format_roots(self, tmp_path: Path) -> None:
        """Should use custom strict_format_roots."""
        config = create_minimal_config(tmp_path)
        config.structure.strict_format_roots = {"lib"}

        # Create structure with custom strict_format_root
        lib = config.project_root / "lib"
        features = lib / "features"
        features.mkdir(parents=True)
        (features / "my_feature").mkdir()
        (features / "my_feature" / "types").mkdir()
        (features / "my_feature" / "types" / "module.py").touch()

        exit_code = validate_structure(config)
        assert exit_code == 0

    def test_multiple_strict_format_roots(
        self, tmp_path: Path, capsys: CaptureFixture[str]
    ) -> None:
        """Should validate multiple strict_format_roots."""
        config = create_minimal_config(tmp_path)
        config.structure.strict_format_roots = {"src", "lib"}

        # Create valid structures in both roots
        for root_name in ["src", "lib"]:
            root = config.project_root / root_name
            features = root / "features"
            features.mkdir(parents=True)
            (features / "my_feature").mkdir()
            (features / "my_feature" / "types").mkdir()
            (features / "my_feature" / "types" / "module.py").touch()

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

    def test_custom_allowed_files(self, tmp_path: Path) -> None:
        """Should allow custom files like py.typed via allowed_files config."""
        config = create_minimal_config(tmp_path)
        config.structure.allowed_files = {"__init__.py", "py.typed"}

        # Create valid structure
        src = config.project_root / "src"
        features = src / "features"
        features.mkdir(parents=True)
        (features / "my_feature").mkdir()
        (features / "my_feature" / "types").mkdir()
        (features / "my_feature" / "types" / "module.py").touch()

        # Add custom allowed file - should be allowed
        (features / "my_feature" / "py.typed").touch()

        exit_code = validate_structure(config)
        assert exit_code == 0

    def test_custom_ignored_folders(self, tmp_path: Path) -> None:
        """Should ignore custom folders like .venv, build via ignored_folders config."""
        config = create_minimal_config(tmp_path)
        config.structure.ignored_folders = {
            "__pycache__",
            ".venv",
            "build",
            ".egg-info",
        }

        # Create valid structure
        src = config.project_root / "src"
        features = src / "features"
        features.mkdir(parents=True)
        (features / "my_feature").mkdir()
        (features / "my_feature" / "types").mkdir()
        (features / "my_feature" / "types" / "module.py").touch()

        # Add ignored directories - should be ignored
        (features / "my_feature" / ".venv").mkdir()
        (features / "my_feature" / ".venv" / "lib").mkdir()
        (features / "my_feature" / "build").mkdir()
        (features / "my_feature" / "build" / "output.txt").touch()

        exit_code = validate_structure(config)
        assert exit_code == 0


class TestFolderDepthVariations:
    """Tests for folder_depth configuration."""

    def test_folder_depth_0_requires_standard_at_base(self, tmp_path: Path) -> None:
        """With folder_depth=0, base folders must have standard folders only."""
        config = create_minimal_config(tmp_path)
        config.structure.folder_depth = 0

        # Create structure: src/features/ must have standard folders only
        src = config.project_root / "src"
        features = src / "features"
        features.mkdir(parents=True)
        (features / "types").mkdir()
        (features / "types" / "module.py").touch()

        exit_code = validate_structure(config)
        # This should pass - base folder has standard folders
        assert exit_code == 0

    def test_folder_depth_0_rejects_nested_custom_folders(
        self, tmp_path: Path, capsys: CaptureFixture[str]
    ) -> None:
        """With folder_depth=0, nested custom folders inside first layer fail."""
        config = create_minimal_config(tmp_path)
        config.structure.folder_depth = 0

        # Create structure with nested custom folder inside first custom layer
        src = config.project_root / "src"
        features = src / "features"
        features.mkdir(parents=True)
        (features / "my_feature").mkdir()
        # nested_feature is a CUSTOM folder inside my_feature - should fail at depth 0
        (features / "my_feature" / "nested_feature").mkdir()
        (features / "my_feature" / "nested_feature" / "types").mkdir()
        (features / "my_feature" / "nested_feature" / "types" / "module.py").touch()

        exit_code = validate_structure(config)
        captured = capsys.readouterr()

        # Nested custom folder "nested_feature" exceeds depth 0
        assert exit_code == 1
        assert "Exceeds max depth" in captured.out

    def test_folder_depth_1_allows_one_custom_layer(self, tmp_path: Path) -> None:
        """With folder_depth=1, one layer of custom folders is allowed."""
        config = create_minimal_config(tmp_path)
        config.structure.folder_depth = 1

        # Create structure: src/features/my_feature/types/
        src = config.project_root / "src"
        features = src / "features"
        features.mkdir(parents=True)
        (features / "my_feature").mkdir()
        (features / "my_feature" / "types").mkdir()
        (features / "my_feature" / "types" / "module.py").touch()

        exit_code = validate_structure(config)
        assert exit_code == 0

    def test_folder_depth_1_rejects_nested_custom(
        self, tmp_path: Path, capsys: CaptureFixture[str]
    ) -> None:
        """With folder_depth=1, nested custom folders should fail."""
        config = create_minimal_config(tmp_path)
        config.structure.folder_depth = 1

        # Create structure with 2 layers of custom folders
        src = config.project_root / "src"
        features = src / "features"
        features.mkdir(parents=True)
        (features / "domain").mkdir()
        (features / "domain" / "subdomain").mkdir()
        (features / "domain" / "subdomain" / "types").mkdir()
        (features / "domain" / "subdomain" / "types" / "module.py").touch()

        exit_code = validate_structure(config)
        captured = capsys.readouterr()

        assert exit_code == 1
        assert "Exceeds max depth" in captured.out

    def test_folder_depth_2_allows_two_custom_layers(self, tmp_path: Path) -> None:
        """With folder_depth=2 (default), two layers of custom folders allowed."""
        config = create_minimal_config(tmp_path)
        # Default is 2, but let's be explicit
        config.structure.folder_depth = 2

        # Create structure with 2 layers of custom folders
        src = config.project_root / "src"
        features = src / "features"
        features.mkdir(parents=True)
        (features / "domain").mkdir()
        (features / "domain" / "subdomain").mkdir()
        (features / "domain" / "subdomain" / "types").mkdir()
        (features / "domain" / "subdomain" / "types" / "module.py").touch()

        exit_code = validate_structure(config)
        assert exit_code == 0

    def test_folder_depth_3_allows_three_custom_layers(self, tmp_path: Path) -> None:
        """With folder_depth=3, three layers of custom folders allowed."""
        config = create_minimal_config(tmp_path)
        config.structure.folder_depth = 3

        # Create structure with 3 layers of custom folders
        src = config.project_root / "src"
        features = src / "features"
        features.mkdir(parents=True)
        (features / "level1").mkdir()
        (features / "level1" / "level2").mkdir()
        (features / "level1" / "level2" / "level3").mkdir()
        (features / "level1" / "level2" / "level3" / "types").mkdir()
        (features / "level1" / "level2" / "level3" / "types" / "module.py").touch()

        exit_code = validate_structure(config)
        assert exit_code == 0


class TestMutualExclusivity:
    """Tests for mutual exclusivity rules at folder levels."""

    def test_standard_and_custom_at_same_level_fails(
        self, tmp_path: Path, capsys: CaptureFixture[str]
    ) -> None:
        """Cannot mix standard folders with custom folders at same level."""
        config = create_minimal_config(tmp_path)

        src = config.project_root / "src"
        features = src / "features"
        features.mkdir(parents=True)
        (features / "my_feature").mkdir()
        # Mix standard folder (types) with custom folder (custom_thing) at same level
        (features / "my_feature" / "types").mkdir()
        (features / "my_feature" / "types" / "module.py").touch()
        (features / "my_feature" / "custom_thing").mkdir()
        (features / "my_feature" / "custom_thing" / "types").mkdir()
        (features / "my_feature" / "custom_thing" / "types" / "module.py").touch()

        exit_code = validate_structure(config)
        captured = capsys.readouterr()

        assert exit_code == 1
        assert "Cannot mix standard and custom folders" in captured.out

    def test_standard_and_general_at_same_level_fails(
        self, tmp_path: Path, capsys: CaptureFixture[str]
    ) -> None:
        """Cannot mix standard folders with general folder at same level."""
        config = create_minimal_config(tmp_path)

        src = config.project_root / "src"
        features = src / "features"
        features.mkdir(parents=True)
        (features / "my_feature").mkdir()
        # Mix standard folder (types) with general folder at same level
        (features / "my_feature" / "types").mkdir()
        (features / "my_feature" / "types" / "module.py").touch()
        (features / "my_feature" / "general").mkdir()
        (features / "my_feature" / "general" / "module.py").touch()

        exit_code = validate_structure(config)
        captured = capsys.readouterr()

        assert exit_code == 1
        assert "Cannot mix general and standard folders" in captured.out

    def test_general_folder_requires_custom_sibling(
        self, tmp_path: Path, capsys: CaptureFixture[str]
    ) -> None:
        """General folder requires at least one custom subfolder as sibling."""
        config = create_minimal_config(tmp_path)

        src = config.project_root / "src"
        features = src / "features"
        features.mkdir(parents=True)
        (features / "my_feature").mkdir()
        # Only general folder, no custom siblings
        (features / "my_feature" / "general").mkdir()
        (features / "my_feature" / "general" / "module.py").touch()

        exit_code = validate_structure(config)
        captured = capsys.readouterr()

        assert exit_code == 1
        assert "general requires at least one custom subfolder" in captured.out


class TestGeneralFolderDepthLimit:
    """Tests for general folder respecting depth limits."""

    def test_general_folder_at_max_depth_rejected(
        self, tmp_path: Path, capsys: CaptureFixture[str]
    ) -> None:
        """General folder at max depth should be rejected."""
        config = create_minimal_config(tmp_path)
        config.structure.folder_depth = 1

        src = config.project_root / "src"
        features = src / "features"
        features.mkdir(parents=True)
        (features / "my_feature").mkdir()
        # At depth=1, my_feature is the max custom layer
        # Adding general here would exceed depth
        (features / "my_feature" / "general").mkdir()
        (features / "my_feature" / "general" / "module.py").touch()
        # Also need a custom sibling for general to be valid
        (features / "my_feature" / "subfolder").mkdir()
        (features / "my_feature" / "subfolder" / "types").mkdir()
        (features / "my_feature" / "subfolder" / "types" / "module.py").touch()

        exit_code = validate_structure(config)
        captured = capsys.readouterr()

        assert exit_code == 1
        # The subfolder exceeds depth too
        assert "Exceeds max depth" in captured.out
