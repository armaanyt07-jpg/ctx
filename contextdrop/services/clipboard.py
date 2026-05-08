"""Clipboard integration with cross-platform fallbacks."""

from __future__ import annotations

import shutil
import subprocess
from typing import Sequence


def copy_to_clipboard(text: str) -> bool:
    """Best-effort copy without making clipboard support a hard dependency."""
    commands: list[Sequence[str]] = []

    if shutil.which("pbcopy"):
        commands.append(["pbcopy"])
    if shutil.which("wl-copy"):
        commands.append(["wl-copy"])
    if shutil.which("xclip"):
        commands.append(["xclip", "-selection", "clipboard"])
    if shutil.which("clip"):
        commands.append(["clip"])

    for command in commands:
        try:
            subprocess.run(command, input=text.encode(), check=True)
            return True
        except Exception:
            continue

    return False
