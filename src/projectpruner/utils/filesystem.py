"""
Filesystem utility module for file operations.
"""

import os
import shutil
from pathlib import Path
from typing import Iterator, List, Optional


def get_directory_size(path: Path) -> int:
    """Calculate the total size of a directory in bytes."""
    total_size = 0
    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            file_path = Path(dirpath) / filename
            if file_path.is_file():
                total_size += file_path.stat().st_size
    return total_size


def get_file_count(path: Path) -> int:
    """Count the number of files in a directory."""
    return sum(1 for _ in find_files(path))


def find_files(
    path: Path,
    pattern: Optional[str] = None,
    exclude_patterns: Optional[List[str]] = None,
) -> Iterator[Path]:
    """Find files in a directory, optionally matching a pattern."""
    if exclude_patterns is None:
        exclude_patterns = []

    for file_path in path.rglob(pattern or "*"):
        if not file_path.is_file():
            continue

        if any(file_path.match(exclude) for exclude in exclude_patterns):
            continue

        yield file_path


def safe_remove(path: Path) -> None:
    """Safely remove a file or directory."""
    try:
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)
    except Exception as e:
        raise RuntimeError(f"Error removing {path}: {str(e)}")


def ensure_directory(path: Path) -> None:
    """Ensure a directory exists, creating it if necessary."""
    path.mkdir(parents=True, exist_ok=True)


def is_empty_directory(path: Path) -> bool:
    """Check if a directory is empty."""
    if not path.is_dir():
        return False
    return not any(path.iterdir())
