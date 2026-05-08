"""Filesystem helpers used by ContextDrop commands."""

from __future__ import annotations

from pathlib import Path

from contextdrop.config import load_config


def get_file_tree(max_depth: int = 2) -> str:
    config = load_config()
    ignore = set(config["ignore"])
    max_entries = int(config["max_file_tree_entries"])
    lines: list[str] = []

    def walk(path: Path, depth: int) -> None:
        if depth > max_depth:
            return
        try:
            entries = sorted(path.iterdir(), key=lambda item: item.name)
        except PermissionError:
            return

        for entry in entries:
            if entry.name in ignore or entry.name.startswith("."):
                continue
            indent = "  " * depth
            if entry.is_dir():
                lines.append(f"{indent}{entry.name}/")
                walk(entry, depth + 1)
            else:
                lines.append(f"{indent}{entry.name}")

    walk(Path("."), 0)
    return "\n".join(lines[:max_entries]) or "(empty project)"


def get_watch_snapshot() -> dict[str, float]:
    config = load_config()
    ignore = set(config["ignore"])
    extensions = set(config["watch_extensions"])
    snap: dict[str, float] = {}
    for path in Path(".").rglob("*"):
        if any(part in ignore for part in path.parts):
            continue
        if not path.is_file() or path.suffix not in extensions:
            continue
        try:
            snap[path.as_posix()] = path.stat().st_mtime
        except OSError:
            pass
    return snap
