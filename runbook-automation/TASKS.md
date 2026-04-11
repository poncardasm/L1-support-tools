# Runbook Automation — Tasks

## Phase 1: Skeleton

- [ ] Create `pyproject.toml` with `click`, `mistune`, `pyyaml`
- [ ] Create `runbook/__init__.py` with `__version__`
- [ ] Create `runbook/__main__.py` entry point
- [ ] Create `tests/test_parser.py` with empty test class
- [ ] Create `.gitignore`
- [ ] Create `runbooks/` directory structure (authentication, infrastructure subdirs)
- [ ] Verify `pip install -e .` works + `runbook --help` prints

---

## Phase 2: Parser

- [ ] Implement `extract_steps()` — parse Markdown, extract fenced bash code blocks
- [ ] Implement `extract_title_before()` — grab text preceding each code block
- [ ] Step namedtuple: number, language, command, title
- [ ] Test: runbook with 5 steps extracts all 5 commands correctly
- [ ] Test: non-bash code blocks (Python, YAML) are NOT extracted as steps
- [ ] Test: title extraction from Markdown structure

---

## Phase 3: Executor

- [ ] Implement `run_step()` with `subprocess.run()` and timeout
- [ ] Implement `execute_runbook()` — loop all steps, stop on non-zero exit
- [ ] Implement interactive prompt on error (s/f/a options)
- [ ] Wire `--dry-run` flag
- [ ] Test: non-zero exit stops execution and prompts
- [ ] Test: `--dry-run` prints commands without executing
- [ ] Test: `--dry-run` does NOT call subprocess at all

---

## Phase 4: Resume / From-Step

- [ ] Implement `save_state()` — write JSON to `~/.runbook/state/`
- [ ] Implement `load_state()` — read state for a runbook
- [ ] Implement `clear_state()` — delete state after successful completion
- [ ] Wire `--from-step N` to executor
- [ ] Wire `--resume` to load saved state and set from-step
- [ ] Test: `--resume` loads correct step from state file
- [ ] Test: `--from-step 3` skips steps 1 and 2
- [ ] Test: state is cleared after full successful run

---

## Phase 5: Indexer

- [ ] Implement `list_runbooks()` — walk `runbooks/` directory, extract step counts
- [ ] Implement `search_runbooks()` — search name + content
- [ ] Wire `runbook list` and `runbook search` commands
- [ ] `--category` filter for `list`
- [ ] Test: `list` returns all runbooks with correct step counts
- [ ] Test: `search` finds runbooks by keyword in content and name

---

## Phase 6: Output Formatting

- [ ] Executing step prints: `[STEP N/M] <title>` then command output
- [ ] Dry-run step prints: `[DRY] <command>`
- [ ] Completion summary: N steps run, X succeeded, 1 failed at step Y
- [ ] Non-interactive (non-TTY) mode: exit code 1 on first failure without prompt

---

## Phase 7: Default Runbooks

- [ ] Create `runbooks/authentication/reset-vpn.md` with 4+ steps
- [ ] Create `runbooks/infrastructure/restart-postgresql.md` with 4+ steps
- [ ] Verify both runbooks pass `runbook run --dry-run`

---

## Phase 8: Testing

- [ ] Parser fixture tests: 5+ sample runbooks with varying step counts
- [ ] Executor tests: dry-run, stop-on-error, force-continue
- [ ] State tests: save, load, clear, resume
- [ ] Indexer tests: list, search, category filter
- [ ] `pytest tests/ -v` passes

---

## Phase 9: Docs + Polish

- [ ] `README.md` with install, write-your-own-runbook guide, all CLI options
- [ ] Tag v1.0.0
- [ ] Commit per project
