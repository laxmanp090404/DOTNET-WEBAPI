"""
config.py — Centralised configuration loader.

Reads all settings from environment variables (via .env) and validates them
at startup so failures surface immediately, not mid-execution.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_PROJECT_ROOT / ".env")


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class GeminiConfig:
    api_key: str
    model: str
    temperature: float
    max_tokens: int


@dataclass(frozen=True)
class GmailConfig:
    sender: str
    app_password: str
    recipient: str
    cc: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class AppConfig:
    log_level: str
    output_dir: Path
    inputs_dir: Path
    requirements_file: Path
    prompt_file: Path
    gemini: GeminiConfig
    gmail: GmailConfig


def _require(key: str) -> str:
    """Return env var value or raise a descriptive error."""
    value = os.getenv(key, "").strip()
    if not value:
        raise EnvironmentError(
            f"Required environment variable '{key}' is missing or empty. "
            f"Copy .env.example to .env and fill in your values."
        )
    return value


def _optional(key: str, default: str = "") -> str:
    return os.getenv(key, default).strip()


def load_config() -> AppConfig:
    """
    Load and validate all configuration from environment variables.

    Raises:
        EnvironmentError: If any required variable is missing.
        ValueError: If a variable has an invalid value (e.g., non-numeric temperature).
    """
    # ── Gemini ──────────────────────────────────────────────────────────────
    try:
        temperature = float(_optional("GEMINI_TEMPERATURE", "0.3"))
    except ValueError as exc:
        raise ValueError("GEMINI_TEMPERATURE must be a float between 0 and 1.") from exc

    try:
        max_tokens = int(_optional("GEMINI_MAX_TOKENS", "8192"))
    except ValueError as exc:
        raise ValueError("GEMINI_MAX_TOKENS must be a positive integer.") from exc

    gemini = GeminiConfig(
        api_key=_require("GEMINI_API_KEY"),
        model=_optional("GEMINI_MODEL", "gemini-2.5-flash"),
        temperature=temperature,
        max_tokens=max_tokens,
    )

    # ── Gmail ────────────────────────────────────────────────────────────────
    cc_raw = _optional("GMAIL_CC", "")
    cc_list = [addr.strip() for addr in cc_raw.split(",") if addr.strip()]

    gmail = GmailConfig(
        sender=_require("GMAIL_SENDER"),
        app_password=_require("GMAIL_APP_PASSWORD"),
        recipient=_require("GMAIL_RECIPIENT"),
        cc=cc_list,
    )

    # ── Paths ────────────────────────────────────────────────────────────────
    output_dir = _PROJECT_ROOT / _optional("OUTPUT_DIR", "outputs")
    inputs_dir = _PROJECT_ROOT / _optional("INPUTS_DIR", "inputs")
    req_filename = _optional("REQUIREMENTS_FILE", "requirements.txt")
    prompt_filename = _optional("PROMPT_FILE", "prompts/requirements_prompt.txt")

    requirements_file = inputs_dir / req_filename
    prompt_file = _PROJECT_ROOT / prompt_filename

    # ── App ──────────────────────────────────────────────────────────────────
    config = AppConfig(
        log_level=_optional("LOG_LEVEL", "INFO").upper(),
        output_dir=output_dir,
        inputs_dir=inputs_dir,
        requirements_file=requirements_file,
        prompt_file=prompt_file,
        gemini=gemini,
        gmail=gmail,
    )

    logger.debug("Configuration loaded successfully.")
    return config