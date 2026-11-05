"""
core/logging.py — Structured logging configuration.

Phase 0: standard-library logging configured from settings.
Later phases may switch to structlog or similar without changing the interface.
"""

from __future__ import annotations

import logging
import sys

from app.core.config import settings


def configure_logging() -> None:
    """
    Configure the root logger.  Call once at application startup.
    Log level is controlled by ``settings.log_level``.
    """
    level = getattr(logging, settings.log_level.upper(), logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S",
        )
    )
    root = logging.getLogger()
    root.setLevel(level)
    root.handlers = [handler]


def get_logger(name: str) -> logging.Logger:
    """Return a named logger.  Call after ``configure_logging()``."""
    return logging.getLogger(name)

