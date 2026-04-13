# AD/User Provisioning CLI — Tasks (Windows)

## Phase 1: Project Skeleton

- [x] Create PowerShell module structure (`ad-provision.psd1`, `ad-provision.psm1`)
- [x] Create `public/` directory with empty function files
- [x] Create `private/` directory for helper functions
- [x] Create `config/creds.env.example`
- [x] Verify `Import-Module ./ad-provision.psd1` works

---

## Phase 2: Microsoft Graph Integration

- [x] Install `Microsoft.Graph` and `ExchangeOnlineManagement` modules
- [x] Implement `Connect-GraphSession` in `private/`
- [x] Implement `Get-ProvisionConfig` for credential loading
- [x] Implement `Connect-ExchangeSession` for Exchange Online
- [x] Implement `New-TemporaryPassword` helper
- [x] Test connection to EntraID with certificate auth

---

## Phase 3: Core Commands

- [x] Implement `New-ADProvisionUser` in `public/`
- [x] Implement `Add-ADProvisionGroup` in `public/`
- [x] Implement `Enable-ADProvisionMailbox` in `public/`
- [x] Implement `Reset-ADProvisionPassword` in `public/`
- [x] Implement `Remove-ADProvisionUser` in `public/`
- [x] All commands support `-WhatIf` (dry-run)

---

## Phase 4: Output Formatting

- [x] Implement `Write-ProvisionOutput` helper
- [x] Consistent `[OK]`, `[FAIL]`, `[TEMP]`, `[WARN]` prefixes
- [x] Test output formatting in PowerShell console

---

## Phase 5: Testing

- [ ] Create Pester test suite in `tests/`
- [ ] Test `-WhatIf` mode for all commands
- [ ] Mock Graph API calls for unit tests
- [ ] Run `Invoke-Pester tests/`

---

## Phase 6: Documentation

- [ ] Write `README.md` with Windows-specific instructions
- [ ] Document credential setup (certificate-based auth)
- [ ] Add PowerShell command examples

---

## Phase 7: Installation

- [ ] Create installation script for module deployment
- [ ] Test module import on clean PowerShell session
- [ ] Document module installation path

---

## Phase 8: Publish

- [ ] Push to GitHub
- [ ] Optional: publish to PowerShell Gallery
