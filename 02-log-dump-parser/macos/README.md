# log-parse

A CLI tool that takes a raw log file (any format: Syslog, journald, application log, Apache, Nginx, Docker, Kubernetes, JSON logs) and returns a cleaned, structured summary of errors and warnings grouped by frequency and severity.

**Target feel:** a senior sysadmin sitting next to you saying "here's what's actually wrong — ignore the noise."

## Installation

### macOS via Homebrew

```bash
brew tap mchael/tools
brew install log-parse
```

### From Source

```bash
git clone https://github.com/mchael/log-parse.git
cd log-parse
pip install -e .
```

## Usage

### Basic Usage

```bash
# Parse a syslog file
log-parse /var/log/system.log

# Parse with format auto-detection
log-parse application.log

# Parse from stdin
cat /var/log/syslog | log-parse -
```

### Supported Formats

| Format | Auto-detected by |
|--------|------------------|
| Syslog (RFC 3164/5424) | timestamp + hostname + process pattern |
| journald (JSON export) | `__CURSOR` field |
| JSON Lines | one JSON object per line |
| Apache/Nginx access | IP + timestamp + request pattern |
| Docker/containerd | JSON with `log` field |
| Plain text (fallback) | best-effort regex extraction |

### Filters

```bash
# Filter by level
log-parse --level ERROR,WARN application.log

# Filter by time range
log-parse --since "2024-01-01 00:00:00" --until "2024-01-02 00:00:00" application.log

# Filter by source/process
log-parse --source nginx access.log

# Search within messages
log-parse --grep "connection refused" application.log

# Show only top N patterns
log-parse --top 5 application.log
```

### Output Formats

```bash
# JSON output for pipelines
log-parse --json application.log | jq '.analysis.errors'

# CSV output for Excel/Sheets
log-parse --csv application.log > report.csv

# Save to file
log-parse -o report.txt application.log
```

## Example Output

```
=== Log Summary ===
File: /var/log/system.log
Format: syslog
Lines parsed: 14,232 | Filtered: 14,232
Errors: 23 | Warnings: 87

[ERRORS — 23 total]
  12x Connection refused to db:5432
   7x Authentication failure for user admin
   4x Disk space threshold exceeded on /dev/sda1

[WARNINGS — 87 total]
  40x Session token expired (idle timeout)
  22x Retry attempt for external API call
  15x Memory usage above 80%

[STATISTICS]
  Time range: 2024-03-01 09:00:00 → 2024-03-01 17:30:00
  Top sources:
    sshd: 143 entries
    postgres: 45 entries
    nginx: 38 entries

[SUGGESTED ACTIONS]
  - "Connection refused to db:5432" → Check if the target service is running and accessible
  - "Authentication failure" → Review credentials and authentication configuration
  - "Disk space threshold" → Free up disk space or expand storage
```

## Unix-Specific Log Formats

### Syslog (RFC 3164/5424)

Standard Unix system logs with format:
```
Jan 15 10:30:45 hostname process[pid]: message
```

Examples:
```bash
log-parse /var/log/syslog
log-parse /var/log/messages
log-parse /var/log/auth.log
```

### journald (systemd)

Modern Linux systems using systemd can export logs via:
```bash
journalctl --since "1 hour ago" --output json > logs.json
log-parse logs.json
```

### Docker Container Logs

Docker JSON logs with `docker logs --timestamps`:
```bash
docker logs container_name 2>&1 | log-parse -
```

Or parse exported logs:
```bash
log-parse /var/lib/docker/containers/.../container.log
```

## Development

```bash
# Setup
cd log-parse
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run on sample data
log-parse tests/fixtures/syslog.log
log-parse tests/fixtures/json_lines.log --json
```

## License

MIT
