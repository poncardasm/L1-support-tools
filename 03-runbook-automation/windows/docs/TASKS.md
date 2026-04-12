# Runbook Automation — Tasks (Windows)

## Phase 1: Project Skeleton

- [x] Create PowerShell module structure (`runbook.psd1`, `runbook.psm1`)
- [x] Create `public/` directory
- [x] Create `private/` directory
- [x] Create `runbooks/` directory
- [x] Verify `Import-Module ./runbook.psd1` works

---

## Phase 2: Markdown Parsing

- [x] Implement `Parse-MarkdownSteps.ps1`
- [x] Extract `powershell` and `pwsh` code blocks
- [x] Handle step numbering

---

## Phase 3: Step Execution

- [x] Implement `Invoke-Step.ps1`
- [x] Execute PowerShell code
- [x] Capture output and exit code
- [x] Handle errors

---

## Phase 4: Runbook Execution

- [ ] Implement `Invoke-Runbook.ps1`
- [ ] Execute steps in sequence
- [ ] Handle `--dry-run` mode
- [ ] Handle `--from-step` option
- [ ] Handle `--resume` option

---

## Phase 5: State Management

- [ ] Implement `Save-RunbookState.ps1`
- [ ] Implement `Get-RunbookState.ps1`
- [ ] Store state in `%APPDATA%\runbook\state\`

---

## Phase 6: Error Handling

- [ ] Implement prompt on failure
- [ ] Skip, force continue, abort options
- [ ] Handle Ctrl+C gracefully

---

## Phase 7: Runbook Index

- [ ] Implement `Get-RunbookList.ps1`
- [ ] Implement `Search-Runbook.ps1`
- [ ] Support category filtering

---

## Phase 8: Testing

- [ ] Create Pester test suite
- [ ] Create sample runbook fixtures
- [ ] Test parsing
- [ ] Test execution
- [ ] Test state management

---

## Phase 9: Documentation

- [ ] Write `README.md`
- [ ] Document runbook format
- [ ] Add PowerShell-specific examples

---

## Phase 10: Sample Runbooks

- [ ] Create sample runbooks for common Windows tasks
- [ ] IIS restart
- [ ] Service restart
- [ ] Event log clearing

---

## Phase 11: Publish

- [ ] Push to GitHub
- [ ] Optional: publish to PowerShell Gallery
