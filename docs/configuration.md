# Project Pruner Configuration

Project Pruner uses a simple YAML configuration file to control archiving, pruning, and cleaning behavior. The config file is auto-detected from `./config.yaml` or `~/.projectpruner/config.yaml`, or you can use environment variables.

## Minimal Example

```yaml
archive:
  compression: xz
  compression_level: 3
  archive_dir: ~/archives
  date_format: "%Y-%m-%d"
clean:
  patterns:
    - "**/node_modules"
    - "**/vendor"
    - "**/dist"
    - "**/build"
    - "**/__pycache__"
    - "**/*.pyc"
    - "**/*.pyo"
    - "**/*.pyd"
    - "**/.DS_Store"
    - "**/Thumbs.db"
  exclude_patterns: []
  min_size: 1024
search_paths:
  - ~/projects
exclude_paths: []
log_level: INFO
log_file: ~/.projectpruner/projectpruner.log
```

## How Configuration Affects Clean and Archive

- **archive.compression**: Compression algorithm for archives (`xz` or `gz`).
- **archive.archive_dir**: Where archives are stored.
- **clean.patterns**: What gets removed by `clean` and before `archive`.
- **search_paths**: Used for reference, but you now specify the parent directory directly in the CLI.
- **log_level, log_file**: Control logging output.

## Environment Variables

You can override config values with environment variables:
- `PROJECTPRUNER_ARCHIVE_DIR`
- `PROJECTPRUNER_COMPRESSION`
- `PROJECTPRUNER_COMPRESSION_LEVEL`
- `PROJECTPRUNER_LOG_LEVEL`
- `PROJECTPRUNER_LOG_FILE`

## No More 'find' or Legacy Commands

All cleaning and archiving is now done via the `clean` and `archive` commands. You do not need to use command substitution or scripting for batch operations.

## Configuration Methods

Project Pruner can be configured using:
1. Configuration file (YAML)
2. Environment variables
3. Command-line options

## Configuration File

By default, Project Pruner looks for `config.yaml` in your current directory. You can specify a custom location using the `--config` option. If neither is found, it falls back to `~/.projectpruner/config.yaml`.

### Example Configuration

```yaml
# Archive settings
archive:
  compression: xz  # Compression algorithm (xz, gz)
  compression_level: 3  # Compression level (1-9)
  archive_dir: ~/.projectpruner/archives  # Archive storage directory
  date_format: "%Y-%m-%d"  # Date format for archive names

# Cleaning settings
clean:
  patterns:  # Patterns to clean
    - "**/node_modules"
    - "**/vendor"
    - "**/dist"
    - "**/build"
    - "**/__pycache__"
    - "**/*.pyc"
    - "**/*.pyo"
    - "**/*.pyd"
    - "**/.DS_Store"
    - "**/Thumbs.db"

  exclude_patterns:  # Patterns to exclude from cleaning
    - "**/node_modules/.bin"
    - "**/vendor/bin"

  min_size: 1024  # Minimum file size to clean (in bytes)

# Search settings
search_paths:  # Directories to search for projects
  - ~/projects
  - ~/workspace
  - ~/code

exclude_paths:  # Directories to exclude from search
  - ~/projects/archive
  - ~/workspace/archive

# Logging settings
log_level: INFO  # Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
log_file: ~/.projectpruner/projectpruner.log  # Log file path
```

## Environment Variables

You can configure Project Pruner using environment variables:

### Archive Settings

- `PROJECTPRUNER_ARCHIVE_DIR`: Archive storage directory
- `PROJECTPRUNER_COMPRESSION`: Compression algorithm (xz, gz)
- `PROJECTPRUNER_COMPRESSION_LEVEL`: Compression level (1-9)

### Cleaning Settings

- `PROJECTPRUNER_CLEAN_PATTERNS`: Comma-separated list of patterns to clean
- `PROJECTPRUNER_CLEAN_EXCLUDE_PATTERNS`: Comma-separated list of patterns to exclude

### Search Settings

- `PROJECTPRUNER_SEARCH_PATHS`: Colon-separated list of directories to search
- `PROJECTPRUNER_EXCLUDE_PATHS`: Colon-separated list of directories to exclude

### Logging Settings

- `PROJECTPRUNER_LOG_LEVEL`: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `PROJECTPRUNER_LOG_FILE`: Log file path

## Command-line Options

### Global Options

- `--config`: Path to configuration file
- `--dry-run`: Preview changes without making them

### Find Command Options

- `--older-than`: Find projects older than specified duration
- `--larger-than`: Find projects larger than specified size
- `--pattern`: Find projects matching specified pattern

### Clean Command Options

- `--pattern`: Additional patterns to clean
- `--exclude`: Additional patterns to exclude

### Archive Command Options

- `--compress`: Compression algorithm to use
- `--clean`: Clean project before archiving

### Restore Command Options

- `--destination`: Destination path for restored project

## Configuration Precedence

1. Command-line options
2. Environment variables
3. Configuration file
4. Default values

## Best Practices

1. Use configuration file for static settings
2. Use environment variables for sensitive settings
3. Use command-line options for one-off changes
4. Keep configuration file in version control
5. Document custom patterns and exclusions
6. Regularly review and update configuration
7. Test configuration changes with `--dry-run`
8. Back up configuration before major changes
9. Use appropriate compression levels
10. Monitor log file size and rotation
