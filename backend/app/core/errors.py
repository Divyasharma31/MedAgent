"""
core/errors.py — Application-wide exception types.

Phase 0: minimal set needed to support the health endpoint and factory.
Later phases will add domain-specific errors (AgentError, ValidationError, etc.).
"""

from __future__ import annotations


class CDSSError(Exception):
    """Base class for all application errors."""


class ConfigurationError(CDSSError):
    """Raised when required configuration is missing or invalid."""


class ProviderNotFoundError(CDSSError):
    """Raised when an unknown LLM_PROVIDER value is requested."""


class IdentifierBlockedError(CDSSError):
    """
    Raised when an obvious personal identifier is detected in input before an
    external call would have been made.  Callers must return an error to the
    user without making any external call.
    """

