# Bulk Action Runner — Tasks (macOS)

## Phase 1: Project Skeleton

- [x] Create `pyproject.toml` with msgraph-sdk + azure-identity deps
- [x] Create `bulk/__init__.py` with version
- [x] Create `bulk/__main__.py` for CLI entry
- [x] Verify `pip install -e .` works and `bulk-run --help` prints

---

## Phase 2: CSV Parsing

- [ ] Implement CSV reader with `csv.DictReader`
- [ ] Handle missing columns gracefully
- [ ] Support both comma and semicolon delimiters

---

## Phase 3: Operations

- [ ] Implement `password-reset` operation
- [ ] Implement `add-group` operation
- [ ] Implement `enable-mailbox` operation
- [ ] Implement `deprovision` operation
- [ ] All commands support `--dry-run`

---

## Phase 4: Throttling

- [ ] Implement 500ms delay between rows
- [ ] Test with 100-row CSV
- [ ] Verify no 429 errors from Graph API

---

## Phase 5: Reporting

- [ ] Implement `--report` CSV output
- [ ] Include all 5 columns
- [ ] Test report generation

---

## Phase 6: Testing

- [ ] Create `tests/test_operations.py`
- [ ] Create test fixture CSV files
- [ ] Test `--dry-run` mode

---

## Phase 7: Homebrew Packaging

- [ ] Create `Formula/bulk-run.rb`
- [ ] Test Homebrew installation

---

## Phase 8: Documentation

- [ ] Write `README.md`
- [ ] Document CSV format
- [ ] Add troubleshooting section

---

## Phase 9: Publish

- [ ] Push to GitHub
- [ ] Optional: publish to PyPI
