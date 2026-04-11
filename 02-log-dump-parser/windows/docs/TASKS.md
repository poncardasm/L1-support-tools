# Log Dump Parser — Tasks (Windows)

## Phase 1: Project Skeleton

- [ ] Create `pyproject.toml` with dependencies (click, python-evtx)
- [ ] Create `log_parse/__init__.py`
- [ ] Create `log_parse/__main__.py`
- [ ] Verify `pip install -e .` works

---

## Phase 2: Format Detection

- [ ] Implement file format detection
- [ ] Detect Windows Event Log (.evtx)
- [ ] Detect Windows Event XML
- [ ] Detect JSON Lines
- [ ] Detect IIS log format
- [ ] Fallback to plain text

---

## Phase 3: Parsers

- [ ] Implement EVTX parser (python-evtx)
- [ ] Implement JSON Lines parser
- [ ] Implement IIS log parser
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

- [ ] Create test fixtures (sample EVTX, JSON)
- [ ] Test format detection
- [ ] Test parsing
- [ ] Test analysis

---

## Phase 9: Windows Build

- [ ] Create PyInstaller spec
- [ ] Build standalone executable
- [ ] Test `log-parse.exe`

---

## Phase 10: Documentation

- [ ] Write `README.md`
- [ ] Document Windows-specific log formats
- [ ] Add usage examples
