"""CLI commands for ad-provision."""

import click


@click.group()
def cli():
    """AD/User Provisioning CLI for Azure AD/EntraID."""
    pass


@cli.command("new-user")
@click.option("--username", required=True, help="Username (UPN prefix)")
@click.option("--name", required=True, help="Display name")
@click.option("--email", required=True, help="Email address (UPN)")
@click.option("--department", required=True, help="Department name")
@click.option(
    "--group", "groups", multiple=True, help="Group to add user to (can be repeated)"
)
@click.option("--enable-mailbox", is_flag=True, help="Enable Exchange Online mailbox")
@click.option(
    "--dry-run", is_flag=True, help="Show what would happen without making changes"
)
def new_user(username, name, email, department, groups, enable_mailbox, dry_run):
    """Create a new AD user with optional mailbox."""
    pass


@cli.command("add-group")
@click.option("--username", required=True, help="Username to add")
@click.option("--group", required=True, help="Group name to add user to")
@click.option(
    "--dry-run", is_flag=True, help="Show what would happen without making changes"
)
def add_group(username, group, dry_run):
    """Add existing user to AD group."""
    pass


@cli.command("enable-mailbox")
@click.option("--username", required=True, help="Username to enable mailbox for")
@click.option(
    "--dry-run", is_flag=True, help="Show what would happen without making changes"
)
def enable_mailbox(username, dry_run):
    """Enable Exchange Online mailbox for existing user."""
    pass


@cli.command("reset-password")
@click.option("--username", required=True, help="Username to reset password")
@click.option(
    "--dry-run", is_flag=True, help="Show what would happen without making changes"
)
def reset_password(username, dry_run):
    """Reset user password and force change on next login."""
    pass


@cli.command("deprovision")
@click.option("--username", required=True, help="Username to deprovision")
@click.option("--reason", default="", help="Reason for deprovision")
@click.option(
    "--dry-run", is_flag=True, help="Show what would happen without making changes"
)
def deprovision(username, reason, dry_run):
    """Deprovision user (disable account, remove groups, revoke sessions)."""
    pass
