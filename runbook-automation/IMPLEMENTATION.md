# Runbook Automation — Implementation Plan

## 1. Project Setup

```
runbook-automation/
├── pyproject.toml
├── runbook/
│   ├── __init__.py
│   ├── __main__.py
│   ├── parser.py        # extract executable steps from Markdown
│   ├── executor.py      # run steps with stop-on-error logic
│   ├── indexer.py       # list + search runbooks
│   └── state.py         # resume state management
├── runbooks/             # default runbook library
│   ├── authentication/
│   │   └── reset-vpn.md
│   └── infrastructure/
│       └── restart-postgresql.md
├── tests/
│   └── test_parser.py
└── README.md
```

Dependencies: `click`, `mistune` (Markdown parser), `pyyaml`

## 2. Parser (parser.py)

### 2.1 Step Extraction

Parse Markdown with `mistune`, find all fenced code blocks:

```python
import mistune

def extract_steps(markdown: str) -> list[Step]:
    tokens = mistune.parse(markdown)
    steps = []
    for token in tokens:
        if token.get('type') == 'fence' and token.get('info') in ('bash', 'sh', 'shell'):
            steps.append(Step(
                number=len(steps) + 1,
                language=token['info'],
                command=token['raw'],
                title=extract_title_before(markdown, token['mark_map']) or f"Step {len(steps)+1}"
            ))
    return steps
```

### 2.2 Title Extraction

Grab text immediately preceding the code block:

```python
def extract_title_before(markdown: str, mark_map: dict) -> str:
    # find the last text token before this fence
    ...
```

### 2.3 Step Namedtuple

```python
Step = namedtuple('Step', ['number', 'language', 'command', 'title'])
```

## 3. Executor (executor.py)

### 3.1 Run Step

```python
def run_step(step: Step, dry_run: bool = False) -> StepResult:
    if dry_run:
        print(f"[DRY] {step.command}")
        return StepResult(step.number, 0, "", True)
    
    result = subprocess.run(
        step.command,
        shell=True,
        capture_output=True,
        text=True,
        timeout=300  # 5 minute timeout per step
    )
    return StepResult(step.number, result.returncode, result.stdout + result.stderr, False)
```

### 3.2 Run All Steps

```python
def execute_runbook(steps: list[Step], resume_from: int = 1, dry_run: bool = False) -> RunbookResult:
    results = []
    for step in steps:
        if step.number < resume_from:
            continue
        print(f"\n[STEP {step.number}/{len(steps)}] {step.title}")
        if not dry_run:
            print(step.command)
        
        result = run_step(step, dry_run)
        results.append(result)
        
        if result.exit_code != 0 and not dry_run:
            return RunbookResult(results, completed=False, failed_at=step.number)
    
    return RunbookResult(results, completed=True, failed_at=None)
```

### 3.3 Interactive Stop

On non-zero exit with interactive TTY:

```python
def prompt_on_error(result: StepResult) -> str:
    if not sys.stdin.isatty():
        return 'abort'
    
    print(f"  Exit code: {result.exit_code}")
    print(f"  Output: {result.output[:500]}")
    print("\n[DID NOT EXPECT THIS] Options:")
    print("  [s] Skip this step and continue")
    print("  [f] Force continue")
    print("  [a] Abort")
    return input("> ").strip().lower()
```

### 3.4 State Persistence

```python
STATE_DIR = Path.home() / ".runbook" / "state"

def save_state(runbook_name: str, current_step: int):
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    state_file = STATE_DIR / f"{slugify(runbook_name)}.json"
    with open(state_file, 'w') as f:
        json.dump({
            "runbook": runbook_name,
            "current_step": current_step,
            "last_run": datetime.utcnow().isoformat()
        }, f, indent=2)

def load_state(runbook_name: str) -> dict | None:
    state_file = STATE_DIR / f"{slugify(runbook_name)}.json"
    if state_file.exists():
        return json.loads(state_file.read_text())
    return None

def clear_state(runbook_name: str):
    state_file = STATE_DIR / f"{slugify(runbook_name)}.json"
    state_file.unlink(missing_ok=True)
```

## 4. Indexer (indexer.py)

### 4.1 List Runbooks

```python
def list_runbooks(path: Path, category: str = None) -> list[RunbookEntry]:
    search_path = path / category if category else path
    runbooks = []
    for md in search_path.rglob("*.md"):
        rel = md.relative_to(search_path)
        steps = extract_steps(md.read_text())
        runbooks.append(RunbookEntry(
            path=md,
            category=rel.parent.name if rel.parent != search_path else "root",
            name=md.stem,
            step_count=len(steps)
        ))
    return sorted(runbooks, key=lambda r: r.name)
```

### 4.2 Search

```python
def search_runbooks(path: Path, query: str) -> list[RunbookEntry]:
    results = []
    for md in path.rglob("*.md"):
        content = md.read_text().lower()
        if query.lower() in content or query.lower() in md.stem.lower():
            steps = extract_steps(md.read_text())
            results.append(RunbookEntry(path=md, name=md.stem, step_count=len(steps)))
    return results
```

## 5. CLI Interface (__main__.py)

```python
@click.group()
@click.pass_context
def runbook(ctx):
    """Runbook automation for IT operations."""
    ctx.ensure_object(Context)

@runbook.command()
@click.argument('runbook_path', type=click.Path(exists=True))
@click.option('--from-step', type=int, default=1, help='Start from step N')
@click.option('--resume', is_flag=True, help='Resume from last failed step')
@click.option('--dry-run', is_flag=True, help='Show commands without executing')
def run(runbook_path, from_step, resume, dry_run):
    """Execute a runbook."""
    ...
```

## 6. Default Runbooks

Pre-included example runbooks:

`runbooks/authentication/reset-vpn.md`:
```markdown
# Reset VPN Profile

## Steps

1. Check VPN client status
   ```bash
   systemctl status vpn-agent
   ```

2. Disconnect if active
   ```bash
   vpn-cli disconnect
   ```

3. Clear local profile
   ```bash
   rm -rf ~/.config/vpn/profiles/current.json
   ```

4. Reconnect
   ```bash
   vpn-cli connect --profile corporate
   ```
```

`runbooks/infrastructure/restart-postgresql.md`:
```markdown
# Restart PostgreSQL

## Steps

1. Check current status
   ```bash
   systemctl status postgresql
   ```

2. Stop
   ```bash
   sudo systemctl stop postgresql
   ```

3. Start
   ```bash
   sudo systemctl start postgresql
   ```

4. Verify
   ```bash
   systemctl status postgresql | grep "Active"
   ```
```

## 7. Known Pitfalls

1. **Shell vs. bash** — `shell=True` is required for pipes/redirection in commands. Without it `|` in `systemctl status | grep` will fail.
2. **Timeout** — set a reasonable per-step timeout (300s). Long-running steps like `apt upgrade` should be expected. Don't let steps run forever.
3. **ANSI codes** — some commands output ANSI color codes. Use `strip()` on output before printing if TTY is dumb.
4. **Step numbering** — `--from-step` is 1-indexed. Internal state uses 1-indexed step numbers to match `--from-step` UX.
5. **State file collision** — if two runbooks have the same slugified name, state files will collide. Use a hash of the full path as key.
