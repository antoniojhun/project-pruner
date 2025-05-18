"""
Project model for representing development projects.
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class Project:
    """Represents a development project."""

    path: Path
    name: str
    size: int
    last_modified: datetime
    type: Optional[str] = None

    @classmethod
    def from_path(cls, path: Path) -> "Project":
        """Create a Project instance from a path."""
        if not path.exists():
            raise ValueError(f"Path does not exist: {path}")

        if not path.is_dir():
            raise ValueError(f"Path is not a directory: {path}")

        # Calculate total size
        total_size = sum(f.stat().st_size for f in path.rglob("*") if f.is_file())

        # Get last modified time
        last_modified = datetime.fromtimestamp(
            max(f.stat().st_mtime for f in path.rglob("*") if f.is_file())
        )

        return cls(
            path=path,
            name=path.name,
            size=total_size,
            last_modified=last_modified,
        )

    def __str__(self) -> str:
        """String representation of the project."""
        return f"{self.name} ({self.path})"

    def __repr__(self) -> str:
        """Detailed string representation of the project."""
        return (
            f"Project("
            f"path={self.path}, "
            f"name={self.name}, "
            f"size={self.size}, "
            f"last_modified={self.last_modified}, "
            f"type={self.type}"
            f")"
        )
