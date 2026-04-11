# Diagnostic Collector — PRD

## 1. Concept & Vision

A one-command system info collector for L1/L2 handoffs. Instead of asking 20 questions over chat — "what does `df -h` say? what about `ip a`?" — L1 runs one script that gathers everything useful: network config, disk space, running services, recent errors, memory, CPU, and packages. Output is a clean HTML or Markdown report L2 can read instantly.

Target feel: the L1 agent who actually prepared properly for the escalation.

## 2. Functional Spec

### 2.1 Usage

```bash
# One command, no args needed
curl -s script.run/diag | bash
# or
diag-collect                    # interactive
diag-collect --html             # HTML report (default)
diag-collect --markdown         # Markdown report
diag-collect --json             # JSON for APIs
diag-collect --host workstation-42  # tag the hostname
diag-collect --upload           # upload to internal pastebin/S3
```

### 2.2 What It Collects

| Category | Commands / Sources |
|---|---|
| System | hostname, uptime, uname -a, dmidecode (if root) |
| CPU/RAM | `free -h`, `df -h`, `top -bn1` snapshot |
| Network | `ip a`, `ip route`, `/etc/resolv.conf`, `ss -tlnp` |
| Disk | mount points, LVM state, RAID status (if hwraid tools) |
| Services | `systemctl list-units --state=running` |
| Recent logs | last 50 errors from `journalctl -p err`, `syslog` |
| Package updates | pending security updates (apt/hyum/pacman) |
| Container status | `docker ps`, `docker ps -a` if Docker present |
| Active users | `who`, `last` last 10 logins |
| Network tests | DNS resolution, gateway ping |

### 2.3 Output

Markdown format:

```markdown
# Diagnostic Report — workstation-42
Collected: 2024-03-01 14:23:00 EET

## System
- Hostname: workstation-42
- Uptime: 14 days, 3 hours
- OS: Ubuntu 22.04.3 LTS

## CPU / Memory
- CPU: AMD Ryzen 7 3700X (8 cores)
- RAM: 31.2Gi / 32Gi used
- Swap: 2.1Gi / 8Gi used

## Disk
- /dev/sda1: 412G / 512G (80%) — ⚠ HIGH
- /dev/sdb1: 1.8T / 2T (90%) — 🔴 CRITICAL

## Network
- eth0: 192.168.1.42/24 (static)
- Gateway: 192.168.1.1
- DNS: 8.8.8.8, 1.1.1.1

## Running Services
- postgresql: active (running) since 2024-02-20
- nginx: active (running) since 2024-01-15
- docker: active (running) since 2024-02-28

## Recent Errors (last 50)
- postgresql: connection refused (3 occurrences)
- docker: health check failed container abc123

## Security Updates
- 14 updates available (3 are security patches)
```

### 2.4 Thresholds

| Condition | Flag |
|---|---|
| Disk > 80% | ⚠ HIGH |
| Disk > 90% | 🔴 CRITICAL |
| RAM > 90% | ⚠ HIGH |
| Security updates pending | 🔴 SECURITY PATCHES AVAILABLE |
| Service down | 🔴 DOWN |

### 2.5 Upload

`--upload` flag uploads report to a configured endpoint (internal pastebin, S3, or custom webhook) and prints the URL so L1 can paste it directly into the ticket.

## 3. Technical Approach

- **Language:** Bash (primary) + Python fallback for JSON output
- **Distribution:** Single self-extracting script via `curl | bash`
- **Script hosting:** Static file on internal web server or GitHub releases
- **No external deps** on target machine beyond standard Linux utilities
- **JSON output:** Python helper script (called from Bash)

### File Structure

```
diagnostic-collector/
├── pyproject.toml             # for Python helper
├── diag/
│   ├── __init__.py
│   ├── __main__.py
│   ├── collector.sh          # main Bash script (the deliverable)
│   ├── formatters.py         # JSON/Markdown output helpers
│   └── thresholds.py         # alert threshold config
├── tests/
│   └── test_formatters.py
└── README.md
```

## 4. Success Criteria

- [ ] `curl -s .../collector.sh | bash` runs on Ubuntu 22.04 and AlmaLinux 8
- [ ] All 10 categories collected in < 30 seconds on a VPS
- [ ] Disk > 80% correctly flagged as HIGH
- [ ] Markdown output renders correctly in GitHub Flavored Markdown
- [ ] JSON output is valid and parseable
- [ ] `--upload` POSTs to configurable endpoint

## 5. Out of Scope (v1)

- Windows agent (Sysinternal port)
- macOS compatibility
- Real-time monitoring / dashboards
- Alerting integration (PagerDuty, OpsGenie)
