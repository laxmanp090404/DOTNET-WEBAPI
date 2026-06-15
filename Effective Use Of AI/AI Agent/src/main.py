"""
main.py — Orchestrator entry point for the Requirements Automation Tool.

Execution flow:
  1. Configure logging
  2. Load and validate config from .env
  3. Read requirements from input file
  4. Send to Gemini and parse structured artifact
  5. Format professional email
  6. Send via Gmail SMTP
  7. Save outputs (JSON, HTML, plain-text) to disk
"""

from __future__ import annotations

import json
import logging
import logging.handlers
import sys
from datetime import datetime, timezone
from pathlib import Path

# ── Bootstrap: ensure src/ is importable when running from project root ───────
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from src.config import load_config
from src.email_formatter import format_email
from src.gmail_sender import send_email
from src.input_reader import read_requirements
from src.llm_processor import process_requirements


def _setup_logging(log_level: str, log_dir: Path) -> None:
    """Configure console + rotating file logging."""
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "app.log"

    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level, logging.INFO))

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level, logging.INFO))
    console_fmt = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )
    console_handler.setFormatter(console_fmt)

    # Rotating file handler (10 MB × 5 backups)
    file_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_fmt = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(file_fmt)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)


def _save_outputs(
    output_dir: Path,
    raw_json: str,
    html_body: str,
    text_body: str,
) -> dict[str, Path]:
    """Persist all outputs to disk. Returns a dict of label → path."""
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

    paths: dict[str, Path] = {
        "json":  output_dir / f"response_{timestamp}.json",
        "html":  output_dir / f"email_draft_{timestamp}.html",
        "text":  output_dir / f"email_draft_{timestamp}.txt",
    }

    paths["json"].write_text(raw_json, encoding="utf-8")
    paths["html"].write_text(html_body, encoding="utf-8")
    paths["text"].write_text(text_body, encoding="utf-8")

    return paths


def main() -> int:
    """
    Run the full automation pipeline.

    Returns:
        0 on success, 1 on any failure.
    """
    # ── 1. Load config (also loads .env) ─────────────────────────────────────
    try:
        config = load_config()
    except EnvironmentError as exc:
        # Can't log yet — print directly
        print(f"[ERROR] Configuration error: {exc}", file=sys.stderr)
        return 1

    # ── 2. Setup logging ──────────────────────────────────────────────────────
    log_dir = _PROJECT_ROOT / "logs"
    _setup_logging(config.log_level, log_dir)
    logger = logging.getLogger(__name__)

    logger.info("=" * 55)
    logger.info("Requirements Automation Tool — Starting")
    logger.info("=" * 55)

    # ── 3. Read requirements ──────────────────────────────────────────────────
    try:
        requirements_text = read_requirements(config.requirements_file)
    except (FileNotFoundError, ValueError, PermissionError) as exc:
        logger.error("Input error: %s", exc)
        return 1

    # ── 4. Process with Gemini ────────────────────────────────────────────────
    try:
        artifact, raw_json = process_requirements(
            requirements=requirements_text,
            gemini_config=config.gemini,
            prompt_file=config.prompt_file,
        )
    except FileNotFoundError as exc:
        logger.error("Prompt file error: %s", exc)
        return 1
    except (ValueError, RuntimeError) as exc:
        logger.error("LLM processing failed: %s", exc)
        return 1

    # ── 5. Format email ───────────────────────────────────────────────────────
    email_payload = format_email(
        artifact=artifact,
        sender=config.gmail.sender,
        recipient=config.gmail.recipient,
        cc=config.gmail.cc,
        recipient_name="Team",
    )

    # ── 6. Save outputs ───────────────────────────────────────────────────────
    saved = _save_outputs(
        output_dir=config.output_dir,
        raw_json=raw_json,
        html_body=email_payload.html_body,
        text_body=email_payload.text_body,
    )
    for label, path in saved.items():
        logger.info("Output saved [%s]: %s", label.upper(), path)

    # ── 7. Send email ─────────────────────────────────────────────────────────
    try:
        send_email(email_payload, app_password=config.gmail.app_password)
    except Exception as exc:
        logger.error("Email sending failed: %s", exc)
        logger.info("Outputs are saved locally — you can send the draft manually.")
        return 1

    logger.info("=" * 55)
    logger.info("✅  Pipeline complete!")
    logger.info("    → Email sent to:  %s", config.gmail.recipient)
    logger.info("    → Outputs in:     %s", config.output_dir)
    logger.info("=" * 55)
    return 0


if __name__ == "__main__":
    sys.exit(main())