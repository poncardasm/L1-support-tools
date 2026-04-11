# AD/User Provisioning CLI — Tasks

## Phase 1: Skeleton

- [ ] Create `pyproject.toml` with `click`, `azure-identity`, `msgraph-sdk`, `python-dotenv`
- [ ] Create `ad_provision/__init__.py` with `__version__`
- [ ] Create `ad_provision/__main__.py` entry point
- [ ] Create `tests/test_commands.py` with empty test class + fixture
- [ ] Create `.gitignore` (exclude `.env`, `creds.env`, `__pycache__/`, `*.pyc`)
- [ ] Verify `pip install -e .` works + `ad-provision --help` prints

---

## Phase 2: Auth + Graph Client

- [ ] Implement `graph_client.py` — `get_graph_client()` with ClientSecretCredential
- [ ] Implement `config.py` — `load_creds()` from `~/.config/ad-provision/creds.env`
- [ ] Test: creds loaded from file successfully
- [ ] Test: missing creds file raises `SystemExit` with message
- [ ] Test: invalid env format raises readable error

---

## Phase 3: Core Commands

- [ ] Implement `new-user` command: create AD user + add to group + mailbox setup
- [ ] Implement `add-group` command: add user to group by email
- [ ] Implement `enable-mailbox` command: enable mailbox via Graph
- [ ] Implement `reset-password` command: set temp password + force change flag
- [ ] Implement `deprovision` command: disable + remove groups
- [ ] Wire `--dry-run` to all commands
- [ ] Test: each command in dry-run does NOT call Graph API
- [ ] Test: each command without dry-run calls correct Graph endpoint

---

## Phase 4: Output + Error Handling

- [ ] All commands print structured `[OK]` / `[TEMP]` / `[ERROR]` output
- [ ] Errors go to stderr with exit code 1
- [ ] Auth failures exit with code 2
- [ ] `--json` flag outputs machine-readable JSON for all commands

---

## Phase 5: Security + Config

- [ ] `.gitignore` verified: no creds files in commit
- [ ] `README.md` documents `chmod 600` for creds file
- [ ] `creds.env.example` created as template (no real values)
- [ ] All Graph calls use HTTPS only

---

## Phase 6: Testing

- [ ] Unit tests for all 5 commands with mocked Graph client
- [ ] Dry-run tests: verify no Graph calls made
- [ ] Password complexity test: generated password meets EntraID policy
- [ ] `pytest tests/ -v` passes

---

## Phase 7: Docs + Polish

- [ ] `README.md` with install, auth setup, usage examples for all 5 commands
- [ ] Tag v1.0.0
- [ ] Commit per project
