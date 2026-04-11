"""Test suite for ticket-triage CLI."""

import pytest
from ticket_triage.triage import (
    load_rules,
    triage,
    TriageResult,
    score_priority,
    score_confidence,
    check_escalation,
)


class TestTriageBasic:
    """Basic triage functionality tests."""

    def test_placeholder(self):
        """Placeholder test to verify test setup."""
        assert True
