"""
Project Pruner - A tool for cleaning, archiving, and managing old software development projects.
"""

__version__ = "0.1.0"

# Import key modules for easier access
from projectpruner.core.archiver import Archiver
from projectpruner.core.cleaner import Cleaner
from projectpruner.core.finder import ProjectFinder
from projectpruner.models.project import Project
from projectpruner.utils.config import ConfigManager
from projectpruner.utils.logger import setup_logger

__all__ = [
    "Archiver",
    "Cleaner",
    "ProjectFinder",
    "Project",
    "ConfigManager",
    "setup_logger",
]
