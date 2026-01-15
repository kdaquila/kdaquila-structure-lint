"""Config functions package."""

from kdaquila_structure_lint.config._functions.loader import load_config
from kdaquila_structure_lint.config._functions.project_root import find_project_root

__all__ = ["find_project_root", "load_config"]
