# Ticket Triage CLI — Tasks

## Phase 1: Project Skeleton

- [ ] Create `pyproject.toml` with Click + PyYAML deps
- [ ] Create `ticket_triage/__init__.py` with version
- [ ] Create `ticket_triage/__main__.py` for `python -m ticket_triage` entry
- [ ] Create `tests/test_triage.py` with empty test class
- [ ] Create `.gitignore`
- [ ] Verify `pip install -e .` works and `ticket-triage --help` prints

---

## Phase 2: Rule Engine + Core Logic

- [ ] Create `ticket_triage/rules.yaml` with all 8 categories
- [ ] Implement `ticket_triage/triage.py`:
  - `load_rules()` — load YAML, merge user config
  - `TriageResult` namedtuple
  - `triage()` — main function
  - `score_priority()` — P1 override logic
  - `check_escalation()` — flag conditions
- [ ] Verify all 8 categories match via keyword tests
- [ ] Verify P1 override words bump priority correctly
- [ ] Verify escalation flags fire on known L2 patterns

---

## Phase 3: CLI Interface

- [ ] Implement main Click command with `--file`, `--llm`, `--json` flags
- [ ] Implement stdin detection via `sys.stdin.isatty()`
- [ ] Route input: file → stdin → error
- [ ] Implement text output formatter
- [ ] Implement JSON output formatter
- [ ] Implement exit codes (0, 1, 2)
- [ ] Test: `cat ticket.txt | ticket-triage` works
- [ ] Test: `ticket-triage --file /path/to/ticket.txt` works
- [ ] Test: `ticket-triage --json` outputs valid JSON
- [ ] Test: empty stdin exits with code 1

---

## Phase 4: LLM Mode (if Ollama available)

- [ ] Implement `ollama_triage()` function
- [ ] Wire `--llm` flag: rule engine → LLM refinement fallback chain
- [ ] Test: `--llm` with Ollama running returns refined result
- [ ] Test: `--llm` with Ollama down falls back to rule engine silently

---

## Phase 5: Config Override

- [ ] Implement `~/.config/ticket-triage/rules.yaml` merge
- [ ] Test: user rules override defaults

---

## Phase 6: Test Suite

- [ ] All Phase 2-5 tests passing
- [ ] Add fixtures: `tests/fixtures/*.txt` — one ticket per category
- [ ] Run full suite: `pytest tests/ -v`

---

## Phase 7: Docs + Polish

- [ ] Write `README.md` with install instructions + usage examples
- [ ] Add `--help` docstring and Click built-in help
- [ ] Tag v1.0.0 git tag

---

## Phase 8: Publish

- [ ] Push to GitHub
- [ ] Optional: publish to PyPI
