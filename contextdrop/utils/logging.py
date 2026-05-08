"""Basic logging setup for package internals."""

from __future__ import annotations

import logging


def configure_logging(level: int = logging.WARNING) -> None:
    logging.basicConfig(
        level=level,
        format="%(levelname)s:%(name)s:%(message)s",
    )
