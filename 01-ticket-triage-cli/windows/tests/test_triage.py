"""Tests for the ticket triage CLI."""

import pytest
from ticket_triage.triage import (
    triage,
    load_rules,
    score_priority,
    score_confidence,
    check_escalation,
    TriageResult,
)


class TestTriage:
    """Test cases for triage functionality."""

    @pytest.fixture
    def rules(self):
        """Load default rules for testing."""
        return load_rules()

    def test_empty_ticket_raises_error(self, rules):
        """Empty ticket text should raise ValueError."""
        with pytest.raises(ValueError, match="empty"):
            triage("", rules)
