# Project Pruner Usage Guide

## Installation

```bash
git clone https://github.com/antoniojhun/project-pruner.git
cd project-pruner
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

## Quick Reference

| Task | Command |
|------|---------|
| Clean (old) projects | `projectpruner clean /path/to/parent --until=3m` |
| Clean (large) projects | `projectpruner clean /path/to/parent --until=3m --larger-than=1GB` |
| Archive old projects | `projectpruner archive /path/to/parent --until=6m` |
| Archive large projects | `projectpruner archive /path/to/parent --until=6m --larger-than=1GB` |
| Restore a project | `projectpruner restore /path/to/archive.tar.xz --destination /path/to/restore_dir` |

- `clean` cleans build artifacts in all subdirectories older than the given duration (keeps the folders).
- `archive` cleans, archives, and removes all subdirectories older than the given duration.

## Basic Usage

### Clean (Clean Only)
```bash
projectpruner clean /path/to/parent --until=3m
```
Cleans up build artifacts in all project folders under `/path/to/parent` not modified in the last 3 months. Keeps the project folders.

Clean only large projects:
```bash
projectpruner clean /path/to/parent --until=3m --larger-than=1GB
```

### Archive (Clean, Archive, Remove)
```bash
projectpruner archive /path/to/parent --until=6m
```
Cleans, archives, and removes all project folders under `/path/to/parent` not modified in the last 6 months.

Archive only large projects:
```bash
projectpruner archive /path/to/parent --until=6m --larger-than=1GB
```

### Restore
```bash
projectpruner restore /path/to/archive.tar.xz --destination /path/to/restore_dir
```

## Advanced Usage

### Dry Run Mode
Preview operations without making changes:
```bash
projectpruner clean /path/to/parent --until=3m --dry-run
projectpruner archive /path/to/parent --until=6m --dry-run
```

### Environment Variables
Configure using environment variables:
```bash
export PROJECTPRUNER_ARCHIVE_DIR=~/archives
export PROJECTPRUNER_COMPRESSION=xz
export PROJECTPRUNER_COMPRESSION_LEVEL=9
projectpruner archive /path/to/parent --until=6m
```

## Tips and Best Practices

1. Always use `--dry-run` first to preview changes
2. Keep your configuration file up to date
3. Use environment variables for sensitive settings
4. Regularly prune and archive old projects
5. Use appropriate compression levels for your needs
6. Back up important projects before archiving (archiving will remove the original directory)
7. Monitor archive storage usage
8. Test restore operations periodically
9. Keep your Project Pruner installation updated

### Compression Support
- `--compress xz` gives best compression (smallest archives, slower)
- `--compress gz` is fastest (larger archives, but quick)
- Python's tarfile does not support zstd natively, so it is not available.
