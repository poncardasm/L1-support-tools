# Ticket Triage CLI

A command-line tool for L1 support teams that automatically categorizes and prioritizes support tickets.

## What It Does

Takes raw support ticket text and returns a structured triage result:
- **Category**: Authentication, Network/VPN, Email, Hardware, Software, Access Request, Printing, or Other
- **Priority**: P1 (Critical) through P4 (Info)
- **Suggested Action**: What to do next
- **Escalation Flag**: Whether to route to L2
- **Confidence Score**: How sure the tool is about the classification

## Quick Example

```bash
$ echo "User can't login, password expired" | ticket-triage
Category: authentication
Priority: P2 (Medium)
Suggested action: Reset EntraID password via Admin Center
Escalate to: None
Related KB: KB-1001
Root cause signals: ['password', 'login']
Confidence: Medium
```

## How It Works

The tool uses keyword matching against a rules file to categorize tickets. No external APIs—everything runs locally.

### Priority Rules
- **P1**: Words like "down", "outage", "production", "urgent"
- **P2**: Default (no keywords matched)
- **P3**: Words like "when possible", "cosmetic"
- **P4**: Words like "FYI", "no action needed"

### Escalation Triggers
- Authentication + MFA/locked account → L2 + Security
- Hardware failure keywords → L2 immediate
- P1 + Authentication → L2 + Security

## Platforms

- **macOS**: Fully implemented
- **Windows**: Planned

## Installation

### macOS (Development)

```bash
cd 01-ticket-triage-cli/macos
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### macOS (Homebrew - Future)

```bash
brew tap your-org/tap
brew install ticket-triage
```

## Usage

```bash
# Pipe from stdin
echo "VPN is down" | ticket-triage

# Read from file
ticket-triage --file ticket.txt

# JSON output
ticket-triage --json < ticket.txt

# Show version
ticket-triage --version
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Triage complete |
| 1 | Parse error / no input |
| 2 | L2 escalation recommended |

Use exit code 2 in scripts:
```bash
if ticket-triage --file ticket.txt; then
    handle_l1
elif [ $? -eq 2 ]; then
    escalate_l2
fi
```

## Configuration

Create `~/.config/ticket-triage/rules.yaml` to override default keywords and actions.

## Documentation

- `macos/docs/PRD.md` - Product requirements
- `macos/docs/IMPLEMENTATION.md` - Technical details
- `macos/docs/TASKS.md` - Implementation checklist
