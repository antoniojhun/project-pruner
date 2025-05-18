# Project Pruner

A Python CLI tool to clean and archive old development projects.

## Features

- Prune (clean) project artifacts (`node_modules`, `vendor`, `dist`, etc.) in bulk
- Archive and remove old projects in one step
- Compress projects using xz (smaller) or gz (faster)
- Organise archives by date
- Restore archives to original paths
- Configurable via YAML or environment variables
- Dry-run option to preview changes
- Simple interface: just `clean` or `archive` a parent directory

## Installation

### Prerequisites
- Python 3.8 or higher
- Node.js 22.15.1 or higher

### Basic Installation
Clone the repository and install:
```bash
git clone https://github.com/antoniojhun/project-pruner.git
cd project-pruner
make setup
```

This will:
- Create a virtual environment in the `venv` directory
- Install the package in development mode

### Additional Development Setup
If you're contributing to the project, run this after the basic installation:
```bash
make dev-setup
```

This adds:
- Development dependencies
- Pre-commit hooks
- Node.js dependencies

### Development Commands
- `make test` - Run tests
- `make coverage` - Run tests with coverage report
- `make lint` - Run linters (ruff, mypy)
- `make format` - Format code (black, isort)
- `make clean` - Clean up development artifacts
- `make pre-commit-test` - Test only the pre-commit hook functionality

## Configuration

Project Pruner supports flexible configuration:
- By default, it looks for `config.yaml` in your current directory.
- If not found, it falls back to `~/.projectpruner/config.yaml`.
- You can also use environment variables.

### Creating a Configuration File
To create a starter config in your project directory:
```bash
projectpruner init-config
```

### Configuration Options
The configuration file contains the following sections:
```yaml
search_paths:  # Directories to search for old projects
  - /path/to/search
exclude_paths: []  # Paths to exclude from search
archive:
  archive_dir: /path/to/archives  # Where archives are stored
  compression: xz  # Compression algorithm (xz or gz)
  compression_level: 3  # Level of compression
  date_format: "%Y-%m-%d"  # Format for date in archive names
clean:
  patterns:  # Patterns to clean
    - '**/node_modules'
    - '**/dist'
  exclude_patterns: []  # Patterns to exclude from cleaning
  min_size: 0  # Minimum size in bytes to clean
```

## Usage

### Quick Reference

| Task | Command |
|------|---------|
| Clean old projects | `projectpruner clean /path/to/parent --until=3m` |
| Archive old projects | `projectpruner archive /path/to/parent --until=6m` |
| Restore a project | `projectpruner restore /path/to/archive.tar.xz --destination /path/to/restore_dir` |

### Clean (Clean Only)
```bash
projectpruner clean /path/to/parent --until=3m
```
Cleans up build artifacts in all project folders under `/path/to/parent` not modified in the last 3 months. Keeps the project folders.

### Archive (Clean, Archive, Remove)
```bash
projectpruner archive /path/to/parent --until=6m
```
Cleans, archives, and removes all project folders under `/path/to/parent` not modified in the last 6 months.

### Restore
```bash
projectpruner restore /path/to/archive.tar.xz --destination /path/to/restore_dir
```

### Compression Options
- `--compress xz` gives best compression (smallest archives, slower)
- `--compress gz` is fastest (larger archives, but quick)

### Dry Run Mode
Add the `--dry-run` flag to any command to preview changes without making them:
```bash
projectpruner clean /path/to/parent --until=3m --dry-run
```

## FAQ

### What does 'clean' do?
The `clean` command removes project artifacts (node_modules, vendor, dist, build, etc.) in all subdirectories older than the specified duration, but keeps the project directories.

### What does 'archive' do?
The `archive` command cleans project artifacts, compresses the project, and then removes the original project directory after archiving, for all subdirectories older than the specified duration.

### How is project age determined?
Project Pruner determines a project's age by the most recently modified file inside the project directory. If any file (including hidden files like `.DS_Store` or files in `node_modules`) was modified recently, the project is considered recent.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see [LICENSE](LICENSE) for details.
