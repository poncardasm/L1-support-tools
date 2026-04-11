# AD/User Provisioning CLI — Implementation Plan

## 1. Project Setup

```
ad-provisioning-cli/
├── pyproject.toml
├── ad_provision/
│   ├── __init__.py
│   ├── __main__.py
│   ├── commands.py      # Click command group + individual ops
│   ├── graph_client.py  # MS Graph auth + operations
│   └── config.py        # Creds loading from .env
├── tests/
│   └── test_commands.py
└── README.md
```

## 2. Authentication (graph_client.py)

### 2.1 MS Graph via azure-identity

```python
from azure.identity import ClientSecretCredential
from msgraph_sdk import GraphServiceClient

def get_graph_client(tenant_id, client_id, client_secret):
    credential = ClientSecretCredential(tenant_id, client_id, client_secret)
    return GraphServiceClient(credential, ["https://graph.microsoft.com/.default"])
```

Scopes required on the app registration:
- `User.ReadWrite.All`
- `Group.ReadWrite.All`
- `Mail.Send` (for welcome email)
- `Directory.AccessAsUser.All` (for password reset)

### 2.2 Config loading

```python
def load_creds():
    env_path = Path.home() / ".config" / "ad-provision" / "creds.env"
    if not env_path.exists():
        raise SystemExit("Missing credentials. See README.")
    return dotenv_values(env_path)
```

creds.env format:
```
TENANT_ID=...
CLIENT_ID=...
CLIENT_SECRET=...
```

## 3. Command Implementations

### 3.1 new-user

```python
@click.command()
@click.option('--name', required=True)
@click.option('--email', required=True)
@click.option('--department', default='')
@click.option('--group', help='Primary group to add user to')
def new_user(name, email, department, group, dry_run):
    user_id = create_ad_user(name, email, department, dry_run)
    if group:
        add_to_group(user_id, group, dry_run)
    enable_exchange_mailbox(email, dry_run)
    print_success(f"User {email} provisioned")
```

Flow:
1. `POST /users` — create user with `userPrincipalName`, `mail`, `department`
2. `POST /groups/{group_id}/members/$ref` — add to dept group
3. `PATCH /users/{id}` — set `passwordProfile` with `forceChangePasswordNextSignIn`

### 3.2 add-group

```python
@click.command()
@click.argument('email')
@click.option('--group', 'group_name', required=True)
def add_group(email, group_name, dry_run):
    user_id = get_user_id(email)
    group_id = get_group_id(group_name)
    if dry_run:
        print(f"[DRY] Would add {email} to {group_name}")
        return
    graph_client.groups.members.add_member(group_id, user_id)
```

### 3.3 enable-mailbox

```python
def enable_exchange_mailbox(user_id, dry_run):
    # Uses Graph API: POST /users/{id}/mailboxSettings
    # or direct Exchange Online PowerShell over connecting Azure AD app
    pass
```

Note: Full Exchange Online management via Graph requires `Mail.ReadWrite` scope + SharePoint-hosted management mailbox approach. For v1, target EntraID-only features.

### 3.4 reset-password

```python
def reset_password(user_id, dry_run):
    temp = generate_password()
    if dry_run:
        print(f"[DRY] Would set temp password for {user_id}")
        return
    graph_client.users.patch(user_id, {
        "passwordProfile": {
            "forceChangePasswordNextSignIn": True,
            "password": temp
        }
    })
    print(f"[TEMP] Password: {temp} — force change required")
```

### 3.5 deprovision

```python
def deprovision(user_id, reason, dry_run):
    if dry_run:
        print(f"[DRY] Would deprovision {user_id}")
        return
    graph_client.users.patch(user_id, {"accountEnabled": False})
    # Remove all group memberships via batched $ref deletes
    groups = graph_client.users.get_member_groups(user_id)
    for group in groups:
        remove_group_member(group.id, user_id)
    print(f"[OK] User {user_id} deprovisioned: {reason}")
```

## 4. Error Handling

```python
try:
    result = graph_call()
except GraphError as e:
    print(f"[ERROR] {e.error.code}: {e.error.message}", file=sys.stderr)
    raise SystemExit(1)
```

Exit codes:
- `0` — all operations succeeded
- `1` — one or more operations failed
- `2` — authentication failure (bad creds)

## 5. Dry-run Implementation

Every mutating function accepts `dry_run: bool`. When True:
- Print what would happen without calling Graph API
- Return early
- Never raise

## 6. Security Notes

- Client secret stored in file, not in code or git
- File permissions: `chmod 600 ~/.config/ad-provision/creds.env`
- `.gitignore` must exclude `.env` and any `*secret*` files
- All Graph API calls are over HTTPS

## 7. Testing Strategy

Mock `GraphServiceClient` responses with `unittest.mock`.

```python
@patch('ad_provision.graph_client.get_graph_client')
def test_new_user_dry_run(mock_client):
    result = runner.invoke(['new-user', '--name', 'Bob', '--email', 'bob@corp.com', '--dry-run'])
    assert '[DRY]' in result.output
    mock_client.users.create.assert_not_called()
```

## 8. Known Pitfalls

1. **Tenant-scoped vs. Invite-scoped users** — `create()` only works within your tenant. If using B2B guests, use `/invitations` endpoint instead.
2. **Group display name vs. mail nickname** — `get_group_id()` should search both `displayName` and `mailNickname`.
3. **Batch $ref limitations** — removing members from large groups requires pagination. Use `$batch` endpoint for bulk removals.
4. **Password policy compliance** — the generated temp password must meet EntraID password policy (8+ chars, complexity). Use `secrets.token_urlsafe(12)` + manual complexity injection.
5. **Soft-deleted users** — `deprovision` only disables. User object stays in Azure AD recycle bin for 30 days.
