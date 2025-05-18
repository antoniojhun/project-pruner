"""
Command-line interface for Project Pruner.
"""

import os
import shutil
from pathlib import Path
from typing import Literal, Optional

import click
from rich.console import Console
from rich.traceback import install

from projectpruner.core.archiver import Archiver
from projectpruner.core.cleaner import Cleaner
from projectpruner.core.finder import ProjectFinder
from projectpruner.models.project import Project
from projectpruner.utils.config import ConfigManager
from projectpruner.utils.logger import setup_logger
from projectpruner.utils.progress import create_progress, format_path

# Install rich traceback handler
install(show_locals=True)

# Initialize console
console = Console()

# Initialize logger
logger = setup_logger()

CONFIG_TEMPLATE = os.path.join(
    os.path.dirname(__file__), "config", "templates", "default_config.yaml"
)
USER_CONFIG_DIR = os.path.expanduser("~/.projectpruner")
USER_CONFIG_PATH = os.path.join(USER_CONFIG_DIR, "config.yaml")


@click.group()
@click.version_option()
@click.option(
    "--dry-run",
    is_flag=True,
    help="Preview changes without making them",
)
@click.option(
    "--config",
    type=click.Path(exists=True, dir_okay=False),
    help="Path to config file",
)
@click.pass_context
def main(ctx: click.Context, dry_run: bool, config: Optional[str] = None) -> None:
    """Project Pruner - Clean and archive old development projects."""
    ctx.ensure_object(dict)
    # Config resolution order: --config, ./config.yaml, ~/.projectpruner/config.yaml, or environment variables
    config_path = None
    if config:
        config_path = Path(config)
    elif os.path.exists("config.yaml"):
        config_path = Path(os.path.abspath("config.yaml"))
    elif os.path.exists(os.path.expanduser("~/.projectpruner/config.yaml")):
        config_path = Path(os.path.expanduser("~/.projectpruner/config.yaml"))
    ctx.obj["config"] = (
        ConfigManager.load_config(config_path)
        if config_path
        else ConfigManager.load_config()
    )
    ctx.obj["dry_run"] = dry_run


@main.command("clean")
@click.argument("parent_dir", type=click.Path(exists=True, file_okay=False))
@click.option(
    "--until",
    "-u",
    required=True,
    help="Only clean projects not modified in the last duration (e.g., 3m, 6months, 1year)",
)
@click.option(
    "--larger-than",
    type=str,
    help="Only clean projects larger than specified size (e.g., 50MB, 1GB)",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Preview changes without making them",
)
@click.pass_context
def clean(
    ctx: click.Context,
    parent_dir: str,
    until: str,
    larger_than: str,
    dry_run: bool,
) -> None:
    """Clean up build artifacts in all project folders under PARENT_DIR older than UNTIL and optionally larger than LARGER_THAN."""
    cleaner = Cleaner(ctx.obj["config"])
    parent = Path(parent_dir).expanduser()
    finder = ProjectFinder(ctx.obj["config"])
    projects = []
    for subdir in parent.iterdir():
        if not subdir.is_dir():
            continue
        try:
            project = Project.from_path(subdir)
        except Exception:
            continue
        if not finder._is_older_than(project, until):
            continue
        if larger_than and not finder._is_larger_than(project, larger_than):
            continue
        projects.append(subdir)
    if len(projects) > 1:
        with create_progress("Cleaning projects") as progress:
            task = progress.add_task("Cleaning...", total=len(projects))
            for subdir in projects:
                progress.update(task, description=f"Cleaning {format_path(subdir)}")
                cleaner.clean(subdir, dry_run=dry_run)
                if not dry_run:
                    console.print(f"[green]Cleaned: {subdir}[/green]")
                progress.advance(task)
    else:
        for subdir in projects:
            console.print(f"[bold]Cleaning {subdir}...[/bold]")
            cleaner.clean(subdir, dry_run=dry_run)
            if not dry_run:
                console.print(f"[green]Cleaned: {subdir}[/green]")


@main.command()
@click.argument("parent_dir", type=click.Path(exists=True, file_okay=False))
@click.option(
    "--until",
    "-u",
    required=True,
    help="Only archive projects not modified in the last duration (e.g., 6m, 1year)",
)
@click.option(
    "--larger-than",
    type=str,
    help="Only archive projects larger than specified size (e.g., 50MB, 1GB)",
)
@click.option(
    "--compress",
    type=click.Choice(["xz", "gz"]),
    default="xz",
    help="Compression algorithm to use (xz=best, gz=fastest)",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Preview changes without making them",
)
@click.pass_context
def archive(
    ctx: click.Context,
    parent_dir: str,
    until: str,
    larger_than: str,
    compress: Literal["xz", "gz"],
    dry_run: bool,
) -> None:
    """Clean, archive, and remove all project folders under PARENT_DIR older than UNTIL and optionally larger than LARGER_THAN."""
    archiver = Archiver(ctx.obj["config"])
    cleaner = Cleaner(ctx.obj["config"])
    parent = Path(parent_dir).expanduser()
    finder = ProjectFinder(ctx.obj["config"])
    projects = []
    for subdir in parent.iterdir():
        if not subdir.is_dir():
            continue
        try:
            project = Project.from_path(subdir)
        except Exception:
            continue
        if not finder._is_older_than(project, until):
            continue
        if larger_than and not finder._is_larger_than(project, larger_than):
            continue
        projects.append(subdir)
    if len(projects) > 1:
        with create_progress("Archiving projects") as progress:
            task = progress.add_task("Archiving...", total=len(projects))
            for subdir in projects:
                progress.update(task, description=f"Archiving {format_path(subdir)}")
                cleaner.clean(subdir, dry_run=dry_run)
                if not dry_run:
                    try:
                        archive_path = archiver.archive(
                            subdir,
                            compress=compress,
                            dry_run=dry_run,
                        )
                        console.print(f"[green]Archived to: {archive_path}[/green]")

                        # Force remove the directory
                        if subdir.exists():
                            shutil.rmtree(subdir)
                            console.print(f"[red]Removed original: {subdir}[/red]")
                    except Exception as e:
                        logger.error(f"Error during archive operation: {str(e)}")
                        console.print(f"[red]Error: {str(e)}[/red]")
                progress.advance(task)
    else:
        for subdir in projects:
            console.print(f"[bold]Cleaning {subdir}...[/bold]")
            cleaner.clean(subdir, dry_run=dry_run)
            console.print(f"[bold]Archiving {subdir}...[/bold]")
            if not dry_run:
                try:
                    archive_path = archiver.archive(
                        subdir,
                        compress=compress,
                        dry_run=dry_run,
                    )
                    console.print(f"[green]Archived to: {archive_path}[/green]")

                    # Force remove the directory
                    if subdir.exists():
                        shutil.rmtree(subdir)
                        console.print(f"[red]Removed original: {subdir}[/red]")
                except Exception as e:
                    logger.error(f"Error during archive operation: {str(e)}")
                    console.print(f"[red]Error: {str(e)}[/red]")


@main.command()
@click.argument("archive_path", type=click.Path(exists=True))
@click.option(
    "--destination",
    "-d",
    type=click.Path(),
    help="Destination path for restored project",
)
@click.pass_context
def restore(
    ctx: click.Context,
    archive_path: str,
    destination: Optional[str],
) -> None:
    """Restore an archived project."""
    archiver = Archiver(ctx.obj["config"])

    try:
        restored_path = archiver.restore(
            Path(archive_path),
            destination=Path(destination) if destination else None,
            dry_run=ctx.obj["dry_run"],
        )

        if not ctx.obj["dry_run"]:
            console.print(f"[green]Restored to: {restored_path}[/green]")

    except Exception as e:
        logger.error(f"Error restoring {archive_path}: {str(e)}")
        console.print(f"[red]Error: {str(e)}[/red]")


@main.command("init-config")
@click.argument("path", required=False, default="config.yaml")
def init_config(path: str) -> None:
    """Create a starter configuration file (default: ./config.yaml)."""
    dest = os.path.abspath(path)
    if os.path.exists(dest):
        console.print(f"[yellow]Config already exists at {dest}[/yellow]")
        return
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copy(CONFIG_TEMPLATE, dest)
    console.print(f"[green]Created config at {dest}[/green]")


if __name__ == "__main__":
    main(obj={})


def cli() -> None:
    main()
