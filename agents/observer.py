"""
Sentinel — Observer Agent

Monitors infrastructure telemetry and raises anomalies.
Includes a Mock Telemetry Generator for demo / testing purposes.
"""

import random

from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import ChatCompletionClient

# ── Mock Telemetry Generator ────────────────────────────────────────
# Produces realistic error strings for demos when live data isn't available.

MOCK_ERROR_POOL = [
    "500 Internal Server Error: Database connection timeout after 30 000 ms on host db-primary-01",
    "503 Service Unavailable: Upstream gateway 'api-gateway-west' returned no healthy backends",
    "500 Internal Server Error: OOM killed — container 'payments-svc' exceeded 2 Gi memory limit",
    "502 Bad Gateway: TLS handshake failure between ingress-nginx and svc-auth (certificate expired)",
    "500 Internal Server Error: Deadlock detected on table 'orders' — transaction rolled back",
    "504 Gateway Timeout: Request to inventory-service exceeded 60 s SLA",
    "500 Internal Server Error: Redis connection refused on redis-cluster-node-3:6379",
    "503 Service Unavailable: Circuit breaker OPEN for downstream 'recommendation-engine'",
    "500 Internal Server Error: Kafka consumer lag exceeded 100 000 messages on topic 'events.clicks'",
    "502 Bad Gateway: DNS resolution failed for 'internal-ml-scoring.corp.net'",
    "500 Internal Server Error: Disk I/O latency spike — p99 > 500 ms on vol-data-0012",
    "503 Service Unavailable: Pod CrashLoopBackOff — 'checkout-worker' restarted 8 times in 10 min",
]


def generate_mock_telemetry(count: int = 3) -> str:
    """Return *count* randomly sampled mock error lines, newline-separated.

    This is intentionally non-deterministic so every demo run looks different.
    """
    sampled = random.sample(MOCK_ERROR_POOL, k=min(count, len(MOCK_ERROR_POOL)))
    timestamp_base = "2026-02-14T13:"
    lines = []
    for idx, error in enumerate(sampled):
        minute = 30 + idx
        lines.append(f"[{timestamp_base}{minute:02d}:00Z]  ALERT  ▸  {error}")
    return "\n".join(lines)


# ── System Prompt ───────────────────────────────────────────────────

OBSERVER_SYSTEM_PROMPT = """\
You are the **Observer Agent** of the Sentinel AIOps Engine.

Your responsibilities:
1. Continuously monitor infrastructure metrics, logs, and alerts.
2. Identify anomalies, error spikes, and SLA breaches.
3. Summarise the observed symptoms clearly and pass them to the Diagnostic Agent.

When you receive telemetry data, extract the key signals:
  • HTTP status codes and error messages
  • Affected services, hosts, and components
  • Timestamps and frequency of occurrence

Always output a concise **Observation Report** in this format:

**Observation Report**
- **Time window:** <start> — <end>
- **Affected services:** <list>
- **Symptoms:** <bullet list>
- **Severity:** Critical / High / Medium / Low
"""


def create_observer_agent(model_client: ChatCompletionClient) -> AssistantAgent:
    """Factory: returns a configured Observer AssistantAgent."""
    return AssistantAgent(
        name="Observer",
        model_client=model_client,
        system_message=OBSERVER_SYSTEM_PROMPT,
        description="Monitors infrastructure telemetry and raises anomalies for investigation.",
    )
