#!/usr/bin/env python3
"""
Sentinel — Autonomous Multi-Agent AIOps Engine

Main entry point.  Sets up the AutoGen RoundRobinGroupChat with all
four agents and kicks off a conversation with mock telemetry data.

Usage:
    python app.py                  # Run with mock telemetry (demo mode)
    python app.py --help           # Show help
    python app.py --errors 5       # Generate 5 mock error lines
"""

import argparse
import asyncio
import sys

from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination

from agents.observer import create_observer_agent, generate_mock_telemetry
from agents.diagnostic import create_diagnostic_agent
from agents.remediation import create_remediation_agent
from agents.reporter import create_reporter_agent
from config.settings import create_model_client
from utils.helpers import setup_logging, banner


async def run_pipeline(
    num_errors: int = 3,
    max_rounds: int = 12,
) -> None:
    """Build the four-agent team and run the AIOps pipeline."""

    # ── Create model client ──────────────────────────────────────────
    model_client = create_model_client()
    if model_client is None:
        print(
            "❌  No LLM configuration found.  "
            "Copy .env.example → .env and add your API key."
        )
        sys.exit(1)

    # ── Instantiate agents ───────────────────────────────────────────
    observer = create_observer_agent(model_client)
    diagnostic = create_diagnostic_agent(model_client)
    remediation = create_remediation_agent(model_client)
    reporter = create_reporter_agent(model_client)

    # ── Build the team ───────────────────────────────────────────────
    termination = MaxMessageTermination(max_messages=max_rounds)
    team = RoundRobinGroupChat(
        participants=[observer, diagnostic, remediation, reporter],
        termination_condition=termination,
    )

    # ── Generate mock telemetry ──────────────────────────────────────
    telemetry = generate_mock_telemetry(count=num_errors)
    print(f"\n📡 Mock telemetry generated:\n{telemetry}\n")

    initial_message = (
        "🚨 **Incoming Telemetry Alert — Sentinel Observer**\n\n"
        "The following anomalies have been detected in the last 5 minutes:\n\n"
        f"```\n{telemetry}\n```\n\n"
        "Observer: please analyse these signals and produce an Observation Report."
    )

    # ── Stream the multi-agent conversation ──────────────────────────
    print("=" * 70)
    print("  🛡️  SENTINEL PIPELINE — LIVE AGENT CONVERSATION")
    print("=" * 70)

    async for message in team.run_stream(task=initial_message):
        # TaskResult is the final object; everything else is a message
        if hasattr(message, "messages"):
            # This is the final TaskResult
            print("\n" + "=" * 70)
            print("  ✅  PIPELINE COMPLETE")
            print("=" * 70)
        else:
            # Individual agent message
            source = getattr(message, "source", "system")
            content = getattr(message, "content", str(message))
            print(f"\n{'─' * 70}")
            print(f"  🤖  [{source}]")
            print(f"{'─' * 70}")
            print(content)


def main() -> None:
    """Parse CLI args and launch the Sentinel pipeline."""

    parser = argparse.ArgumentParser(
        description="Sentinel: Autonomous Multi-Agent AIOps Engine",
    )
    parser.add_argument(
        "--errors",
        type=int,
        default=3,
        help="Number of mock error lines to generate (default: 3)",
    )
    parser.add_argument(
        "--max-rounds",
        type=int,
        default=12,
        help="Maximum conversation messages before termination (default: 12)",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging verbosity (default: INFO)",
    )
    args = parser.parse_args()

    # ── Bootstrap ────────────────────────────────────────────────────
    setup_logging(log_level=args.log_level)
    print(banner())

    asyncio.run(run_pipeline(num_errors=args.errors, max_rounds=args.max_rounds))


if __name__ == "__main__":
    main()
