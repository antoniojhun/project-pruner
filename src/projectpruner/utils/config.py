"""
Configuration utility module.
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

from projectpruner.models.config import Config


class ConfigManager:
    """Manages configuration loading and saving."""

    DEFAULT_CONFIG_PATH = Path.home() / ".projectpruner" / "config.yaml"

    @classmethod
    def load_config(cls, config_path: Optional[Path] = None) -> Config:
        """Load configuration from file or environment variables."""
        if config_path is not None:
            config_path = Path(config_path)  # <-- Ensure it's a Path object
        else:
            config_path = cls.DEFAULT_CONFIG_PATH

        # Try to load from file
        if config_path.exists():
            try:
                with open(config_path) as f:
                    data = yaml.safe_load(f)
                return Config.from_dict(data)
            except Exception as e:
                raise RuntimeError(f"Error loading config file: {str(e)}")

        # Load from environment variables
        return cls._load_from_env()

    @classmethod
    def save_config(cls, config: Config, config_path: Optional[Path] = None) -> None:
        """Save configuration to file."""
        if config_path is None:
            config_path = cls.DEFAULT_CONFIG_PATH

        try:
            config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(config_path, "w") as f:
                yaml.dump(config.to_dict(), f, default_flow_style=False)
        except Exception as e:
            raise RuntimeError(f"Error saving config file: {str(e)}")

    @classmethod
    def _load_from_env(cls) -> Config:
        """Load configuration from environment variables."""
        data: Dict[str, Any] = {
            "archive": {},
            "clean": {},
            "search_paths": [],
            "exclude_paths": [],
        }

        # Archive settings
        if archive_dir := os.getenv("PROJECTPRUNER_ARCHIVE_DIR"):
            data["archive"]["archive_dir"] = archive_dir

        if compression := os.getenv("PROJECTPRUNER_COMPRESSION"):
            data["archive"]["compression"] = compression

        if compression_level := os.getenv("PROJECTPRUNER_COMPRESSION_LEVEL"):
            data["archive"]["compression_level"] = int(compression_level)

        # Clean settings
        if patterns := os.getenv("PROJECTPRUNER_CLEAN_PATTERNS"):
            data["clean"]["patterns"] = patterns.split(",")

        if exclude_patterns := os.getenv("PROJECTPRUNER_CLEAN_EXCLUDE_PATTERNS"):
            data["clean"]["exclude_patterns"] = exclude_patterns.split(",")

        # Search paths
        if search_paths := os.getenv("PROJECTPRUNER_SEARCH_PATHS"):
            data["search_paths"] = search_paths.split(":")

        # Exclude paths
        if exclude_paths := os.getenv("PROJECTPRUNER_EXCLUDE_PATHS"):
            data["exclude_paths"] = exclude_paths.split(":")

        # Log settings
        if log_level := os.getenv("PROJECTPRUNER_LOG_LEVEL"):
            data["log_level"] = log_level

        if log_file := os.getenv("PROJECTPRUNER_LOG_FILE"):
            data["log_file"] = log_file

        return Config.from_dict(data)
