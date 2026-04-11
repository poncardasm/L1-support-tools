# Log Dump Parser — Tasks

## Phase 1: Skeleton

- [ ] Create `pyproject.toml` with `click`, `pyyaml`, `python-dateutil`
- [ ] Create `log_parse/__init__.py` with `__version__`
- [ ] Create `log_parse/__main__.py` entry point
- [ ] Create `tests/test_parser.py` with empty test class
- [ ] Create `.gitignore`
- [ ] Verify `pip install -e .` works + `log-parse --help` prints

---

## Phase 2: Format Detection

- [ ] Implement `detect_format()` — scan first 10 lines for format signals
- [ ] Auto-detect: syslog, Windows Event XML, JSON Lines, Apache/Nginx, plain text
- [ ] Test: each format correctly detected from sample lines
- [ ] Test: mixed first lines returns first match

---

## Phase 3: Per-Format Parsers

- [ ] Implement `parse_syslog_line()` — timestamp, host, process, pid, message
- [ ] Implement `parse_windows_event_line()` — XML extraction
- [ ] Implement `parse_json_line()` — nested field extraction
- [ ] Implement `parse_apache_line()` — IP, timestamp, method, path, status
- [ ] Implement `parse_plain_text()` — fallback with best-effort extraction
- [ ] Verify all parsers pass fixture tests

---

## Phase 4: Pattern Engine

- [ ] Create `patterns.yaml` with 5+ error patterns and 3+ warning patterns
- [ ] Implement pattern compiler — compile regex once at startup
- [ ] Implement `match_line()` — run patterns against parsed message
- [ ] Implement pre-filter: skip lines with no keyword from any pattern
- [ ] Group matched errors by (pattern_name, message) using Counter
- [ ] Test: pattern matching correctly identifies known error messages
- [ ] Test: multi-line stack traces grouped with preceding error

---

## Phase 5: Filters

- [ ] Implement `--level ERROR,WARN` filter
- [ ] Implement `--since "1 hour ago"` relative time filter
- [ ] Implement `--until "2024-03-01"` absolute time filter
- [ ] Implement `--source nginx` process/source filter
- [ ] Implement `--grep "connection"` search filter
- [ ] Implement `--top 10` frequency limit
- [ ] Test: each filter independently on fixture data
- [ ] Test: multiple filters combined (AND logic)

---

## Phase 6: Output Formatters

- [ ] Implement text formatter with frequency counts + suggested actions
- [ ] Implement `--json` formatter — valid JSON with all fields
- [ ] Implement `--csv` formatter — flat CSV with headers
- [ ] Verify JSON output parses as valid JSON
- [ ] Verify CSV output opens correctly in spreadsheet

---

## Phase 7: Performance + Robustness

- [ ] Stream input: never call `.read()` on large files
- [ ] Malformed lines: wrap in try/except, increment skip counter, continue
- [ ] `--encoding` flag for Latin-1/UTF-16 override
- [ ] Test: 10k line file processes in < 2 seconds
- [ ] Test: encoding override works

---

## Phase 8: Testing

- [ ] Create `tests/fixtures/` with one sample log file per format
- [ ] All 6 format parsers tested
- [ ] Pattern engine tests: 10+ known error messages matched correctly
- [ ] Filter tests: all 6 filter types
- [ ] `pytest tests/ -v` passes

---

## Phase 9: Docs + Polish

- [ ] `README.md` with install, usage, format list, filter examples
- [ ] Tag v1.0.0
- [ ] Commit per project
