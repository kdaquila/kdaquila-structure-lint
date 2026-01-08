"""Tests for basic structure validation functionality."""


from features.validation.utils.validator_structure import validate_structure


class TestStructureValidatorBasic:
    """Basic tests for validate_structure function."""

    def test_missing_src_root_fails(self, minimal_config, capsys):
        """Should fail when src root doesn't exist."""
        config = minimal_config

        exit_code = validate_structure(config)
        captured = capsys.readouterr()

        assert "not found" in captured.out or "Error" in captured.out
        assert exit_code == 1

    def test_valid_minimal_structure_passes(self, minimal_config):
        """Should pass with valid minimal structure."""
        config = minimal_config

        # Create minimal valid structure
        src = config.project_root / "src"
        features = src / "features"
        features.mkdir(parents=True)

        # Create a valid folder in features
        (features / "my_feature").mkdir()
        (features / "my_feature" / "types").mkdir()
        (features / "my_feature" / "types" / "module.py").touch()

        exit_code = validate_structure(config)
        assert exit_code == 0

    def test_missing_base_folder_fails(self, minimal_config):
        """Should fail when required base folder is missing."""
        config = minimal_config

        # Create src but not features
        (config.project_root / "src").mkdir()

        exit_code = validate_structure(config)
        assert exit_code == 1

    def test_extra_base_folder_fails(self, minimal_config):
        """Should fail when extra folders exist in src."""
        config = minimal_config

        src = config.project_root / "src"
        src.mkdir()
        (src / "features").mkdir()
        (src / "extra_folder").mkdir()  # Not in src_base_folders

        exit_code = validate_structure(config)
        assert exit_code == 1

    def test_files_in_src_root_fails(self, minimal_config):
        """Should fail when files exist in src root."""
        config = minimal_config

        src = config.project_root / "src"
        features = src / "features"
        features.mkdir(parents=True)

        # Add file in src root (not allowed)
        (src / "module.py").touch()

        exit_code = validate_structure(config)
        assert exit_code == 1

    def test_files_in_base_folder_fails(self, minimal_config, capsys):
        """Should fail when files exist directly in base folders like features/."""
        config = minimal_config

        src = config.project_root / "src"
        features = src / "features"
        features.mkdir(parents=True)

        # Add files directly in features/ (not allowed)
        (features / "calculator.py").touch()
        (features / "validator.py").touch()
        (features / "process_data.py").touch()

        exit_code = validate_structure(config)
        captured = capsys.readouterr()

        assert exit_code == 1
        assert "Files not allowed in root" in captured.out
        assert "calculator.py" in captured.out
