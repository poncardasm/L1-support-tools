# Log Dump Parser — Tasks (macOS)

## Phase 1: Project Skeleton

- [ ] Create `pyproject.toml` with dependencies
- [ ] Create `log_parse/__init__.py`
- [ ] Create `log_parse/__main__.py`
- [ ] Verify `pip install -e .` works

---

## Phase 2: Format Detection

- [ ] Implement file format detection
- [ ] Detect syslog format
- [ ] Detect journald JSON export
- [ ] Detect JSON Lines
- [ ] Detect Docker container logs
- [ ] Detect Apache/Nginx logs
- [ ] Fallback to plain text

---

## Phase 3: Parsers

- [ ] Implement syslog parser
- [ ] Implement journald parser
- [ ] Implement JSON Lines parser
- [ ] Implement Docker parser
- [ ] Implement plain text parser

---

## Phase 4: Analysis

- [ ] Implement error/warning grouping
- [ ] Implement message normalization
- [ ] Implement frequency counting
- [ ] Implement statistics calculation

---

## Phase 5: Filters

- [ ] Implement `--level` filter
- [ ] Implement `--since` time filter
- [ ] Implement `--until` time filter
- [ ] Implement `--source` filter
- [ ] Implement `--grep` search

---

## Phase 6: Output Formats

- [ ] Implement text output
- [ ] Implement JSON output
- [ ] Implement CSV output

---

## Phase 7: CLI

- [ ] Implement main Click command
- [ ] Implement all options
- [ ] Test stdin input

---

## Phase 8: Testing

- [ ] Create test fixtures
- [ ] Test format detection
- [ ] Test parsing
- [ ] Test analysis

---

## Phase 9: Homebrew Packaging

- [ ] Create `Formula/log-parse.rb`
- [ ] Test Homebrew installation

---

## Phase 10: Documentation

- [ ] Write `README.md`
- [ ] Document Unix-specific log formats
- [ ] Add usage examples

---

## Phase 11: Publish

- [ ] Push to GitHub
- [ ] Optional: PyPI
