# Log Dump Parser — Implementation Plan

## 1. Project Setup

```
log-dump-parser/
├── pyproject.toml
├── log_parse/
│   ├── __init__.py
│   ├── __main__.py
│   ├── parser.py         # core parsing engine
│   ├── formatters.py     # output formatting
│   ├── patterns.yaml     # common pattern library
│   └── patterns/
│       ├── syslog.py
│       ├── windows_event.py
│       ├── json_lines.py
│       └── apache.py
├── tests/
│   ├── fixtures/          # sample log files per format
│   └── test_parser.py
└── README.md
```

Dependencies: `click`, `pyyaml`, `python-dateutil`, `re` (stdlib)

## 2. Format Detection (parser.py)

Auto-detect format from first 10 lines:

```python
def detect_format(sample_lines: list[str]) -> str:
    for line in sample_lines[:10]:
        if line.startswith('<Event>'): return 'windows_event'
        if re.match(r'\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}', line): return 'syslog'
        if line.startswith('{') and json.loads(line): return 'json_lines'
        if re.match(r'\d+\.\d+\.\d+\.\d+.*\[.*\]', line): return 'apache'
    return 'plain_text'
```

## 3. Pattern Library (patterns.yaml)

```yaml
error_patterns:
  - pattern: "Connection refused to (\\w+):(\\d+)"
    severity: ERROR
    suggestion: "Check if {0} service is running (systemctl status {0})"
  - pattern: "Authentication failure for user (\\w+)"
    severity: ERROR
    suggestion: "Review failed login audit log (auth.log)"
  - pattern: "Disk space threshold exceeded on (.+)"
    severity: ERROR
    suggestion: "Run `df -h` on {0}"
  - pattern: "Permission denied"
    severity: ERROR
    suggestion: "Check file permissions with `ls -la`"

warning_patterns:
  - pattern: "Session token expired"
    severity: WARN
  - pattern: "Retry attempt for external API"
    severity: WARN
  - pattern: "Memory usage above \\d+%"
    severity: WARN
    suggestion: "Check `free -h` and top processes"
```

Pattern matching: compile regex once at startup, store in dict keyed by pattern string.

## 4. Core Parsing Loop

```python
def parse_log(lines: Iterator[str], format: str) -> ParseResult:
    matched = []
    unknown_lines = []
    
    for line_num, line in enumerate(lines, 1):
        line = line.rstrip()
        if not line:
            continue
        
        # Skip malformed lines
        try:
            parsed = PARSERS[format].parse_line(line)
        except Exception:
            unknown_lines.append((line_num, line))
            continue
        
        for pattern in patterns:
            if pattern['compiled'].search(parsed.get('message', '')):
                matched.append({
                    'pattern': pattern['name'],
                    'severity': pattern['severity'],
                    'message': pattern['compiled'].search(parsed.get('message', '')).group(0),
                    'timestamp': parsed.get('timestamp'),
                    'source': parsed.get('source', 'unknown'),
                    'line_num': line_num,
                })
                break
    
    return ParseResult(matched, unknown_lines, len(lines))
```

Use `collections.Counter` for frequency grouping:

```python
from collections import Counter
error_counts = Counter((m['pattern'], m['message']) for m in errors)
top_errors = error_counts.most_common(10)
```

## 5. Time Filtering

Parse timestamps with `dateutil.parser` for flexibility:

```python
from dateutil import parser as date_parser

def parse_timestamp(ts_str: str) -> datetime:
    return date_parser.parse(ts_str, fuzzy=True)

def is_in_range(timestamp, since, until) -> bool:
    if since and timestamp < since: return False
    if until and timestamp > until: return False
    return True
```

Relative time parsing (e.g. "1 hour ago"):

```python
from dateutil.relativedelta import relativedelta

RELATIVE_UNITS = {
    'minute': relativedelta(minutes=1),
    'hour': relativedelta(hours=1),
    'day': relativedelta(days=1),
    'week': relativedelta(weeks=1),
}

def parse_relative(s: str) -> datetime:
    m = re.match(r'(\d+)\s+(minute|hour|day|week)s?\s+ago', s)
    if m:
        return now() - RELATIVE_UNITS[m.group(2)] * int(m.group(1))
    raise ValueError(f"Cannot parse relative time: {s}")
```

## 6. Output Formatters (formatters.py)

### Text (default)

```
[ERRORS — {n} total]
  {count:4dx} {pattern_name} {message}
```

### JSON

```json
{
  "file": "system.log",
  "lines_parsed": 14232,
  "errors": [{"count": 12, "pattern": "...", "first_seen": "ISO8601"}],
  "warnings": [...],
  "stats": {"time_range": {"start": "...", "end": "..."}},
  "suggestions": [...]
}
```

### CSV

```csv
severity,count,pattern,message,first_seen,last_seen
ERROR,12,Connection refused,Connection refused to db:5432,2024-03-01T09:00:00,2024-03-01T09:45:00
```

## 7. Per-Format Parsers

### 7.1 Syslog

```python
SYSLOG_RE = re.compile(
    r'(?P<timestamp>\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+'
    r'(?P<host>\S+)\s+'
    r'(?P<process>\S+?)(?:\[(?P<pid>\d+)\])?:\s+'
    r'(?P<message>.+)'
)
```

### 7.2 Windows Event XML

```python
from xml.etree import ElementTree as ET

def parse_windows_event(line: str) -> dict:
    root = ET.fromstring(line)
    ns = {'e': 'http://schemas.microsoft.com/win/2004/08/events/event'}
    return {
        'timestamp': root.findtext('.//e:TimeCreated', '', ns),
        'level': root.findtext('.//e:Level', '', ns),
        'source': root.findtext('.//e:Provider', '', ns),
        'message': root.findtext('.//e:Data', '', ns),
    }
```

### 7.3 JSON Lines

```python
def parse_json_line(line: str) -> dict:
    obj = json.loads(line)
    return {
        'timestamp': obj.get('time') or obj.get('timestamp') or obj.get('@timestamp'),
        'level': obj.get('level') or obj.get('severity'),
        'message': obj.get('message') or obj.get('log') or obj.get('msg'),
        'source': obj.get('source') or obj.get('logger'),
    }
```

### 7.4 Apache/Nginx

```python
APACHE_RE = re.compile(
    r'(?P<ip>\S+)\s+\S+\s+\S+\s+\[(?P<ts>[^\]]+)\]\s+'
    r'"(?P<method>\S+)\s+(?P<path>\S+)\s+(?P<proto>\S+)"\s+'
    r'(?P<status>\d+)\s+(?P<size>\S+)'
)
```

## 8. Performance

- Stream input line-by-line — never load full file into memory
- Compile all regex patterns once at startup (stored in `patterns.py`)
- Counter aggregation is O(n) with minimal overhead
- Target: 10k lines in < 2 seconds on a commodity VPS

```python
# Stream large files:
with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
    # f is an iterator — don't call f.read()
    for line in f:
        ...
```

## 9. Known Pitfalls

1. **Encoding issues** — logs may be Latin-1 or UTF-16. Use `encoding='utf-8', errors='ignore'` as default, add `--encoding` flag for explicit override.
2. **Malformed lines** — always wrap `parse_line()` in try/except. Never crash on a single bad line.
3. **Multi-line stack traces** — these typically follow an error line and are indented. Group indented continuation lines with the preceding error.
4. **Timestamp ambiguity** — syslog omits year. Infer from file mtime or current year if timestamp is in the future.
5. **Pattern explosion** — don't run every pattern against every line. Use a fast pre-filter: if the line doesn't contain any keyword from any pattern, skip regex entirely.
