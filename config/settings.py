"""
Sentinel — Central Configuration

Loads environment variables from a .env file (if present) and exposes
a factory function to create the OpenAI model client used by all agents.

Supports both OpenAI and Azure OpenAI backends.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# ── Locate and load .env ────────────────────────────────────────────
_project_root = Path(__file__).resolve().parent.parent
_dotenv_path = _project_root / ".env"

if _dotenv_path.exists():
    load_dotenv(dotenv_path=_dotenv_path)
    print(f"[config] ✅  Loaded .env from {_dotenv_path}")
else:
    print(
        f"[config] ⚠️  No .env file found at {_dotenv_path}. "
        "Falling back to system environment variables."
    )

# ── Read keys ───────────────────────────────────────────────────────
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "")

MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.3"))

if not OPENAI_API_KEY and not AZURE_OPENAI_API_KEY:
    print(
        "[config] ❌  Neither OPENAI_API_KEY nor AZURE_OPENAI_API_KEY is set. "
        "Copy .env.example → .env and add your key."
    )


def create_model_client():
    """Create and return an OpenAI or Azure OpenAI model client.

    Returns an `OpenAIChatCompletionClient` or `AzureOpenAIChatCompletionClient`
    depending on which environment variables are set.
    Azure is preferred if both are set.
    """
    if AZURE_OPENAI_API_KEY:
        from autogen_ext.models.openai import AzureOpenAIChatCompletionClient

        return AzureOpenAIChatCompletionClient(
            azure_deployment=AZURE_OPENAI_DEPLOYMENT or MODEL_NAME,
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_key=AZURE_OPENAI_API_KEY,
            api_version=AZURE_OPENAI_API_VERSION,
            model=AZURE_OPENAI_DEPLOYMENT or MODEL_NAME,
            temperature=TEMPERATURE,
        )

    if OPENAI_API_KEY:
        from autogen_ext.models.openai import OpenAIChatCompletionClient

        return OpenAIChatCompletionClient(
            model=MODEL_NAME,
            api_key=OPENAI_API_KEY,
            temperature=TEMPERATURE,
        )

    return None
