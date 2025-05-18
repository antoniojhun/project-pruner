"""
Project cleaner module for removing unnecessary files and directories.
"""

import shutil
from pathlib import Path
from typing import Set

from projectpruner.models.config import Config
from projectpruner.utils.logger import get_logger

logger = get_logger(__name__)


class Cleaner:
    """Handles cleaning operations for development projects."""

    def __init__(self, config: Config):
        """Initialize the Cleaner with configuration."""
        self.config = config

    def clean(self, project_path: Path, dry_run: bool = False) -> None:
        """Clean a project by removing unnecessary files and directories."""
        if not project_path.exists():
            raise ValueError(f"Project path does not exist: {project_path}")

        if not project_path.is_dir():
            raise ValueError(f"Path is not a directory: {project_path}")

        # Find all matching paths
        paths_to_remove = self._find_paths_to_remove(project_path)

        if not paths_to_remove:
            logger.info(f"No files to clean in {project_path}")
            return

        # Calculate total size to be removed
        total_size = sum(
            path.stat().st_size if path.is_file() else self._get_dir_size(path)
            for path in paths_to_remove
        )

        logger.info(
            f"Found {len(paths_to_remove)} items to clean "
            f"({self._format_size(total_size)})"
        )

        if dry_run:
            logger.info("Dry run - no files will be removed")
            return

        # Remove paths
        for path in paths_to_remove:
            try:
                if path.is_file():
                    path.unlink()
                elif path.is_dir():
                    shutil.rmtree(path)
                logger.debug(f"Removed: {path}")
            except Exception as e:
                logger.error(f"Error removing {path}: {str(e)}")

    def _find_paths_to_remove(self, project_path: Path) -> Set[Path]:
        """Find all paths that should be removed."""
        paths_to_remove = set()

        # Check each pattern
        for pattern in self.config.clean.patterns:
            # Use rglob to search recursively for patterns like "**/node_modules"
            if pattern.startswith("**/"):
                # Remove the leading "**/" to get the actual directory name
                dir_name = pattern[3:]

                # First, try direct match in the project directory
                direct_match = project_path / dir_name
                if direct_match.exists() and not any(
                    direct_match.match(exclude)
                    for exclude in self.config.clean.exclude_patterns
                ):
                    paths_to_remove.add(direct_match)

                # Then find nested matches
                for path in project_path.rglob(dir_name):
                    if path.exists() and not any(
                        path.match(exclude)
                        for exclude in self.config.clean.exclude_patterns
                    ):
                        paths_to_remove.add(path)
            else:
                # Standard glob for non-recursive patterns
                for path in project_path.glob(pattern):
                    if not any(
                        path.match(exclude)
                        for exclude in self.config.clean.exclude_patterns
                    ):
                        paths_to_remove.add(path)

        return paths_to_remove

    def _get_dir_size(self, directory: Path) -> int:
        """Calculate the total size of a directory."""
        return sum(
            file.stat().st_size for file in directory.rglob("*") if file.is_file()
        )

    def _format_size(self, size_bytes: float) -> str:
        """Format size in bytes to human-readable format."""
        for unit in ["B", "KB", "MB", "GB"]:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} TB"
