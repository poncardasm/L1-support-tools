# Bulk Action Runner — Tasks

## Phase 1: Skeleton

- [ ] Create `pyproject.toml` with `click`, `azure-identity`, `msgraph-sdk`, `pandas`, `python-dotenv`, `tqdm`
- [ ] Create `bulk/__init__.py`
- [ ] Create `bulk/__main__.py` entry point (`bulk-run`)
- [ ] Create `tests/test_operations.py` with empty test class
- [ ] Create `.gitignore` (exclude `creds.env`, `__pycache__/`)
- [ ] Verify `pip install -e .` works + `bulk-run --help` prints

---

## Phase 2: Config + Graph Client

- [ ] Implement creds loading from `~/.config/bulk-action/creds.env`
- [ ] Implement `get_graph_client()` using ClientSecretCredential
- [ ] Create `creds.env.example` as template (no real values)
- [ ] Test: missing creds file exits with helpful message
- [ ] Test: `creds.env.example` exists and has correct keys

---

## Phase 3: Operation Registry + Row Processing

- [ ] Implement `OPERATIONS` registry dict with all 4 operations
- [ ] Implement `process_row()` — dispatch to correct operation per row
- [ ] Implement `RowResult` namedtuple: email, operation, result, detail, timestamp
- [ ] Wire dry-run mode: Graph API NOT called when `--dry-run`
- [ ] Test: each operation returns RowResult with correct result field

---

## Phase 4: Operations

- [ ] Implement `reset_password()` — set temp password + force change flag
- [ ] Implement `add_to_group()` — resolve email to user_id, group name to group_id, add member
- [ ] Implement `enable_mailbox()` — enable Exchange Online mailbox via Graph
- [ ] Implement `deprovision_user()` — disable account, remove group memberships
- [ ] Rate limiting: 500ms sleep between rows (`--delay-ms` flag override)
- [ ] Test: all 4 operations in dry-run mode: no Graph API calls made
- [ ] Test: all 4 operations in live mode: correct Graph endpoints called

---

## Phase 5: CSV Processing

- [ ] Implement `read_csv()` — parse CSV with `csv.DictReader`
- [ ] Implement `run_batch()` — process all rows with tqdm progress bar
- [ ] Validate: CSV must have `email` column (fail fast if missing)
- [ ] Implement `--delay-ms` flag for rate limit tuning
- [ ] Test: CSV with 100 rows processes all 100 in < 70 seconds (500ms delay)
- [ ] Test: empty CSV exits cleanly with message

---

## Phase 6: Reporting

- [ ] Implement `write_report()` — export results to CSV with all 5 columns
- [ ] Wire `--report <output.csv>` to save results
- [ ] Test: output CSV opens in spreadsheet with correct columns
- [ ] Test: `--report` works combined with `--dry-run` (shows planned results)

---

## Phase 7: Error Handling

- [ ] Graph API errors: captured per row, logged to detail, batch continues
- [ ] 429 rate limit handling: back off 60s, retry once, fail row if persists
- [ ] Duplicate group membership: mark as "already member", not failure
- [ ] Missing required `--group` / `--reason`: exit with error before processing
- [ ] Test: one bad row in 100-row CSV: 99 processed, 1 failed, exit code 1

---

## Phase 8: Testing

- [ ] All 4 operation tests with mocked Graph client
- [ ] Dry-run tests: verify no Graph API calls
- [ ] CSV validation tests: missing email column, empty file
- [ ] Report generation tests: CSV output matches RowResult fields
- [ ] Rate limiting tests: delay fires correctly between rows
- [ ] `pytest tests/ -v` passes

---

## Phase 9: Docs + Polish

- [ ] `README.md` with install, CSV format docs, all operations, --dry-run, --report examples
- [ ] Tag v1.0.0
- [ ] Commit per project
