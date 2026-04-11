# Diagnostic Collector — Tasks (Windows)

## Phase 1: Project Skeleton

- [ ] Create main `diag-collect.ps1` script
- [ ] Create `modules/` directory structure
- [ ] Create `formatters/` directory structure
- [ ] Test basic script execution

---

## Phase 2: Collector Modules

- [ ] Implement `Get-SystemInfo.ps1`
- [ ] Implement `Get-DiskInfo.ps1` with threshold detection
- [ ] Implement `Get-NetworkInfo.ps1`
- [ ] Implement `Get-ServiceInfo.ps1`
- [ ] Implement `Get-EventLogInfo.ps1`
- [ ] Implement `Get-InstalledSoftwareInfo.ps1`
- [ ] Implement `Get-UpdateInfo.ps1`
- [ ] Implement `Get-ActiveUsersInfo.ps1`
- [ ] Implement `Get-NetworkTests.ps1`

---

## Phase 3: Formatters

- [ ] Implement `Format-Markdown.ps1`
- [ ] Implement `Format-Html.ps1`
- [ ] Implement `Format-Json.ps1`

---

## Phase 4: Thresholds

- [ ] Implement disk space threshold detection (80%, 90%)
- [ ] Implement memory threshold detection (90%)
- [ ] Flag pending security updates
- [ ] Flag failed services

---

## Phase 5: Upload Feature

- [ ] Implement `--upload` option
- [ ] Support configurable endpoint
- [ ] Handle authentication

---

## Phase 6: Testing

- [ ] Create Pester test suite
- [ ] Test threshold detection
- [ ] Test all collectors
- [ ] Test formatters

---

## Phase 7: Documentation

- [ ] Write `README.md`
- [ ] Document all collected data
- [ ] Add usage examples

---

## Phase 8: Distribution

- [ ] Host script for `Invoke-WebRequest | Invoke-Expression`
- [ ] Create signed version (optional)
- [ ] Push to GitHub
