"""
input_reader.py — Reads and validates the raw requirements text file.

Responsibilities:
  - Verify the file exists and is readable.
  - Ensure the content is non-empty and meets minimum length.
  - Strip extraneous whitespace.
  - Return a clean string ready for the LLM prompt.
"""

from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Minimum character count to be considered a meaningful requirement
_MIN_CONTENT_LENGTH: int = 50


def read_requirements(file_path: Path) -> str:
    """
    Read and validate requirements from a text file.

    Args:
        file_path: Absolute or relative path to the requirements .txt file.

    Returns:
        Stripped, non-empty requirements string.

    Raises:
        FileNotFoundError: If the file does not exist.
        PermissionError:   If the file cannot be read.
        ValueError:        If the file is empty or below minimum length.
    """
    logger.info("Reading requirements from: %s", file_path)

    resolved = Path(file_path).resolve()

    if not resolved.exists():
        raise FileNotFoundError(
            f"Requirements file not found: '{resolved}'\n"
            f"Place your requirements in '{file_path}' and try again."
        )

    if not resolved.is_file():
        raise ValueError(f"Path exists but is not a file: '{resolved}'")

    try:
        raw_text = resolved.read_text(encoding="utf-8")
    except PermissionError as exc:
        raise PermissionError(
            f"Cannot read '{resolved}': permission denied."
        ) from exc

    cleaned = raw_text.strip()

    if not cleaned:
        raise ValueError(
            f"Requirements file is empty: '{resolved}'\n"
            f"Please add your client requirements and try again."
        )

    if len(cleaned) < _MIN_CONTENT_LENGTH:
        raise ValueError(
            f"Requirements are too short ({len(cleaned)} chars). "
            f"Minimum is {_MIN_CONTENT_LENGTH} characters. "
            f"Please provide more detail."
        )

    logger.info(
        "Requirements loaded successfully (%d characters, ~%d words).",
        len(cleaned),
        len(cleaned.split()),
    )
    return cleaned