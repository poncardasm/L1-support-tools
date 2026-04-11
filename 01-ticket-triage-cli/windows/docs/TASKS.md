# Ticket Triage CLI — Tasks (Windows)

## Phase 1: Project Skeleton

- [x] Create `pyproject.toml` with Click + PyYAML + requests deps (requests optional, for `--llm`)
- [x] Create `ticket_triage/__init__.py` with version
- [x] Create `ticket_triage/__main__.py` for `python -m ticket_triage` entry
- [x] Create `tests/test_triage.py` with empty test class
- [x] Create `.gitignore`
- [x] Verify `pip install -e .` works and `ticket-triage --help` prints
- [x] Test PowerShell pipe: `Get-Content ticket.txt | ticket-triage` (placeholder works)

---

## Phase 2: Rule Engine + Core Logic

- [ ] Create `ticket_triage/rules.yaml` with all 8 categories (include `suggested_action` field per category)
- [ ] Implement `ticket_triage/triage.py`:
  - `load_rules()` — load YAML, merge user config from `%APPDATA%`
  - `TriageResult` namedtuple
  - `triage()` — main function
  - `score_priority()` — P1 override logic, urgency modifiers, priority bump
  - `score_confidence()` — confidence based on keyword match count and category overlap
  - `check_escalation()` — flag conditions
- [ ] Verify all 8 categories match via keyword tests
- [ ] Verify P1 override words bump priority correctly
- [ ] Verify escalation flags fire on known L2 patterns

---

## Phase 3: CLI Interface

- [ ] Implement main Click command with `--file`, `--llm`, `--json`, `--version` flags
- [ ] Implement stdin detection via `sys.stdin.isatty()`
- [ ] Route input: file → stdin → error
- [ ] Implement text output formatter
- [ ] Implement JSON output formatter
- [ ] Implement exit codes (0, 1, 2)
- [ ] Test: `Get-Content ticket.txt | ticket-triage` works
- [ ] Test: `ticket-triage --file C:\tickets\ticket.txt` works
- [ ] Test: `ticket-triage --json` outputs valid JSON
- [ ] Test: empty stdin exits with code 1

---

## Phase 4: LLM Mode (if Ollama available)

- [ ] Implement `ollama_triage()` function
- [ ] Wire `--llm` flag: rule engine → LLM refinement fallback chain
- [ ] Test: `--llm` with Ollama running returns refined result
- [ ] Test: `--llm` with Ollama down falls back to rule engine silently
- [ ] Add `requests` as optional dependency in `pyproject.toml` (only installed for LLM mode)
- [ ] Mock Ollama responses in tests for CI environments without Ollama

---

## Phase 5: Config Override

- [ ] Implement `%APPDATA%\ticket-triage\rules.yaml` merge
- [ ] Test: user rules override defaults

---

## Phase 6: Test Suite

- [ ] All Phase 2-5 tests passing
- [ ] Add fixtures: `tests/fixtures/*.txt` — one ticket per category
- [ ] Add confidence scoring tests (High/Medium/Low)
- [ ] Run full suite: `pytest tests/ -v`

---

## Phase 7: Windows Build

- [ ] Create `ticket-triage.spec` for PyInstaller
- [ ] Build standalone executable: `pyinstaller ticket-triage.spec`
- [ ] Test: `dist\ticket-triage.exe --help` works
- [ ] Test: `Get-Content ticket.txt | .\dist\ticket-triage.exe` works
- [ ] Create `build.ps1` for automated builds

---

## Phase 8: Docs + Polish

- [ ] Write `README.md` with Windows install instructions + usage examples
- [ ] Add PowerShell-specific examples
- [ ] Add `--help` docstring and Click built-in help
- [ ] Tag v1.0.0 git tag

---

## Phase 9: Publish

- [ ] Push to GitHub
- [ ] Attach `.exe` to GitHub Release
- [ ] Optional: publish to PyPI
