# 🛡️ Sentinel — Autonomous Multi-Agent AIOps Engine

> An intelligent, multi-agent AIOps pipeline powered by [Microsoft AutoGen](https://github.com/microsoft/autogen) that **observes**, **diagnoses**, **remediates**, and **reports** on infrastructure incidents — autonomously, in real-time.

[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![AutoGen v0.7](https://img.shields.io/badge/AutoGen-v0.7-purple.svg)](https://github.com/microsoft/autogen)
[![Tests](https://img.shields.io/badge/tests-9%20passed-brightgreen.svg)](#testing)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🧠 What is Sentinel?

Sentinel is an **autonomous AIOps engine** that uses a team of four AI agents working together in a round-robin pipeline to handle infrastructure incidents end-to-end — from detection to resolution report — without human intervention.

Instead of relying on a single LLM call, Sentinel breaks the problem into **specialised roles**, each with its own system prompt and reasoning strategy. The agents collaborate through AutoGen's `RoundRobinGroupChat`, streaming their conversation in real-time to your terminal.

### Why Multi-Agent?

| Traditional Approach | Sentinel Approach |
|---------------------|-------------------|
| One monolithic prompt | Four specialised agents with distinct roles |
| Single-pass analysis | Multi-step reasoning with structured handoffs |
| Generic output | Structured reports (Observation → Diagnosis → Remediation → Report) |
| No reasoning trace | Full Chain-of-Thought visible in terminal |

---

## 🏗️ Architecture

```
  ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
  │    Observer      │ ───▶ │   Diagnostic    │ ───▶ │  Remediation    │ ───▶ │    Reporter      │
  │   🔭 Monitor     │      │   🔬 CoT RCA     │      │   🔧 Fix & Plan  │      │   📋 Report      │
  │                 │      │                 │      │                 │      │                 │
  │ • Ingest alerts │      │ • Identify      │      │ • Propose safe  │      │ • Timeline      │
  │ • Detect anomaly│      │   symptom       │      │   actions       │      │ • RCA summary   │
  │ • Flag severity │      │ • Rule out      │      │ • Blast radius  │      │ • Impact assess │
  │ • Produce       │      │   network       │      │ • Rollback plan │      │ • Lessons       │
  │   Observation   │      │ • Pinpoint root │      │ • Simulate exec │      │   learned       │
  │   Report        │      │   cause         │      │                 │      │                 │
  └─────────────────┘      └─────────────────┘      └─────────────────┘      └─────────────────┘
```

### Agent Details

| Agent | Module | Role | Key Features |
|-------|--------|------|--------------|
| **Observer** | `agents/observer.py` | Monitors infrastructure telemetry and raises anomalies | Built-in **Mock Telemetry Generator** with 12 realistic AIOps error strings (500s, OOM kills, CrashLoopBackOff, circuit breakers, etc.) |
| **Diagnostic** | `agents/diagnostic.py` | Performs root-cause analysis using **Chain-of-Thought** reasoning | 3-step CoT prompt: (1) Identify the symptom → (2) Rule out network issues → (3) Identify the specific failing component |
| **Remediation** | `agents/remediation.py` | Proposes and simulates remediation actions | Ordered by risk (least-disruptive first), includes blast radius analysis, rollback procedures, and safety guardrails |
| **Reporter** | `agents/reporter.py` | Produces stakeholder-ready incident reports | Structured template: Timeline, Root-Cause Analysis, Remediation Actions, Impact Assessment, Lessons Learned |

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Agent Framework** | [AutoGen v0.7](https://github.com/microsoft/autogen) (`autogen-agentchat`, `autogen-core`, `autogen-ext`) |
| **Orchestration** | `RoundRobinGroupChat` with `MaxMessageTermination` |
| **LLM Provider** | OpenAI or **Azure OpenAI** (configurable via `.env`) |
| **Model Client** | `OpenAIChatCompletionClient` / `AzureOpenAIChatCompletionClient` |
| **Streaming** | Async `run_stream()` for real-time terminal output |
| **Config** | `python-dotenv` with explicit path resolution and key validation |
| **Testing** | `pytest` with `unittest.mock` (no API calls in tests) |
| **Logging** | Python `logging` with rotating file handler + console output |

---

## 🚀 Quick Start

### Prerequisites

- Python **3.12+**
- An **OpenAI** or **Azure OpenAI** API key

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/nanda1045/Sentinel.git
cd Sentinel

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

### Configuration

```bash
# 4. Create your environment file
cp .env.example .env
```

Edit `.env` with your credentials:

**For Azure OpenAI:**
```env
AZURE_OPENAI_API_KEY=your-azure-key-here
AZURE_OPENAI_ENDPOINT=https://your-resource.cognitiveservices.azure.com
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
AZURE_OPENAI_API_VERSION=2025-01-01-preview
MODEL_NAME=gpt-4o-mini
```

**For OpenAI:**
```env
OPENAI_API_KEY=sk-your-openai-key-here
MODEL_NAME=gpt-4
```

### Run the Engine

```bash
# 5. Launch the pipeline
python app.py
```

You'll see the Sentinel banner, followed by live agent conversation streamed to your terminal:

```
  ╔═══════════════════════════════════════════════════════╗
  ║   🛡️  SENTINEL — Autonomous Multi-Agent AIOps Engine  ║
  ║        Observe · Diagnose · Remediate · Report        ║
  ╚═══════════════════════════════════════════════════════╝

📡 Mock telemetry generated:
[2026-02-14T13:30:00Z]  ALERT  ▸  503 Service Unavailable: Pod CrashLoopBackOff ...
[2026-02-14T13:31:00Z]  ALERT  ▸  500 Internal Server Error: Redis connection refused ...
[2026-02-14T13:32:00Z]  ALERT  ▸  500 Internal Server Error: OOM killed ...

======================================================================
  🛡️  SENTINEL PIPELINE — LIVE AGENT CONVERSATION
======================================================================

──────────────────────────────────────────────────────────────────────
  🤖  [Observer]
──────────────────────────────────────────────────────────────────────
**Observation Report**
- **Severity:** Critical
- **Affected services:** checkout-worker, redis-cluster-node-3, payments-svc
...
```

---

## ⚙️ CLI Options

| Flag | Default | Description |
|------|---------|-------------|
| `--errors N` | `3` | Number of mock telemetry error lines to generate |
| `--max-rounds N` | `12` | Maximum conversation messages before auto-termination |
| `--log-level LEVEL` | `INFO` | Logging verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |
| `--help` | — | Show all available options |

```bash
python app.py --errors 5 --max-rounds 8 --log-level DEBUG
```

---

## 🧪 Testing

Sentinel includes **9 smoke tests** that verify agent instantiation, Chain-of-Thought prompt content, and the mock telemetry generator — all without making any API calls.

```bash
python -m pytest tests/ -v
```

```
tests/test_agents.py::TestAgentCreation::test_observer_agent           PASSED
tests/test_agents.py::TestAgentCreation::test_diagnostic_agent         PASSED
tests/test_agents.py::TestAgentCreation::test_diagnostic_agent_cot_prompt  PASSED
tests/test_agents.py::TestAgentCreation::test_remediation_agent        PASSED
tests/test_agents.py::TestAgentCreation::test_reporter_agent           PASSED
tests/test_agents.py::TestMockTelemetry::test_default_count            PASSED
tests/test_agents.py::TestMockTelemetry::test_custom_count             PASSED
tests/test_agents.py::TestMockTelemetry::test_max_cap                  PASSED
tests/test_agents.py::TestMockTelemetry::test_contains_alert_prefix    PASSED

9 passed in 0.53s
```

---

## 📁 Project Structure

```
Sentinel/
├── app.py                     # Main entry point — async pipeline with streaming output
├── requirements.txt           # Python dependencies
├── .env.example               # API key template (OpenAI + Azure OpenAI)
├── .gitignore                 # Excludes .env, __pycache__, .venv, logs
│
├── config/
│   ├── __init__.py
│   └── settings.py            # Loads .env → creates OpenAI/Azure model client
│
├── agents/
│   ├── __init__.py            # Re-exports all agent factory functions
│   ├── observer.py            # Observer agent + Mock Telemetry Generator (12 errors)
│   ├── diagnostic.py          # Diagnostic agent with Chain-of-Thought system prompt
│   ├── remediation.py         # Remediation agent with safety guardrails
│   └── reporter.py            # Reporter agent with incident report template
│
├── utils/
│   ├── __init__.py
│   └── helpers.py             # Logging setup (rotating file + console) & banner
│
├── tests/
│   ├── __init__.py
│   └── test_agents.py         # 9 smoke tests (agents + telemetry + CoT prompt)
│
└── logs/                      # Runtime log files (gitignored)
    └── .gitkeep
```

---

## 🔑 How the Chain-of-Thought (CoT) Works

The Diagnostic Agent's system prompt enforces a **3-step reasoning chain** that makes the terminal output look intelligent and traceable during demos:

1. **Identify the symptom** — Restate the anomaly in precise technical terms
2. **Rule out network issues** — Explicitly consider DNS, TLS, load balancers, firewalls, packet loss
3. **Identify the specific failing component** — Narrow down to the exact subsystem with evidence

This structured approach ensures the agent doesn't jump to conclusions and provides a visible reasoning trace that operations teams can follow during live incidents.

---

## 🔒 Security

- **API keys** are loaded from `.env` which is **gitignored** — never committed to the repo
- The Remediation Agent has built-in **safety guardrails**:
  - Never proposes deletion of production data without human approval
  - Prefers restarts and scaling over destructive operations
  - Recommends manual intervention when confidence is low

---

## 📄 License

MIT

---

## 👤 Author

Nanda Kishroe Vuppili — [@nanda1045](https://github.com/nanda1045)
