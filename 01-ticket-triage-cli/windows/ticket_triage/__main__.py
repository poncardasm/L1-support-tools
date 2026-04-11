"""Entry point for `python -m ticket_triage`."""

import sys


def main():
    """Main entry point - imports and runs the CLI."""
    from ticket_triage.triage import triage_cli

    triage_cli()


if __name__ == "__main__":
    main()
