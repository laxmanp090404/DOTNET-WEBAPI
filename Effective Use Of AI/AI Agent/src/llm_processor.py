"""
llm_processor.py — Sends requirements to Gemini and parses the structured response.

Responsibilities:
  - Load the prompt template from disk.
  - Inject raw requirements into the template.
  - Call the Gemini API with retry/backoff.
  - Validate and parse the JSON response against the expected schema.
  - Return a strongly-typed RequirementsArtifact.
"""

from __future__ import annotations

import json
import logging
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from google import genai
from google.genai import types
from src.config import GeminiConfig

logger = logging.getLogger(__name__)

# ── Schema field names ────────────────────────────────────────────────────────
_REQUIRED_KEYS: frozenset[str] = frozenset(
    {
        "functional_requirements",
        "non_functional_requirements",
        "risks",
        "assumptions",
        "questions_for_client",
        "missing_information",
        "summary",
    }
)

# ── Retry settings ────────────────────────────────────────────────────────────
_MAX_RETRIES: int = 3
_BASE_BACKOFF_SEC: float = 2.0


# ── Data model ────────────────────────────────────────────────────────────────
@dataclass
class FunctionalRequirement:
    id: str
    title: str
    description: str
    priority: str  # High | Medium | Low


@dataclass
class NonFunctionalRequirement:
    id: str
    category: str
    description: str


@dataclass
class Risk:
    id: str
    risk: str
    severity: str
    mitigation: str


@dataclass
class Assumption:
    id: str
    assumption: str


@dataclass
class ClientQuestion:
    id: str
    question: str
    rationale: str


@dataclass
class RequirementsArtifact:
    functional_requirements: list[FunctionalRequirement] = field(default_factory=list)
    non_functional_requirements: list[NonFunctionalRequirement] = field(
        default_factory=list
    )
    risks: list[Risk] = field(default_factory=list)
    assumptions: list[Assumption] = field(default_factory=list)
    questions_for_client: list[ClientQuestion] = field(default_factory=list)
    missing_information: list[str] = field(default_factory=list)
    summary: str = ""


# ── Private helpers ───────────────────────────────────────────────────────────

def _load_prompt_template(prompt_file: Path) -> str:
    if not prompt_file.exists():
        raise FileNotFoundError(f"Prompt template not found: '{prompt_file}'")
    return prompt_file.read_text(encoding="utf-8")


def _build_prompt(template: str, requirements: str) -> str:
    if "{requirements}" not in template:
        raise ValueError(
            "Prompt template is missing the '{requirements}' placeholder."
        )
    return template.replace("{requirements}", requirements)


def _strip_markdown_fences(text: str) -> str:
    """Remove ```json ... ``` wrappers that some models add despite instructions."""
    # Match optional language tag after triple backticks
    pattern = r"^```(?:json)?\s*\n?(.*?)\n?```\s*$"
    match = re.match(pattern, text.strip(), re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()


def _parse_response(raw: str) -> dict[str, Any]:
    """Parse JSON from Gemini response, raising ValueError on failure."""
    cleaned = _strip_markdown_fences(raw)
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Gemini returned invalid JSON. Parse error: {exc}\n"
            f"Raw response (first 500 chars): {cleaned[:500]}"
        ) from exc
    return data


def _validate_schema(data: dict[str, Any]) -> None:
    """Ensure all required top-level keys are present."""
    missing = _REQUIRED_KEYS - set(data.keys())
    if missing:
        raise ValueError(
            f"Gemini response is missing required fields: {missing}\n"
            f"Received keys: {set(data.keys())}"
        )


def _map_to_artifact(data: dict[str, Any]) -> RequirementsArtifact:
    """Map raw dict to typed RequirementsArtifact dataclass."""
    frs = [
        FunctionalRequirement(**{k: v for k, v in item.items()})
        for item in data.get("functional_requirements", [])
    ]
    nfrs = [
        NonFunctionalRequirement(**{k: v for k, v in item.items()})
        for item in data.get("non_functional_requirements", [])
    ]
    risks = [
        Risk(**{k: v for k, v in item.items()})
        for item in data.get("risks", [])
    ]
    assumptions = [
        Assumption(**{k: v for k, v in item.items()})
        for item in data.get("assumptions", [])
    ]
    questions = [
        ClientQuestion(**{k: v for k, v in item.items()})
        for item in data.get("questions_for_client", [])
    ]
    return RequirementsArtifact(
        functional_requirements=frs,
        non_functional_requirements=nfrs,
        risks=risks,
        assumptions=assumptions,
        questions_for_client=questions,
        missing_information=data.get("missing_information", []),
        summary=data.get("summary", ""),
    )


# ── Public API ────────────────────────────────────────────────────────────────

def process_requirements(
    requirements: str,
    gemini_config: GeminiConfig,
    prompt_file: Path,
) -> tuple[RequirementsArtifact, str]:
    """
    Send requirements to Gemini and return a parsed artifact plus raw JSON.

    Args:
        requirements:  Raw requirements text.
        gemini_config: Gemini connection settings.
        prompt_file:   Path to the prompt template file.

    Returns:
        Tuple of (RequirementsArtifact, raw_json_string).

    Raises:
        FileNotFoundError: If prompt template is missing.
        ValueError:        If Gemini returns unparseable or schema-invalid JSON.
        RuntimeError:      If all retries are exhausted.
    """
    # Configure Gemini client (google-genai SDK)
    client = genai.Client(api_key=gemini_config.api_key)

    generation_config = types.GenerateContentConfig(
        temperature=gemini_config.temperature,
        max_output_tokens=gemini_config.max_tokens,
    )

    # Build prompt
    template = _load_prompt_template(prompt_file)
    prompt = _build_prompt(template, requirements)

    logger.info(
        "Sending requirements to Gemini (model=%s, temperature=%s).",
        gemini_config.model,
        gemini_config.temperature,
    )

    # Retry loop
    last_error: Exception | None = None
    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            response = client.models.generate_content(
                model=gemini_config.model,
                contents=prompt,
                config=generation_config,
            )
            raw_text = response.text
            logger.debug("Gemini raw response length: %d chars", len(raw_text))

            data = _parse_response(raw_text)
            _validate_schema(data)
            artifact = _map_to_artifact(data)

            logger.info(
                "Gemini response parsed: %d FRs, %d NFRs, %d risks, %d questions.",
                len(artifact.functional_requirements),
                len(artifact.non_functional_requirements),
                len(artifact.risks),
                len(artifact.questions_for_client),
            )
            return artifact, json.dumps(data, indent=2)

        except (ValueError, KeyError) as exc:
            last_error = exc
            logger.warning(
                "Attempt %d/%d failed (parse/schema error): %s",
                attempt,
                _MAX_RETRIES,
                exc,
            )
        except Exception as exc:  # Gemini API errors, network issues, etc.
            last_error = exc
            logger.warning(
                "Attempt %d/%d failed (API error): %s",
                attempt,
                _MAX_RETRIES,
                exc,
            )

        if attempt < _MAX_RETRIES:
            backoff = _BASE_BACKOFF_SEC * (2 ** (attempt - 1))
            logger.info("Retrying in %.1f seconds...", backoff)
            time.sleep(backoff)

    raise RuntimeError(
        f"All {_MAX_RETRIES} Gemini attempts failed. Last error: {last_error}"
    )