"""Line limits configuration."""

from dataclasses import dataclass


@dataclass
class LineLimitsConfig:
    """Configuration for line limits validator."""
    max_lines: int = 150
