# Project Pruner Examples

## Basic Examples

### Clean (Clean Only)

Clean up build artifacts in all project folders under `/path/to/parent` not modified in the last 3 months (keeps the folders):
```bash
projectpruner clean /path/to/parent --until=3m
```

Clean only large projects:
```bash
projectpruner clean /path/to/parent --until=3m --larger-than=1GB
```

### Archive (Clean, Archive, Remove)

Clean, archive, and remove all project folders under `/path/to/parent` not modified in the last 6 months:
```bash
projectpruner archive /path/to/parent --until=6m
```

Archive only large projects:
```bash
projectpruner archive /path/to/parent --until=6m --larger-than=1GB
```

### Restore

Restore a project from an archive:
```bash
projectpruner restore /path/to/archive.tar.xz --destination /path/to/restore
```

## Advanced Examples

### Dry Run

Preview what would be cleaned or archived without making changes:
```bash
projectpruner clean /path/to/parent --until=3m --dry-run
projectpruner archive /path/to/parent --until=6m --dry-run
```

### Compression

Use maximum compression:
```bash
projectpruner archive /path/to/parent --until=6m --compress xz
```

Use fast compression:
```bash
projectpruner archive /path/to/parent --until=6m --compress gz
```

### Environment Variables

Set archive directory and compression via environment variables:
```bash
export PROJECTPRUNER_ARCHIVE_DIR=~/archives
export PROJECTPRUNER_COMPRESSION=xz
export PROJECTPRUNER_COMPRESSION_LEVEL=9
projectpruner archive /path/to/parent --until=6m
```

### Logging

Enable debug logging:
```bash
export PROJECTPRUNER_LOG_LEVEL=DEBUG
projectpruner archive /path/to/parent --until=6m
```

Custom log file:
```bash
export PROJECTPRUNER_LOG_FILE=/path/to/custom.log
projectpruner archive /path/to/parent --until=6m
```
