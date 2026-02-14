"""
Sentinel — Smoke Tests for Agent Instantiation

Verifies that each factory function returns a valid AssistantAgent
and that the mock telemetry generator works as expected.

These tests use a mock model client so no real API calls are made.
"""

import pytest
from unittest.mock import MagicMock

from autogen_agentchat.agents import AssistantAgent

from agents.observer import create_observer_agent, generate_mock_telemetry
from agents.diagnostic import create_diagnostic_agent
from agents.remediation import create_remediation_agent
from agents.reporter import create_reporter_agent


# ── Fixtures ─────────────────────────────────────────────────────────

@pytest.fixture
def mock_model_client() -> MagicMock:
    """A mock model client that won't hit any real API."""
    return MagicMock()


# ── Agent creation tests ────────────────────────────────────────────

class TestAgentCreation:
    """Each agent factory should return a properly-named AssistantAgent."""

    def test_observer_agent(self, mock_model_client: MagicMock) -> None:
        agent = create_observer_agent(mock_model_client)
        assert isinstance(agent, AssistantAgent)
        assert agent.name == "Observer"

    def test_diagnostic_agent(self, mock_model_client: MagicMock) -> None:
        agent = create_diagnostic_agent(mock_model_client)
        assert isinstance(agent, AssistantAgent)
        assert agent.name == "Diagnostic"

    def test_diagnostic_agent_cot_prompt(self, mock_model_client: MagicMock) -> None:
        """Verify that the Chain-of-Thought instructions are present."""
        agent = create_diagnostic_agent(mock_model_client)
        prompt = agent._system_messages[0].content
        assert "step-by-step" in prompt.lower()
        assert "identify the symptom" in prompt.lower()
        assert "rule out network" in prompt.lower()
        assert "failing component" in prompt.lower()

    def test_remediation_agent(self, mock_model_client: MagicMock) -> None:
        agent = create_remediation_agent(mock_model_client)
        assert isinstance(agent, AssistantAgent)
        assert agent.name == "Remediation"

    def test_reporter_agent(self, mock_model_client: MagicMock) -> None:
        agent = create_reporter_agent(mock_model_client)
        assert isinstance(agent, AssistantAgent)
        assert agent.name == "Reporter"


# ── Mock telemetry tests ────────────────────────────────────────────

class TestMockTelemetry:
    """The mock telemetry generator should produce formatted alert lines."""

    def test_default_count(self) -> None:
        output = generate_mock_telemetry()
        lines = output.strip().split("\n")
        assert len(lines) == 3

    def test_custom_count(self) -> None:
        output = generate_mock_telemetry(count=5)
        lines = output.strip().split("\n")
        assert len(lines) == 5

    def test_max_cap(self) -> None:
        """Should never return more lines than the error pool size."""
        output = generate_mock_telemetry(count=999)
        lines = output.strip().split("\n")
        assert len(lines) <= 12  # size of MOCK_ERROR_POOL

    def test_contains_alert_prefix(self) -> None:
        output = generate_mock_telemetry(count=1)
        assert "ALERT" in output
