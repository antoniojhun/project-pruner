"""
Project finder module for locating development projects.
"""

import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional

from projectpruner.models.config import Config
from projectpruner.models.project import Project


def is_relative_to(path: Path, other: Path) -> bool:
    try:
        path.relative_to(other)
        return True
    except ValueError:
        return False


class ProjectFinder:
    """Finds development projects based on various criteria."""

    def __init__(self, config: Config):
        """Initialize the ProjectFinder with configuration."""
        self.config = config

    def find(
        self,
        older_than: Optional[str] = None,
        larger_than: Optional[str] = None,
        pattern: Optional[str] = None,
    ) -> List[Project]:
        """Find projects matching the specified criteria."""
        projects = []

        search_paths = [Path(p).expanduser() for p in self.config.search_paths]
        exclude_paths = [Path(p).expanduser() for p in self.config.exclude_paths]

        for search_path in search_paths:
            if not search_path.exists():
                continue

            for path in search_path.iterdir():
                if not path.is_dir():
                    continue

                # Ensure exclude paths are absolute and expanded
                if any(
                    is_relative_to(path.resolve(), exclude.resolve())
                    for exclude in exclude_paths
                ):
                    continue

                try:
                    project = Project.from_path(path)

                    if self._matches_criteria(
                        project,
                        older_than=older_than,
                        larger_than=larger_than,
                        pattern=pattern,
                    ):
                        projects.append(project)

                except ValueError:
                    continue

        return projects

    def _matches_criteria(
        self,
        project: Project,
        older_than: Optional[str] = None,
        larger_than: Optional[str] = None,
        pattern: Optional[str] = None,
    ) -> bool:
        """Check if a project matches the specified criteria."""
        if older_than and not self._is_older_than(project, older_than):
            return False

        if larger_than and not self._is_larger_than(project, larger_than):
            return False

        if pattern and not self._matches_pattern(project, pattern):
            return False

        return True

    def _is_older_than(self, project: Project, duration: str) -> bool:
        """Check if a project is older than the specified duration."""
        now = datetime.now()

        # Parse duration string (e.g., "6months", "1year", "1y", "6m")
        match = re.match(r"(\d+)([a-z]+)", duration.lower())
        if not match:
            raise ValueError(f"Invalid duration format: {duration}")

        amount, unit = match.groups()
        amount = int(amount)

        # Support short and long forms
        if unit in ("y", "yr", "yrs", "year", "years"):
            delta = timedelta(days=amount * 365)
        elif unit in ("m", "mo", "mos", "month", "months"):
            delta = timedelta(days=amount * 30)
        elif unit in ("w", "wk", "wks", "week", "weeks"):
            delta = timedelta(weeks=amount)
        elif unit in ("d", "day", "days"):
            delta = timedelta(days=amount)
        else:
            raise ValueError(f"Unsupported time unit: {unit}")

        return project.last_modified < (now - delta)

    def _is_larger_than(self, project: Project, size: str) -> bool:
        """Check if a project is larger than the specified size."""
        # Parse size string (e.g., "1GB", "500MB")
        match = re.match(r"(\d+)([A-Za-z]+)", size)
        if not match:
            raise ValueError(f"Invalid size format: {size}")

        amount, unit = match.groups()
        amount = int(amount)

        # Convert to bytes
        if unit.upper() == "GB":
            size_bytes = amount * 1024 * 1024 * 1024
        elif unit.upper() == "MB":
            size_bytes = amount * 1024 * 1024
        elif unit.upper() == "KB":
            size_bytes = amount * 1024
        else:
            raise ValueError(f"Unsupported size unit: {unit}")

        return project.size > size_bytes

    def _matches_pattern(self, project: Project, pattern: str) -> bool:
        """Check if a project matches the specified pattern."""
        try:
            return bool(re.search(pattern, str(project.path)))
        except re.error:
            raise ValueError(f"Invalid pattern: {pattern}")
