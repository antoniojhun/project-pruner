"""
Configuration model for Project Pruner settings.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class ArchiveConfig:
    """Archive-specific configuration."""

    compression: str = "xz"
    compression_level: int = 3
    archive_dir: Path = Path.home() / ".projectpruner" / "archives"
    date_format: str = "%Y-%m-%d"


@dataclass
class CleanConfig:
    """Cleaning-specific configuration."""

    patterns: List[str] = field(
        default_factory=lambda: [
            "**/node_modules",
            "**/vendor",
            "**/dist",
            "**/build",
            "**/__pycache__",
            "**/*.pyc",
            "**/*.pyo",
            "**/*.pyd",
            "**/.DS_Store",
            "**/Thumbs.db",
        ]
    )

    exclude_patterns: List[str] = field(default_factory=list)
    min_size: int = 1024  # 1KB


@dataclass
class Config:
    """Main configuration for Project Pruner."""

    archive: ArchiveConfig = field(default_factory=ArchiveConfig)
    clean: CleanConfig = field(default_factory=CleanConfig)
    search_paths: List[Path] = field(default_factory=lambda: [Path.home()])
    exclude_paths: List[Path] = field(default_factory=list)
    log_level: str = "INFO"
    log_file: Optional[Path] = None

    @classmethod
    def from_dict(cls, data: Dict) -> "Config":
        """Create a Config instance from a dictionary."""
        archive_data = data.get("archive", {})
        if "archive_dir" in archive_data:
            archive_data["archive_dir"] = str(
                Path(archive_data["archive_dir"]).expanduser()
            )
        archive_config = ArchiveConfig(**archive_data)
        clean_config = CleanConfig(**data.get("clean", {}))

        return cls(
            archive=archive_config,
            clean=clean_config,
            search_paths=[Path(p).expanduser() for p in data.get("search_paths", [])],
            exclude_paths=[Path(p).expanduser() for p in data.get("exclude_paths", [])],
            log_level=data.get("log_level", "INFO"),
            log_file=(
                Path(data["log_file"]).expanduser() if "log_file" in data else None
            ),
        )

    def to_dict(self) -> Dict:
        """Convert the Config instance to a dictionary."""
        return {
            "archive": {
                "compression": self.archive.compression,
                "compression_level": self.archive.compression_level,
                "archive_dir": str(self.archive.archive_dir),
                "date_format": self.archive.date_format,
            },
            "clean": {
                "patterns": self.clean.patterns,
                "exclude_patterns": self.clean.exclude_patterns,
                "min_size": self.clean.min_size,
            },
            "search_paths": [str(p) for p in self.search_paths],
            "exclude_paths": [str(p) for p in self.exclude_paths],
            "log_level": self.log_level,
            "log_file": str(self.log_file) if self.log_file else None,
        }
