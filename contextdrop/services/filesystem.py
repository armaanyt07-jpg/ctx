"""Filesystem helpers used by ContextDrop commands."""

from __future__ import annotations

from pathlib import Path

from contextdrop.constants import WATCH_EXTENSIONS, WATCH_IGNORE


def get_file_tree(max_depth: int = 2) -> str:
    lines: list[str] = []

    def walk(path: Path, depth: int) -> None:
        if depth > max_depth:
            return
        try:
            entries = sorted(path.iterdir(), key=lambda item: item.name)
        except PermissionError:
            return

        for entry in entries:
            if entry.name in WATCH_IGNORE or entry.name.startswith("."):
                continue
            indent = "  " * depth
            if entry.is_dir():
                lines.append(f"{indent}{entry.name}/")
                walk(entry, depth + 1)
            else:
                lines.append(f"{indent}{entry.name}")

    walk(Path("."), 0)
    return "\n".join(lines[:60]) or "(empty project)"


def get_watch_snapshot() -> dict[str, float]:
    snap: dict[str, float] = {}
    for path in Path(".").rglob("*"):
        if any(part in WATCH_IGNORE for part in path.parts):
            continue
        if not path.is_file() or path.suffix not in WATCH_EXTENSIONS:
            continue
        try:
            snap[path.as_posix()] = path.stat().st_mtime
        except OSError:
            pass
    return snap
