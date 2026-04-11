"""Core triage logic for the ticket triage CLI."""

from collections import namedtuple

TriageResult = namedtuple(
    "TriageResult",
    [
        "category",
        "priority",
        "action",
        "escalate_to",
        "kb",
        "signals",
        "confidence",
        "flag_l2",
    ],
)


def load_rules():
    """Load rules from package and user config (placeholder)."""
    return {}


def score_priority(ticket_text: str, category: str, rules: dict) -> str:
    """Score priority based on ticket text (placeholder)."""
    return "P2 (Medium)"


def score_confidence(matched_keywords: list, category_count: int) -> str:
    """Score confidence based on match count (placeholder)."""
    return "Medium"


def check_escalation(ticket_text: str, category: str, priority: str) -> tuple:
    """Check if ticket should be escalated (placeholder)."""
    return False, "None"


def triage(raw_ticket: str, rules: dict) -> TriageResult:
    """Main triage function (placeholder)."""
    if not raw_ticket or not raw_ticket.strip():
        raise ValueError("empty ticket")
    # Placeholder return
    return TriageResult(
        category="Other/Unknown",
        priority="P2 (Medium)",
        action="No action available",
        escalate_to="None",
        kb="KB-0000",
        signals=[],
        confidence="Low",
        flag_l2=False,
    )


def triage_cli():
    """CLI entry point (placeholder)."""
    print("Ticket Triage CLI v1.0.0")
    print("Use --help for usage information.")
