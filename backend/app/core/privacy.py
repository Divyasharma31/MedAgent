"""
core/privacy.py — Input de-identification and log-redaction utilities.

Phase 0: only the identifier-detection / blocking logic used by the config
guard.  Full de-identification (before external LLM calls) is wired in Phase 2
when real providers are added.

§12B distinction:
- Log redaction  → what is stored (hashes, codes, IDs, masked text).
- Input de-identification → what is sent to external providers (best-effort
  regex masking of obvious identifiers: phone, email, long digit strings).

Neither control guarantees anonymity; they are safety nets for accidents.
Real data must not enter the system.
"""

from __future__ import annotations

import re

# Patterns that indicate obvious personal identifiers.
# Deliberately conservative: false positives (blocking a benign message) are
# acceptable; false negatives (letting a real identifier through) are not.
_PHONE_RE = re.compile(
    r"""
    (?:
        \+?91[\s\-]?         # optional India country code
    )?
    [6-9]\d{9}              # 10-digit mobile starting 6-9
    |
    \b\d{10,13}\b           # any 10-13 digit run (generic phone / ID)
    """,
    re.VERBOSE,
)

_EMAIL_RE = re.compile(
    r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b"
)

# Aadhaar: 12-digit number, optionally grouped in 4s.
_AADHAAR_RE = re.compile(
    r"\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b"
)


def contains_identifier(text: str) -> bool:
    """
    Return True if ``text`` appears to contain an obvious personal identifier.
    Used by the request guard (§12B) to block before any external call.
    """
    return bool(
        _PHONE_RE.search(text)
        or _EMAIL_RE.search(text)
        or _AADHAAR_RE.search(text)
    )


def redact_for_log(text: str) -> str:
    """
    Replace obvious identifiers with placeholder tokens for log storage.
    Does NOT make the text safe to send externally — use a separate
    de-identification step for that.
    """
    text = _EMAIL_RE.sub("[EMAIL]", text)
    text = _AADHAAR_RE.sub("[AADHAAR]", text)
    text = _PHONE_RE.sub("[PHONE]", text)
    return text

