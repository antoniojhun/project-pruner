"""
Logging utility module.
"""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logger(
    name: str = "projectpruner",
    level: str = "INFO",
    log_file: Optional[Path] = None,
) -> logging.Logger:
    """Set up and configure the logger."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create formatters
    console_formatter = logging.Formatter("%(message)s")
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler (if specified)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for the specified name."""
    return logging.getLogger(name)
