"""
Sentinel — Shared Utilities
"""

import logging
import sys
from pathlib import Path


def setup_logging(
    log_level: str = "INFO",
    log_dir: str | None = None,
) -> logging.Logger:
    """Configure and return the root Sentinel logger.

    Writes to both stdout (coloured) and a rotating log file under `logs/`.
    """
    logger = logging.getLogger("sentinel")
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    if logger.handlers:
        return logger  # Already configured

    formatter = logging.Formatter(
        fmt="%(asctime)s │ %(levelname)-8s │ %(name)s │ %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # ── Console handler ──────────────────────────────────────────────
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    logger.addHandler(console)

    # ── File handler ─────────────────────────────────────────────────
    if log_dir is None:
        log_dir = Path(__file__).resolve().parent.parent / "logs"
    else:
        log_dir = Path(log_dir)

    log_dir.mkdir(parents=True, exist_ok=True)
    from logging.handlers import RotatingFileHandler

    file_handler = RotatingFileHandler(
        log_dir / "sentinel.log",
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3,
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def banner() -> str:
    """Return a startup banner for console output."""
    return r"""
  ╔═══════════════════════════════════════════════════════╗
  ║   🛡️  SENTINEL — Autonomous Multi-Agent AIOps Engine  ║
  ║        Observe · Diagnose · Remediate · Report        ║
  ╚═══════════════════════════════════════════════════════╝
"""
