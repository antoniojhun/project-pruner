"""
Progress utility module for displaying progress bars.
"""

from pathlib import Path
from typing import Optional

from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)


def create_progress(
    description: str,
    total: Optional[int] = None,
) -> Progress:
    """Create a progress bar with standard columns."""
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        expand=True,
    )


def format_path(path: Path, max_length: int = 50) -> str:
    """Format a path for display in progress bars."""
    path_str = str(path)
    if len(path_str) > max_length:
        return f"...{path_str[-max_length+3:]}"
    return path_str
