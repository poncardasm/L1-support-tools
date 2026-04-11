# Diagnostic Collector — Tasks

## Phase 1: Skeleton

- [ ] Create `pyproject.toml` with `click`
- [ ] Create `diag/__init__.py`
- [ ] Create `diag/__main__.py` entry point (`diag-collect`)
- [ ] Create `.gitignore`
- [ ] Verify `pip install -e .` works + `diag-collect --help` prints

---

## Phase 2: Bash Collector Script

- [ ] Create `diag/collector.sh` with `set -euo pipefail`
- [ ] Implement `collect_system()` — hostname, uptime, OS
- [ ] Implement `collect_cpu_mem()` — `nproc`, `free -h`
- [ ] Implement `collect_disk()` — `df -h` with threshold flags
- [ ] Implement `collect_network()` — `ip a`, `ip route`, DNS
- [ ] Implement `collect_services()` — `systemctl list-units --state=running`
- [ ] Implement `collect_logs()` — `journalctl -p err -n 50`
- [ ] Implement `collect_packages()` — apt/dnf security update count
- [ ] Implement `collect_docker()` — `docker ps` if docker present
- [ ] Implement `collect_users()` — `who`, `last -n 10`
- [ ] Implement `collect_network_tests()` — DNS resolve, gateway ping
- [ ] Wire `--hostname` tag override
- [ ] Test: script runs on Ubuntu 22.04 and AlmaLinux 8 without errors

---

## Phase 3: Output Formatters

- [ ] Implement Markdown formatter (Bash)
- [ ] Implement JSON formatter (Python helper called from Bash)
- [ ] Implement HTML formatter (optional, Python)
- [ ] Threshold flagging: > 80% = HIGH, > 90% = CRITICAL
- [ ] Color codes stripped for non-TTY output
- [ ] Verify: Markdown renders correctly in GFM

---

## Phase 4: Upload

- [ ] Implement `upload_report()` — POST to configurable endpoint
- [ ] `--upload` flag: POST markdown/JSON to pastebin/S3/webhook
- [ ] Config: `UPLOAD_URL` env var or `~/.config/diag-collector/config`
- [ ] Test: `--upload` POSTs to a local test endpoint

---

## Phase 5: Distribution

- [ ] Create GitHub release workflow: `release.sh` builds single-file tarball
- [ ] `curl | bash` one-liner documented in README
- [ ] Self-hosted: nginx config example in README
- [ ] Test: `curl -sL <release-url> | bash` runs end-to-end

---

## Phase 6: Testing

- [ ] Mock system commands with `unittest.mock`
- [ ] Threshold tests: disk 85% → HIGH, disk 92% → CRITICAL
- [ ] JSON formatter tests: valid JSON output
- [ ] Bash script: runs against fixture mock data without real system calls
- [ ] `pytest tests/ -v` passes

---

## Phase 7: Docs + Polish

- [ ] `README.md` with curl|bash install, all options, screenshot of sample output
- [ ] Tag v1.0.0
- [ ] Commit per project
