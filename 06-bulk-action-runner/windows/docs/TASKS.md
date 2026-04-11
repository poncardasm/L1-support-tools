# Bulk Action Runner — Tasks (Windows)

## Phase 1: Project Skeleton

- [ ] Create PowerShell module structure (`bulk-run.psd1`, `bulk-run.psm1`)
- [ ] Create `public/` directory with empty function files
- [ ] Create `private/` directory for helpers
- [ ] Verify `Import-Module ./bulk-run.psd1` works

---

## Phase 2: CSV Parsing

- [ ] Test `Import-Csv` with sample CSV files
- [ ] Handle missing columns gracefully
- [ ] Support both comma and semicolon delimiters

---

## Phase 3: Operations

- [ ] Implement `Invoke-BulkPasswordReset`
- [ ] Implement `Invoke-BulkAddGroup`
- [ ] Implement `Invoke-BulkEnableMailbox`
- [ ] Implement `Invoke-BulkDeprovision`
- [ ] All commands support `-WhatIf`

---

## Phase 4: Throttling

- [ ] Implement `Start-Throttle` helper
- [ ] Configure 500ms delay between rows
- [ ] Test with 100-row CSV

---

## Phase 5: Reporting

- [ ] Implement `--report` CSV output
- [ ] Include all 5 columns: email, operation, result, detail, timestamp
- [ ] Test report generation

---

## Phase 6: Testing

- [ ] Create Pester test suite
- [ ] Create test fixture CSV files
- [ ] Test `-WhatIf` mode for all operations

---

## Phase 7: Documentation

- [ ] Write `README.md` with PowerShell examples
- [ ] Document CSV format requirements
- [ ] Add troubleshooting section

---

## Phase 8: Publish

- [ ] Push to GitHub
- [ ] Optional: publish to PowerShell Gallery
