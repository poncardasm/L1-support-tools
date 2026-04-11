# Diagnostic Collector — Implementation Plan

## 1. Architecture

The primary deliverable is `collector.sh` — a pure Bash script requiring only standard Linux utilities. Python is only used to generate the JSON output format.

```
diagnostic-collector/
├── diag/
│   ├── collector.sh           # main Bash script
│   ├── formatters.py          # Python JSON/Markdown formatter
│   ├── thresholds.py          # threshold config
│   └── __main__.py           # `diag-collect` entry point (Python)
└── README.md
```

collector.sh is the installable `curl | bash` script. Python is the CLI wrapper.

## 2. collector.sh Core

### 2.1 Script Structure

```bash
#!/bin/bash
set -euo pipefail

HOSTNAME_TAG="${HOSTNAME_TAG:-$(hostname)}"
OUTPUT_FORMAT="${OUTPUT_FORMAT:-markdown}"
UPLOAD_URL="${UPLOAD_URL:-}"

# Color codes (strip with -c flag for non-TTY)
RED='\033[0;31m'; YELLOW='\033[0;33m'; GREEN='\033[0;32m'; NC='\033[0m'

# Functions per category
collect_system() { ... }
collect_cpu_mem() { ... }
collect_disk() { ... }
collect_network() { ... }
collect_services() { ... }
collect_logs() { ... }
collect_packages() { ... }
collect_docker() { ... }
collect_users() { ... }
collect_network_tests() { ... }

# Main
main() {
    report_start=$(date '+%Y-%m-%d %H:%M:%S %Z')
    # collect all categories into temp file
    # format output
    # upload if requested
}
```

### 2.2 Category Collection Functions

```bash
collect_system() {
    echo "## System"
    echo "- Hostname: $(hostname)"
    echo "- Uptime: $(uptime -p 2>/dev/null || uptime)"
    echo "- OS: $(cat /etc/os-release | grep PRETTY_NAME | cut -d'"' -f2)"
}

collect_cpu_mem() {
    echo "## CPU / Memory"
    echo "\`\`\`"
    echo "CPU: $(nproc) cores"
    echo "RAM: $(free -h | awk '/^Mem:/ {print $3 "/" $2}')
    echo "Swap: $(free -h | awk '/^Swap:/ {print $3 "/" $2}')"
    echo "\`\`\`"
}

collect_disk() {
    echo "## Disk"
    df -h --output=source,size,used,pcent,target | tail -n +2 | while read -r source size used pcent target; do
        flag=""
        used_pct=${pcent%\%}
        if [ "$used_pct" -ge 90 ]; then flag="🔴 CRITICAL"
        elif [ "$used_pct" -ge 80 ]; then flag="⚠ HIGH"
        fi
        echo "- $target: $used/$size ($pcent) $flag"
    done
}

collect_network() {
    echo "## Network"
    echo "- IPs: $(ip -4 a | grep inet | awk '{print $2}' | paste -sd ',' -)"
    echo "- Gateway: $(ip route | grep default | awk '{print $3}')"
    echo "- DNS: $(cat /etc/resolv.conf | grep nameserver | awk '{print $2}' | paste -sd ',' -)"
}

collect_services() {
    echo "## Running Services"
    systemctl list-units --state=running --type=service --no-pager --no-legend \
        | awk '{print "- " $1 ": " $4 " " $5}' | head -20
}

collect_logs() {
    echo "## Recent Errors"
    echo "\`\`\`"
    journalctl -p err -n 50 --no-pager 2>/dev/null | head -30 || echo "(no recent errors)"
    echo "\`\`\`"
}

collect_packages() {
    echo "## Package Updates"
    if command -v apt &>/dev/null; then
        updates=$(apt list --upgradable 2>/dev/null | tail -n +2 | wc -l)
        security=$(apt-get -qq -y --only-upgrade install 2>&1 | grep -i security | wc -l)
        echo "- $updates updates available ($security security)"
    elif command -v dnf &>/dev/null; then
        updates=$(dnf check-update --quiet 2>/dev/null | wc -l)
        echo "- $updates updates available"
    fi
}

collect_docker() {
    if command -v docker &>/dev/null; then
        echo "## Docker"
        echo "Running containers: $(docker ps -q 2>/dev/null | wc -l)"
        docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Image}}" 2>/dev/null | head -10
    fi
}
```

### 2.3 Output Formatters

Markdown (Bash):
```bash
print_markdown() {
    echo "# Diagnostic Report — $HOSTNAME_TAG"
    echo "Collected: $report_start"
    collect_system; echo
    collect_cpu_mem; echo
    collect_disk; echo
    collect_network; echo
    collect_services; echo
    collect_logs; echo
    collect_packages; echo
    collect_docker; echo
}
```

JSON (Python helper):
```bash
# Bash calls Python formatter for JSON
python3 -c "
import sys, json
data = json.loads('$JSON_DATA')
print(format_json(data))
"
```

### 2.4 Upload

```bash
upload_report() {
    if [ -z "$UPLOAD_URL" ]; then return 1; fi
    response=$(curl -s -X POST -F "file=@-" "$UPLOAD_URL" < /dev/stdin)
    echo "Report URL: $response"
}
```

Config: `UPLOAD_URL` env var or `~/.config/diag-collector/config` with `upload_url=https://...`

### 2.5 Distribution

One-file distribution via GitHub releases:

```bash
curl -sL https://github.com/poncardasm/L1-support-tools/releases/latest/download/collector.sh | bash
```

Or self-hosted: drop on internal nginx, `curl -s https://internal.lan/scripts/collector.sh | bash`.

## 3. Known Pitfalls

1. **sudo requirements** — `dmidecode`, `journalctl` without `--user` may need sudo. Script should detect and warn if permission denied.
2. **Redhat/ AlmaLinux** — `systemctl` works same as Ubuntu. `apt` → `dnf`. Detect OS and route accordingly.
3. **Empty outputs** — commands like `journalctl` may return nothing. Always handle empty gracefully — don't print "(null)".
4. **Large outputs** — `docker ps -a` on a host with 200 containers. Cap at 20 rows.
5. **Color codes in TTY** — if output is not a TTY, strip color codes (add `\033[0m` reset after each colored output).
6. **Uptime parsing** — `uptime -p` is Ubuntu-specific. Fall back to `uptime` on RedHat/AlmaLinux.
7. **Exit code** — script should exit 0 even if some commands fail. Use `|| true` on optional commands.
