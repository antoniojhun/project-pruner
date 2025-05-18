"""
Project archiver module for compressing and managing project archives.
"""

import shutil
import tarfile
from datetime import datetime
from pathlib import Path
from typing import List, Literal, Optional

from projectpruner.models.config import Config
from projectpruner.utils.logger import get_logger

logger = get_logger(__name__)


class Archiver:
    """Handles archiving operations for development projects."""

    def __init__(self, config: Config):
        """Initialize the Archiver with configuration."""
        self.config = config
        self.archive_dir = Path(self.config.archive.archive_dir).expanduser()
        self.archive_dir.mkdir(parents=True, exist_ok=True)

    def archive(
        self,
        project_path: Path,
        compress: Literal["xz", "gz"] = "xz",
        dry_run: bool = False,
    ) -> Path:
        """Archive a project directory."""
        if not project_path.exists():
            raise ValueError(f"Project path does not exist: {project_path}")

        if not project_path.is_dir():
            raise ValueError(f"Project path is not a directory: {project_path}")

        # Only support xz and gz
        if compress not in ("xz", "gz"):
            raise ValueError(f"Unsupported compression: {compress}. Use 'xz' or 'gz'.")

        # Create archive path
        date_str = datetime.now().strftime(self.config.archive.date_format)
        archive_name = f"{project_path.name}_{date_str}.tar.{compress}"
        archive_path = self.archive_dir / archive_name

        if archive_path.exists():
            raise ValueError(f"Archive already exists: {archive_path}")

        logger.info(f"Archiving {project_path} to {archive_path}")

        if dry_run:
            logger.info("Dry run - no archive will be created")
            return archive_path

        # Create archive
        try:
            mode: Literal["w:gz", "w:xz"] = f"w:{compress}"  # type: ignore
            with tarfile.open(str(archive_path), mode) as tar:
                tar.add(project_path, arcname=project_path.name)

            logger.info(f"Successfully created archive: {archive_path}")
            return archive_path

        except Exception as e:
            if archive_path.exists():
                archive_path.unlink()
            raise RuntimeError(f"Error creating archive: {str(e)}")

    def restore(
        self,
        archive_path: Path,
        destination: Optional[Path] = None,
        dry_run: bool = False,
    ) -> Path:
        """Restore a project from an archive."""
        # Ensure archive_path is a Path object
        if isinstance(archive_path, str):
            archive_path = Path(archive_path)
        if not archive_path.exists():
            raise ValueError(f"Archive does not exist: {archive_path}")

        if not archive_path.is_file():
            raise ValueError(f"Archive path is not a file: {archive_path}")

        # Determine destination
        if destination is None:
            # Extract project name from archive name
            project_name = archive_path.stem.split("_")[0]
            destination = Path.cwd() / project_name
        else:
            destination = Path(destination)

        if destination.exists():
            raise ValueError(f"Destination already exists: {destination}")

        logger.info(f"Restoring {archive_path} to {destination}")

        if dry_run:
            logger.info("Dry run - no files will be extracted")
            return destination

        # Extract archive
        try:
            destination.mkdir(parents=True, exist_ok=True)
            with tarfile.open(str(archive_path), "r:*") as tar:
                tar.extractall(path=destination)

            logger.info(f"Successfully restored project to: {destination}")
            return destination

        except Exception as e:
            if destination.exists():
                shutil.rmtree(destination)
            raise RuntimeError(f"Error restoring archive: {str(e)}")

    def list_archives(self) -> List[Path]:
        """List all available archives."""
        return sorted(
            path for path in self.archive_dir.glob("*.tar.*") if path.is_file()
        )

    def get_archive_info(self, archive_path: Path) -> dict:
        """Get information about an archive."""
        if not archive_path.exists():
            raise ValueError(f"Archive does not exist: {archive_path}")

        if not archive_path.is_file():
            raise ValueError(f"Archive path is not a file: {archive_path}")

        try:
            with tarfile.open(str(archive_path), "r:*") as tar:
                members = tar.getmembers()
                total_size = sum(member.size for member in members)

                return {
                    "path": archive_path,
                    "size": archive_path.stat().st_size,
                    "compressed_size": total_size,
                    "file_count": len(members),
                    "created": datetime.fromtimestamp(archive_path.stat().st_mtime),
                }

        except Exception as e:
            raise RuntimeError(f"Error reading archive info: {str(e)}")
