# project-pruner

A lightweight Python CLI tool to clean, archive, and manage old development projects for efficient workspace storage optimisation.

## Features

- Prune (clean) project artifacts (`node_modules`, `vendor`, `dist`, etc.) in bulk
- Archive and remove old projects in one step
- Compress projects using xz or gz
- Organize archives by date
- Restore archives to original paths
- Configurable via YAML or environment variables
- Dry-run option to preview changes
- Simple interface: just `clean` or `archive` a parent directory

## Development Setup

### Prerequisites
- Python 3.8 or higher
- Node.js 22.15.1 or higher
- Git

### Quick Start
1. Clone the repository:
```bash
git clone https://github.com/antoniojhun/project-pruner.git
cd project-pruner
```

2. Set up the development environment:
```bash
make setup
```

3. Activate the virtual environment:
```bash
source venv/bin/activate  # On Unix/macOS
# or
.\venv\Scripts\activate  # On Windows
```

### Development Commands
- `make test` - Run tests
- `make lint` - Run linters (ruff, mypy)
- `make format` - Format code (black, isort)
- `make clean` - Clean up development artifacts
- `make pre-commit-test` - Test only the pre-commit hook functionality

## Installation

```bash
git clone https://github.com/antoniojhun/project-pruner.git
cd projectpruner
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

## Quick Reference

| Task | Command |
|------|---------|
| Clean old projects | `projectpruner clean /path/to/parent --until=3m` |
| Archive old projects | `projectpruner archive /path/to/parent --until=6m` |
| Restore a project | `projectpruner restore /path/to/archive.tar.xz --destination /path/to/restore_dir` |

- `clean` cleans build artifacts in all subdirectories older than the given duration (keeps the folders).
- `archive` cleans, archives, and removes all subdirectories older than the given duration.

## Usage

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

## Compression Support
- `--compress xz` gives best compression (smallest archives, slower)
- `--compress gz` is fastest (larger archives, but quick)

## Configuration

Project Pruner supports flexible configuration:
- By default, it looks for `config.yaml` in your current directory.
- If not found, it falls back to `~/.projectpruner/config.yaml`.
- You can also use environment variables.

To create a starter config in your project directory:
```bash
projectpruner init-config
```

## Requirements

- Python 3.8+
- Cross-platform support (Linux, macOS, Windows)

## FAQ

### What does 'clean' do?
- The `clean` command cleans project artifacts (node_modules, vendor, dist, build, etc.) in all subdirectories older than the specified duration, but keeps the project directories.

### What does 'archive' do?
- The `archive` command cleans project artifacts, compresses the project, and then removes the original project directory after archiving, for all subdirectories older than the specified duration.

### How is project age determined?
- Project Pruner determines a project's age by the most recently modified file inside the project directory. If any file (including hidden files like `.DS_Store` or files in `node_modules`) was modified recently, the project is considered recent.

## License

MIT License - see [LICENSE](LICENSE) for details.