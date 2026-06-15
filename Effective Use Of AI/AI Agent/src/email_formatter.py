"""
email_formatter.py — Converts a RequirementsArtifact into a professional email.

Responsibilities:
  - Render an HTML email with branded styling.
  - Render a plain-text fallback.
  - Return an EmailPayload dataclass ready for gmail_sender.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timezone

from src.llm_processor import RequirementsArtifact

logger = logging.getLogger(__name__)


@dataclass
class EmailPayload:
    subject: str
    html_body: str
    text_body: str
    sender: str
    recipient: str
    cc: list[str]


# ── Styling constants ─────────────────────────────────────────────────────────
_PRIMARY_COLOR = "#1a56db"
_ACCENT_HIGH = "#dc2626"    # High priority / High severity
_ACCENT_MED  = "#d97706"    # Medium
_ACCENT_LOW  = "#16a34a"    # Low
_BG_LIGHT    = "#f8fafc"
_BORDER      = "#e2e8f0"


def _priority_badge(level: str) -> str:
    colors = {
        "High": (_ACCENT_HIGH, "#fff"),
        "Medium": (_ACCENT_MED, "#fff"),
        "Low": (_ACCENT_LOW, "#fff"),
    }
    bg, fg = colors.get(level, ("#6b7280", "#fff"))
    return (
        f'<span style="background:{bg};color:{fg};padding:2px 8px;'
        f'border-radius:9999px;font-size:11px;font-weight:600;">{level}</span>'
    )


def _html_table_rows(items: list[str]) -> str:
    return "".join(f"<li style='margin:4px 0;'>{item}</li>" for item in items)


def _build_html(artifact: RequirementsArtifact, recipient_name: str) -> str:
    today = datetime.now(timezone.utc).strftime("%d %B %Y")

    # ── Functional Requirements ───────────────────────────────────────────────
    fr_rows = ""
    for fr in artifact.functional_requirements:
        fr_rows += f"""
        <tr>
          <td style="padding:8px 12px;border-bottom:1px solid {_BORDER};
                     font-size:13px;color:#374151;white-space:nowrap;">{fr.id}</td>
          <td style="padding:8px 12px;border-bottom:1px solid {_BORDER};
                     font-size:13px;font-weight:600;color:#111827;">{fr.title}</td>
          <td style="padding:8px 12px;border-bottom:1px solid {_BORDER};
                     font-size:13px;color:#374151;">{fr.description}</td>
          <td style="padding:8px 12px;border-bottom:1px solid {_BORDER};
                     text-align:center;">{_priority_badge(fr.priority)}</td>
        </tr>"""

    # ── NFRs ─────────────────────────────────────────────────────────────────
    nfr_rows = ""
    for nfr in artifact.non_functional_requirements:
        nfr_rows += f"""
        <tr>
          <td style="padding:8px 12px;border-bottom:1px solid {_BORDER};
                     font-size:13px;color:#374151;">{nfr.id}</td>
          <td style="padding:8px 12px;border-bottom:1px solid {_BORDER};
                     font-size:13px;font-weight:600;color:#111827;">{nfr.category}</td>
          <td style="padding:8px 12px;border-bottom:1px solid {_BORDER};
                     font-size:13px;color:#374151;">{nfr.description}</td>
        </tr>"""

    # ── Risks ─────────────────────────────────────────────────────────────────
    risk_rows = ""
    for r in artifact.risks:
        risk_rows += f"""
        <tr>
          <td style="padding:8px 12px;border-bottom:1px solid {_BORDER};
                     font-size:13px;">{r.id}</td>
          <td style="padding:8px 12px;border-bottom:1px solid {_BORDER};
                     font-size:13px;color:#374151;">{r.risk}</td>
          <td style="padding:8px 12px;border-bottom:1px solid {_BORDER};
                     text-align:center;">{_priority_badge(r.severity)}</td>
          <td style="padding:8px 12px;border-bottom:1px solid {_BORDER};
                     font-size:13px;color:#374151;">{r.mitigation}</td>
        </tr>"""

    # ── Assumptions ───────────────────────────────────────────────────────────
    assumption_items = "".join(
        f'<li style="margin:6px 0;font-size:13px;color:#374151;">'
        f'<strong>{a.id}:</strong> {a.assumption}</li>'
        for a in artifact.assumptions
    )

    # ── Questions ─────────────────────────────────────────────────────────────
    question_items = "".join(
        f'<li style="margin:8px 0;">'
        f'<span style="font-size:13px;color:#111827;font-weight:600;">{q.question}</span><br>'
        f'<span style="font-size:12px;color:#6b7280;font-style:italic;">Rationale: {q.rationale}</span>'
        f'</li>'
        for q in artifact.questions_for_client
    )

    # ── Missing Information ───────────────────────────────────────────────────
    missing_block = ""
    if artifact.missing_information:
        missing_items = "".join(
            f'<li style="margin:4px 0;font-size:13px;color:#92400e;">{item}</li>'
            for item in artifact.missing_information
        )
        missing_block = f"""
        <div style="background:#fffbeb;border:1px solid #fcd34d;border-radius:6px;
                    padding:16px 20px;margin-top:24px;">
          <h3 style="margin:0 0 8px 0;font-size:14px;color:#92400e;">
            ⚠️ Information Gaps Identified
          </h3>
          <ul style="margin:0;padding-left:20px;">{missing_items}</ul>
        </div>"""

    def _section(title: str, content: str) -> str:
        return f"""
        <div style="margin-bottom:28px;">
          <h2 style="font-size:16px;font-weight:700;color:{_PRIMARY_COLOR};
                     border-bottom:2px solid {_PRIMARY_COLOR};padding-bottom:6px;
                     margin:0 0 12px 0;">{title}</h2>
          {content}
        </div>"""

    fr_table = f"""
    <table style="width:100%;border-collapse:collapse;">
      <thead><tr style="background:{_BG_LIGHT};">
        <th style="padding:8px 12px;text-align:left;font-size:12px;
                   color:#6b7280;border-bottom:2px solid {_BORDER};">ID</th>
        <th style="padding:8px 12px;text-align:left;font-size:12px;
                   color:#6b7280;border-bottom:2px solid {_BORDER};">Feature</th>
        <th style="padding:8px 12px;text-align:left;font-size:12px;
                   color:#6b7280;border-bottom:2px solid {_BORDER};">Description</th>
        <th style="padding:8px 12px;text-align:center;font-size:12px;
                   color:#6b7280;border-bottom:2px solid {_BORDER};">Priority</th>
      </tr></thead>
      <tbody>{fr_rows}</tbody>
    </table>"""

    nfr_table = f"""
    <table style="width:100%;border-collapse:collapse;">
      <thead><tr style="background:{_BG_LIGHT};">
        <th style="padding:8px 12px;text-align:left;font-size:12px;
                   color:#6b7280;border-bottom:2px solid {_BORDER};">ID</th>
        <th style="padding:8px 12px;text-align:left;font-size:12px;
                   color:#6b7280;border-bottom:2px solid {_BORDER};">Category</th>
        <th style="padding:8px 12px;text-align:left;font-size:12px;
                   color:#6b7280;border-bottom:2px solid {_BORDER};">Requirement</th>
      </tr></thead>
      <tbody>{nfr_rows}</tbody>
    </table>"""

    risk_table = f"""
    <table style="width:100%;border-collapse:collapse;">
      <thead><tr style="background:{_BG_LIGHT};">
        <th style="padding:8px 12px;text-align:left;font-size:12px;
                   color:#6b7280;border-bottom:2px solid {_BORDER};">ID</th>
        <th style="padding:8px 12px;text-align:left;font-size:12px;
                   color:#6b7280;border-bottom:2px solid {_BORDER};">Risk</th>
        <th style="padding:8px 12px;text-align:center;font-size:12px;
                   color:#6b7280;border-bottom:2px solid {_BORDER};">Severity</th>
        <th style="padding:8px 12px;text-align:left;font-size:12px;
                   color:#6b7280;border-bottom:2px solid {_BORDER};">Mitigation</th>
      </tr></thead>
      <tbody>{risk_rows}</tbody>
    </table>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>Requirements Analysis</title>
</head>
<body style="margin:0;padding:0;font-family:'Segoe UI',Arial,sans-serif;
             background:#f1f5f9;">
  <table width="100%" cellpadding="0" cellspacing="0">
    <tr><td align="center" style="padding:24px 16px;">
      <table width="640" cellpadding="0" cellspacing="0"
             style="background:#ffffff;border-radius:8px;
                    box-shadow:0 1px 3px rgba(0,0,0,0.1);overflow:hidden;">

        <!-- Header -->
        <tr><td style="background:{_PRIMARY_COLOR};padding:28px 32px;">
          <h1 style="margin:0;color:#fff;font-size:22px;font-weight:700;">
            Requirements Analysis Report
          </h1>
          <p style="margin:6px 0 0 0;color:rgba(255,255,255,0.8);font-size:13px;">
            Prepared for: {recipient_name} &nbsp;|&nbsp; {today}
          </p>
        </td></tr>

        <!-- Body -->
        <tr><td style="padding:32px;">

          <p style="margin:0 0 20px 0;font-size:14px;color:#374151;line-height:1.6;">
            Dear {recipient_name},<br><br>
            Thank you for sharing your requirements with us. Please find below our
            structured analysis, including functional and non-functional requirements,
            identified risks, working assumptions, and questions we'd like to clarify
            before proceeding.
          </p>

          <!-- Executive Summary -->
          <div style="background:{_BG_LIGHT};border-left:4px solid {_PRIMARY_COLOR};
                      padding:14px 18px;border-radius:0 6px 6px 0;margin-bottom:28px;">
            <strong style="font-size:13px;color:{_PRIMARY_COLOR};">Executive Summary</strong>
            <p style="margin:6px 0 0 0;font-size:13px;color:#374151;line-height:1.6;">
              {artifact.summary}
            </p>
          </div>

          {_section("📋 Functional Requirements", fr_table)}
          {_section("⚙️ Non-Functional Requirements", nfr_table)}
          {_section("⚠️ Risks & Mitigations", risk_table)}
          {_section("📌 Working Assumptions",
                    f'<ul style="margin:0;padding-left:20px;">{assumption_items}</ul>')}
          {_section("❓ Questions for Your Team",
                    f'<ul style="margin:0;padding-left:20px;">{question_items}</ul>')}

          {missing_block}

          <p style="margin:28px 0 0 0;font-size:13px;color:#374151;line-height:1.6;">
            We look forward to your responses so we can refine this analysis and
            move into solution design. Please don't hesitate to schedule a call
            if you'd prefer to walk through these points together.
          </p>

          <p style="margin:20px 0 0 0;font-size:13px;color:#374151;">
            Kind regards,<br>
            <strong>Solutions Architecture Team</strong>
          </p>

        </td></tr>

        <!-- Footer -->
        <tr><td style="background:{_BG_LIGHT};padding:16px 32px;
                        border-top:1px solid {_BORDER};">
          <p style="margin:0;font-size:11px;color:#9ca3af;text-align:center;">
            This document was auto-generated on {today}.
            Confidential — for the intended recipient only.
          </p>
        </td></tr>

      </table>
    </td></tr>
  </table>
</body>
</html>"""


def _build_text(artifact: RequirementsArtifact, recipient_name: str) -> str:
    today = datetime.now(timezone.utc).strftime("%d %B %Y")
    lines: list[str] = []

    lines.append(f"REQUIREMENTS ANALYSIS REPORT")
    lines.append(f"Prepared for: {recipient_name}  |  {today}")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"Dear {recipient_name},")
    lines.append("")
    lines.append(
        "Please find below our structured analysis of the requirements you shared."
    )
    lines.append("")

    lines.append("EXECUTIVE SUMMARY")
    lines.append("-" * 40)
    lines.append(artifact.summary)
    lines.append("")

    lines.append("FUNCTIONAL REQUIREMENTS")
    lines.append("-" * 40)
    for fr in artifact.functional_requirements:
        lines.append(f"[{fr.id}] [{fr.priority}] {fr.title}")
        lines.append(f"  {fr.description}")
    lines.append("")

    lines.append("NON-FUNCTIONAL REQUIREMENTS")
    lines.append("-" * 40)
    for nfr in artifact.non_functional_requirements:
        lines.append(f"[{nfr.id}] [{nfr.category}] {nfr.description}")
    lines.append("")

    lines.append("RISKS & MITIGATIONS")
    lines.append("-" * 40)
    for r in artifact.risks:
        lines.append(f"[{r.id}] [{r.severity}] {r.risk}")
        lines.append(f"  Mitigation: {r.mitigation}")
    lines.append("")

    lines.append("ASSUMPTIONS")
    lines.append("-" * 40)
    for a in artifact.assumptions:
        lines.append(f"[{a.id}] {a.assumption}")
    lines.append("")

    lines.append("QUESTIONS FOR YOUR TEAM")
    lines.append("-" * 40)
    for q in artifact.questions_for_client:
        lines.append(f"[{q.id}] {q.question}")
        lines.append(f"  Why: {q.rationale}")
    lines.append("")

    if artifact.missing_information:
        lines.append("INFORMATION GAPS")
        lines.append("-" * 40)
        for item in artifact.missing_information:
            lines.append(f"• {item}")
        lines.append("")

    lines.append("Kind regards,")
    lines.append("Solutions Architecture Team")

    return "\n".join(lines)


# ── Public API ────────────────────────────────────────────────────────────────

def format_email(
    artifact: RequirementsArtifact,
    sender: str,
    recipient: str,
    cc: list[str],
    recipient_name: str = "Team",
) -> EmailPayload:
    """
    Build a complete EmailPayload from a RequirementsArtifact.

    Args:
        artifact:       Parsed requirements artifact.
        sender:         From address (Gmail).
        recipient:      Primary To address.
        cc:             List of CC addresses (may be empty).
        recipient_name: Name used in greeting (default: "Team").

    Returns:
        EmailPayload ready for gmail_sender.send_email().
    """
    today = datetime.now(timezone.utc).strftime("%d %B %Y")
    subject = f"Requirements Analysis — {today}"

    html_body = _build_html(artifact, recipient_name)
    text_body = _build_text(artifact, recipient_name)

    logger.info("Email formatted (subject: '%s').", subject)

    return EmailPayload(
        subject=subject,
        html_body=html_body,
        text_body=text_body,
        sender=sender,
        recipient=recipient,
        cc=cc,
    )