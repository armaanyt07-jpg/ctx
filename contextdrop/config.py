"""Runtime configuration helpers."""

from __future__ import annotations

from pathlib import Path

from .constants import CTX_DIR
from .utils.formatting import err


def project_root() -> Path:
    """Return the directory where the user invoked ctx.

    Original prototype behavior was cwd-relative, so this intentionally does
    not search parent directories for .ctx.
    """
    return Path.cwd()


def project_name() -> str:
    return project_root().name


def ensure_ctx() -> None:
    if not CTX_DIR.is_dir():
        err("No .ctx/ found. Run: ctx init")
