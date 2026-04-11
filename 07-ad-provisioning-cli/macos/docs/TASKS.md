# AD/User Provisioning CLI — Tasks (macOS)

## Phase 1: Project Skeleton

- [ ] Create `pyproject.toml` with msgraph-sdk + azure-identity deps
- [ ] Create `ad_provision/__init__.py` with version
- [ ] Create `ad_provision/__main__.py` for CLI entry
- [ ] Create `config/creds.env.example`
- [ ] Verify `pip install -e .` works and `ad-provision --help` prints

---

## Phase 2: Microsoft Graph Integration

- [ ] Implement `graph_client.py` with certificate-based auth
- [ ] Implement `config.py` for loading credentials from `~/.config/`
- [ ] Test connection to EntraID with certificate

---

## Phase 3: Core Commands

- [ ] Implement `new-user` command in Click
- [ ] Implement `add-group` command
- [ ] Implement `enable-mailbox` command
- [ ] Implement `reset-password` command
- [ ] Implement `deprovision` command
- [ ] All commands support `--dry-run` flag

---

## Phase 4: Output Formatting

- [ ] Implement `output.py` with consistent formatting
- [ ] Test `[OK]`, `[FAIL]`, `[TEMP]`, `[WARN]` prefixes

---

## Phase 5: Testing

- [ ] Create `tests/test_commands.py`
- [ ] Test `--dry-run` mode for all commands
- [ ] Mock Graph API calls for unit tests
- [ ] Run `pytest tests/ -v`

---

## Phase 6: Homebrew Packaging

- [ ] Create `Formula/ad-provision.rb`
- [ ] Test: `brew install -- Formula/ad-provision.rb` works

---

## Phase 7: Documentation

- [ ] Write `README.md` with macOS-specific instructions
- [ ] Document certificate setup
- [ ] Add bash/zsh command examples

---

## Phase 8: Publish

- [ ] Push to GitHub
- [ ] Optional: publish to PyPI
- [ ] Optional: create Homebrew tap
