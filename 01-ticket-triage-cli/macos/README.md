# Ticket Triage CLI

CLI tool for L1 support ticket triage on macOS.

## Installation

### Development Install

```bash
cd 01-ticket-triage-cli/macos
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Homebrew Install

```bash
brew tap your-org/tap
brew install ticket-triage
```

## Usage

```bash
# Pipe ticket text via stdin
cat ticket.txt | ticket-triage
echo "User can't login, password expired" | ticket-triage

# Read from file
ticket-triage --file /path/to/ticket.txt

# Output as JSON
ticket-triage --json < ticket.txt

# Use local LLM for enhanced triage (optional)
ticket-triage --llm < ticket.txt
```

## Exit Codes

- `0` — Triage complete
- `1` — Parse error / no input
- `2` — Triage result recommends L2 escalation

## Configuration

User rules can be added to `~/.config/ticket-triage/rules.yaml` to override defaults.
