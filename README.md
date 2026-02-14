# 🛡️ Sentinel — Autonomous Multi-Agent AIOps Engine

An intelligent, multi-agent AIOps pipeline built with [AutoGen](https://github.com/microsoft/autogen) that **observes**, **diagnoses**, **remediates**, and **reports** on infrastructure incidents autonomously.

## Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Observer   │ ──▶ │  Diagnostic  │ ──▶ │ Remediation  │ ──▶ │   Reporter   │
│  (Telemetry) │     │    (CoT)     │     │   (Actions)  │     │   (Report)   │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
```

| Agent | Role |
|-------|------|
| **Observer** | Monitors metrics & logs, raises anomalies. Includes a mock telemetry generator for demos. |
| **Diagnostic** | Performs Chain-of-Thought root-cause analysis: symptom → network check → failing component. |
| **Remediation** | Proposes safe, ordered remediation actions with rollback plans. |
| **Reporter** | Produces a polished, stakeholder-ready incident report. |

## Quick Start

```bash
# 1. Clone & enter the project
cd Sentinel

# 2. Create a virtual environment
python -m venv .venv && source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure your API key
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY (or Azure OpenAI credentials)

# 5. Run the engine
python app.py

# 6. Run tests
python -m pytest tests/ -v
```

### CLI Options

```
python app.py --errors 5        # Generate 5 mock error lines
python app.py --max-rounds 8    # Limit conversation to 8 rounds
python app.py --log-level DEBUG # Verbose logging
python app.py --help            # Show all options
```

## Project Structure

```
Sentinel/
├── app.py                 # Main entry point
├── requirements.txt       # Dependencies
├── .env.example           # API key template
├── config/
│   └── settings.py        # LLM & env configuration
├── agents/
│   ├── observer.py        # Observer + Mock Telemetry Generator
│   ├── diagnostic.py      # Diagnostic (Chain-of-Thought)
│   ├── remediation.py     # Remediation planner
│   └── reporter.py        # Incident report generator
├── utils/
│   └── helpers.py         # Logging & shared utilities
├── tests/
│   └── test_agents.py     # Smoke tests
└── logs/                  # Runtime logs
```

## License

MIT
