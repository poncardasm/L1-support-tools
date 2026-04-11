# Bulk Action Runner — Implementation Plan

## 1. Architecture

Shared MS Graph client with `ad-provisioning-cli` (same creds file). Different entry point + batch operation logic.

```
bulk-action-runner/
├── bulk/
│   ├── __init__.py
│   ├── __main__.py      # `bulk-run` entry point
│   ├── operations.py    # per-row operation implementations
│   ├── report.py        # CSV report generation
│   └── config.py        # shared creds loading
├── tests/
└── README.md
```

Dependencies: `click`, `azure-identity`, `msgraph-sdk`, `pandas`, `python-dotenv`, `tqdm`

## 2. Operations (operations.py)

### 2.1 Operation Registry

```python
OPERATIONS = {
    "password-reset": Operation(
        name="Password Reset",
        action=reset_password,
        supports_dry_run=True,
    ),
    "add-group": Operation(
        name="Add to Group",
        action=add_to_group,
        supports_dry_run=True,
        required_params=["group"],
    ),
    "enable-mailbox": Operation(
        name="Enable Mailbox",
        action=enable_mailbox,
        supports_dry_run=True,
    ),
    "deprovision": Operation(
        name="Deprovision",
        action=deprovision_user,
        supports_dry_run=True,
        required_params=["reason"],
    ),
}
```

### 2.2 Row Processing

```python
def process_row(row: dict, operation: str, params: dict, dry_run: bool) -> RowResult:
    email = row.get("email")
    if not email:
        return RowResult(email, operation, "failure", "missing email column", 0)
    
    try:
        op_func = OPERATIONS[operation].action
        result_detail = op_func(email, params, dry_run)
        return RowResult(email, operation, "success", result_detail, 0)
    except GraphError as e:
        return RowResult(email, operation, "failure", e.error.message, e.status_code)
    except Exception as e:
        return RowResult(email, operation, "failure", str(e), -1)
```

### 2.3 Password Reset

```python
def reset_password(email: str, params: dict, dry_run: bool) -> str:
    if dry_run:
        return f"[DRY] Would reset password for {email}"
    
    temp = generate_temp_password()
    graph_client.users.patch(user_id, {
        "passwordProfile": {
            "forceChangePasswordNextSignIn": True,
            "password": temp
        }
    })
    return f"temp: {temp}"
```

### 2.4 Add Group

```python
def add_to_group(email: str, params: dict, dry_run: bool) -> str:
    group_name = params.get("group")
    if not group_name:
        raise ValueError("Missing --group parameter")
    
    user_id = get_user_id_by_email(email)
    group_id = get_group_id_by_name(group_name)
    
    if dry_run:
        return f"[DRY] Would add {email} to {group_name}"
    
    graph_client.groups.members.add_member(group_id, user_id)
    return f"added to {group_name}"
```

### 2.5 Enable Mailbox + Deprovision

Mirror `ad-provisioning-cli` implementations. Reuse from shared module if extracting shared library.

## 3. CSV Processing

### 3.1 Reading

```python
import csv
import pandas as pd

def read_csv(path: Path) -> list[dict]:
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        return list(reader)
```

### 3.2 Batch Runner

```python
def run_batch(csv_path: Path, operation: str, params: dict, dry_run: bool, report_path: Path | None) -> list[RowResult]:
    rows = read_csv(csv_path)
    results = []
    
    for i, row in enumerate(tqdm(rows, desc=operation)):
        result = process_row(row, operation, params, dry_run)
        results.append(result)
        
        if i < len(rows) - 1:  # delay between rows, not after last
            time.sleep(0.5)
    
    if report_path:
        write_report(results, report_path)
    
    return results
```

Use `tqdm` for progress bar during batch operations.

### 3.3 Report Writer (report.py)

```python
def write_report(results: list[RowResult], path: Path):
    df = pd.DataFrame([r.to_dict() for r in results])
    df.to_csv(path, index=False)

# RowResult.to_dict():
{
    "email": "alice@company.com",
    "operation": "password-reset",
    "result": "success",
    "detail": "temp: Xy#9aBc!",
    "timestamp": "2024-03-01T14:00:00"
}
```

## 4. CLI Interface (__main__.py)

```python
@click.command()
@click.argument("operation")
@click.argument("csv_path", type=click.Path(exists=True))
@click.option("--group", help="Group name for add-group operation")
@click.option("--reason", help="Reason for deprovision operation")
@click.option("--dry-run", is_flag=True)
@click.option("--report", type=click.Path(), help="Save results to CSV")
def run(operation, csv_path, group, reason, dry_run, report):
    """Run a bulk operation on a CSV of users."""
    params = {"group": group, "reason": reason}
    op = get_operation(operation)
    
    if operation not in OPERATIONS:
        click.echo(f"Unknown operation: {operation}", err=True)
        raise SystemExit(1)
    
    if dry_run:
        click.echo(f"[DRY RUN] {operation} on {csv_path}")
    
    results = run_batch(Path(csv_path), operation, params, dry_run, Path(report) if report else None)
    
    # Print summary
    successes = sum(1 for r in results if r.result == "success")
    failures = sum(1 for r in results if r.result == "failure")
    click.echo(f"\nSummary: {successes} OK, {failures} failed")
    raise SystemExit(1 if failures else 0)
```

## 5. Throttling / Rate Limiting

### 5.1 EntraID Rate Limits

- User creation: 250/tenant/day
- Group membership changes: ~200/minute/tenant
- Password resets: ~50/minute/tenant

Default 500ms delay between operations handles all of these comfortably.

### 5.2 Delay Implementation

```python
DELAY_MS = 500

def process_row_with_delay(...):
    result = process_row(...)
    time.sleep(DELAY_MS / 1000)
    return result
```

Expose delay as `--delay-ms` flag for tuning.

## 6. Error Handling

### 6.1 Per-Row Errors

Never crash the batch on a bad row. Capture error, continue to next.

```python
try:
    ...
except GraphError as e:
    results.append(RowResult(email, op, "failure", f"Graph: {e.error.code}", e.status_code))
    continue
```

### 6.2 Missing Email Column

Immediately fatal — raise with helpful message:

```python
if "email" not in rows[0]:
    raise SystemExit("CSV must have 'email' column")
```

## 7. Testing

### 7.1 Mock Graph Client

Patch `GraphServiceClient` with `unittest.mock`:

```python
@patch("bulk.operations.get_graph_client")
def test_password_reset_dry_run(mock_client):
    result = process_row({"email": "alice@corp.com"}, "password-reset", {}, dry_run=True)
    assert result.result == "success"
    mock_client.users.patch.assert_not_called()
```

### 7.2 Dry Run Tests

Verify no Graph API calls in dry-run mode for all 4 operations.

### 7.3 CSV Tests

Test with valid CSV, missing email column, empty rows.

## 8. Known Pitfalls

1. **Email column case sensitivity** — CSV DictReader lowercases keys on some Python versions. Use `email` lowercase column name in all CSVs and document this.
2. **Rate limit on 429** — catch HTTP 429, back off 60s, retry once. If still 429, fail the row gracefully.
3. **Large CSVs** — pandas reads full CSV into memory. For v1, cap at 1000 rows with warning. Future: streaming CSV.
4. **Group name → ID resolution** — `get_group_id_by_name()` should search both `displayName` and `mailNickname`. Groups can have spaces in displayName but not mailNickname.
5. **Duplicate group membership** — adding a user already in a group returns 400. Mark as "already member" in detail, not failure.
6. **Deprovision ordering** — must disable account first, THEN remove groups. Reversing causes session tokens to remain active during removal window.
