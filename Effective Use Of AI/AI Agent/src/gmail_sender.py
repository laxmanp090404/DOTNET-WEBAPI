"""
gmail_sender.py — Sends emails via Gmail SMTP using an App Password.

Responsibilities:
  - Build a MIMEMultipart message with HTML + plain-text parts.
  - Connect to Gmail SMTP over TLS (port 587 STARTTLS).
  - Authenticate with App Password.
  - Send with retry on transient SMTP errors.
  - Never log the App Password.
"""

from __future__ import annotations

import logging
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.email_formatter import EmailPayload

logger = logging.getLogger(__name__)

_SMTP_HOST = "smtp.gmail.com"
_SMTP_PORT = 587
_MAX_RETRIES = 3
_BASE_BACKOFF = 2.0

# SMTP errors that are worth retrying
_TRANSIENT_CODES = {421, 450, 451, 452}


def _build_mime(payload: EmailPayload) -> MIMEMultipart:
    """Construct a MIME multipart/alternative message."""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = payload.subject
    msg["From"] = payload.sender
    msg["To"] = payload.recipient
    if payload.cc:
        msg["Cc"] = ", ".join(payload.cc)

    # Plain text first (lower priority), HTML second (higher priority)
    msg.attach(MIMEText(payload.text_body, "plain", "utf-8"))
    msg.attach(MIMEText(payload.html_body, "html", "utf-8"))
    return msg


def send_email(payload: EmailPayload, app_password: str) -> None:
    """
    Send the email via Gmail SMTP with retry on transient errors.

    Args:
        payload:      Complete email payload from email_formatter.
        app_password: Gmail App Password (16 characters, no spaces).

    Raises:
        smtplib.SMTPAuthenticationError: If credentials are rejected.
        smtplib.SMTPException:           If sending fails after all retries.
        RuntimeError:                    If all retries are exhausted.
    """
    recipients = [payload.recipient] + payload.cc
    msg = _build_mime(payload)

    last_error: Exception | None = None

    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            logger.info(
                "SMTP attempt %d/%d → %s (to: %s)",
                attempt,
                _MAX_RETRIES,
                _SMTP_HOST,
                payload.recipient,
            )
            with smtplib.SMTP(_SMTP_HOST, _SMTP_PORT, timeout=30) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                # Log sender but NEVER log the password
                logger.debug("Authenticating as %s", payload.sender)
                server.login(payload.sender, app_password)
                server.sendmail(payload.sender, recipients, msg.as_string())

            logger.info(
                "Email sent successfully to %s (CC: %s).",
                payload.recipient,
                payload.cc or "none",
            )
            return  # Success — exit immediately

        except smtplib.SMTPAuthenticationError as exc:
            # Auth failures are permanent — do not retry
            raise smtplib.SMTPAuthenticationError(
                exc.smtp_code,
                (
                    "Gmail authentication failed. Ensure:\n"
                    "  1. 2-Step Verification is enabled on the sending account.\n"
                    "  2. GMAIL_APP_PASSWORD is a 16-character App Password.\n"
                    "  3. The password in .env has no spaces.\n"
                    f"  Original error: {exc.smtp_error}"
                ),
            ) from exc

        except smtplib.SMTPResponseException as exc:
            if exc.smtp_code in _TRANSIENT_CODES:
                last_error = exc
                logger.warning(
                    "Transient SMTP error %d on attempt %d: %s",
                    exc.smtp_code,
                    attempt,
                    exc.smtp_error,
                )
            else:
                raise  # Permanent error — re-raise immediately

        except (smtplib.SMTPException, OSError, TimeoutError) as exc:
            last_error = exc
            logger.warning("SMTP error on attempt %d: %s", attempt, exc)

        if attempt < _MAX_RETRIES:
            backoff = _BASE_BACKOFF * (2 ** (attempt - 1))
            logger.info("Retrying SMTP in %.1f seconds...", backoff)
            time.sleep(backoff)

    raise RuntimeError(
        f"Failed to send email after {_MAX_RETRIES} attempts. "
        f"Last error: {last_error}"
    )