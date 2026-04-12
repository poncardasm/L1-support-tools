# Runbook Automation — Tasks (macOS)

## Phase 1: Project Skeleton

- [x] Create `pyproject.toml` with dependencies
- [x] Create `runbook/__init__.py`
- [x] Create `runbook/__main__.py`
- [x] Create `runbooks/` directory
- [x] Verify `pip install -e .` works

---

## Phase 2: Markdown Parsing

- [x] Implement `parse_runbook()` in `parser.py`
- [x] Extract `bash`, `sh`, `zsh` code blocks
- [x] Handle step numbering

---

## Phase 3: Step Execution

- [ ] Implement `execute_step()` in `executor.py`
- [ ] Execute shell commands
- [ ] Capture output and exit code
- [ ] Handle errors

---

## Phase 4: Runbook Execution

- [ ] Implement `execute_runbook()`
- [ ] Execute steps in sequence
- [ ] Handle `--dry-run` mode
- [ ] Handle `--from-step` option
- [ ] Handle `--resume` option

---

## Phase 5: State Management

- [ ] Implement `save_state()` and `load_state()`
- [ ] Store state in `~/.config/runbook/state/`

---

## Phase 6: Error Handling

- [ ] Implement prompt on failure
- [ ] Skip, force continue, abort options
- [ ] Handle Ctrl+C gracefully

---

## Phase 7: Runbook Index

- [ ] Implement `list_runbooks()`
- [ ] Implement `search_runbooks()`
- [ ] Support category filtering

---

## Phase 8: CLI

- [ ] Implement `run` command
- [ ] Implement `list` command
- [ ] Implement `search` command

---

## Phase 9: Testing

- [ ] Create test suite
- [ ] Create sample runbook fixtures
- [ ] Test parsing
- [ ] Test execution
- [ ] Test state management

---

## Phase 10: Homebrew Packaging

- [ ] Create `Formula/runbook.rb`
- [ ] Test Homebrew installation

---

## Phase 11: Documentation

- [ ] Write `README.md`
- [ ] Document runbook format
- [ ] Add bash/zsh-specific examples

---

## Phase 12: Sample Runbooks

- [ ] Create sample runbooks for common macOS tasks
- [ ] Service restart (brew services)
- [ ] Log clearing

---

## Phase 13: Publish

- [ ] Push to GitHub
- [ ] Optional: PyPI
- [ ] Optional: Homebrew tap
