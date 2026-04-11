# Ticket Triage CLI — PRD

## 1. Concept & Vision

A CLI tool that takes raw L1 support ticket text and returns a structured triage result: category, priority, recommended action, escalation guidance, and related KB links. The goal is to reduce decision fatigue for L1 agents and ensure clean escalations to L2 — no ambiguity about why something was bumped up.

Target feel: a senior L1 analyst looking over the agent's shoulder saying "here's what's going on, here's what you do next."

## 2. Functional Spec

### 2.1 Input

- Single ticket text via stdin, pipe, or file flag
- Accepts: plain email bodies, Jira descriptions, ServiceNow notes, raw pasted text
- Multi-line input supported

```bash
cat ticket.txt | ticket-triage
echo "User can't login, VPN keeps dropping" | ticket-triage
ticket-triage --file /path/to/ticket.txt
```

### 2.2 Output

Structured text:

```
Category: 🔴 Authentication
Priority: P2 (Medium)
Suggested action: Reset EntraID password via Admin Center
Escalate to: L2 if "MFA not working" or "account locked"
Related KB: KB-1042
Root cause signals: ["VPN", "credential", "reset"]
Confidence: High
```

Exit codes:
- `0` — triage complete (any confidence level)
- `1` — parse error / no input
- `2` — flag: requires L2 (unresolved by L1 procedures)

### 2.3 Category Taxonomy

| Category | Keywords |
|---|---|
| Authentication | password, login, MFA, SSO, EntraID, account locked, access denied |
| Network/VPN | VPN, connection, network, firewall, cannot connect, timeout |
| Email/Outlook | outlook, email, calendar, mailbox, PST, OST, signature |
| Hardware | laptop, monitor, keyboard, mouse, hardware failure, device |
| Software | install, uninstall, update, crash, blue screen, application |
| Access Request | access, permissions, SharePoint, Teams, group, role |
| Printing | printer, print job, driver, spooler |
| Other/Unknown | no match above |

### 2.4 Priority Scoring

- **P1 (Critical)** — "down", "outage", "everyone", "production", "urgent"
- **P2 (Medium)** — standard ticket with clear workaround
- **P3 (Low)** — "when possible", cosmetic, question-only
- **P4 (Info)** — no action needed, just logging

Urgency modifiers: words like "ASAP", "immediately", "right now" bump priority by one level.

### 2.5 Escalation Rules

If category is Hardware (with hardware failure keywords) → flag L2 immediately.
If multiple categories detected → flag for L2 review.
If P1 + Authentication → flag for L2 + Security.

### 2.6 Rule Engine (v1)

Regex + keyword matching. No external API calls.

Pattern file: `rules.yaml`

```yaml
categories:
  authentication:
    keywords: [password, login, MFA, SSO, EntraID, locked, access denied]
    escalation: L2 if MFA or account locked
    kb: KB-1001
    priority_bump: 0
```

### 2.7 Optional Local LLM Mode (v2)

Toggle with `--llm` flag. Uses local Ollama endpoint. Falls back to rule engine if Ollama unavailable.

## 3. Technical Approach

- **Language:** Python 3.10+
- **CLI framework:** Click
- **Config parsing:** PyYAML
- **Local LLM:** requests to Ollama at `http://localhost:11434`
- **Packaging:** `pip install -e .`
- **Config:** `~/.config/ticket-triage/rules.yaml` for custom rules

### File Structure

```
ticket-triage-cli/
├── pyproject.toml
├── ticket_triage/
│   ├── __init__.py
│   ├── __main__.py
│   ├── triage.py
│   └── rules.yaml
├── tests/
│   └── test_triage.py
└── README.md
```

## 4. Success Criteria

- [ ] `cat ticket.txt | ticket-triage` produces valid output in < 500ms
- [ ] All 8 categories correctly matched via keyword test suite
- [ ] Priority scoring tests pass
- [ ] Escalation flags fire on known L2 patterns
- [ ] `--file`, `--llm`, `--json` flags work as specified
- [ ] Config override works
- [ ] Exit codes are correct per spec

## 5. Out of Scope (v1)

- Ticket management system integration
- Multi-language support
- Web UI
- macOS `.app` bundle
