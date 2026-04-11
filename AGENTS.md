# L1 Support Tools

Monorepo for L1 support CLI tools. Each tool has platform-specific implementations.

**Current state:** Tools are in planning phase — only docs exist, no implementation code yet.

## Structure

```
NN-tool-name/
├── macos/docs/    # PRD.md, IMPLEMENTATION.md, TASKS.md
└── windows/docs/  # PRD.md, IMPLEMENTATION.md, TASKS.md
```

Tools are numbered 01-07 for ordering.

## Tool Stack

All tools use:

- Python 3.10+
- Click for CLI
- pytest for tests
- Homebrew (macOS) for distribution

## Commands

Per tool (inside tool directory after implementation):

```bash
pip install -e .          # dev install
pytest tests/ -v          # run tests
```

## Config Locations

macOS: `~/.config/<tool-name>/`
Windows: `%APPDATA%\<tool-name>\`

## Git Workflow

Use conventional commits standard for all commits:

```
<type>: <description>

Examples:
feat: add ticket-triage-cli project scaffold
chore: add comprehensive .gitignore with OS temp files
docs: update AGENTS.md with git workflow section
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## Docs Purpose

- PRD.md — product spec
- IMPLEMENTATION.md — technical plan
- TASKS.md — phased checklist
