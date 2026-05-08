"""Task summary helpers."""

from __future__ import annotations


def format_tasks_summary(tasks: dict) -> str:
    lines: list[str] = []
    for key in ["in_progress", "todo", "done", "blocked"]:
        items = tasks.get(key, [])
        if items:
            lines.append(f"{key.replace('_', ' ').title()} ({len(items)}):")
            for item in items[-5:]:
                task = item.get("task", item) if isinstance(item, dict) else item
                lines.append(f"  - {task}")
    return "\n".join(lines) or "(empty)"


def task_lines(items: list, prefix: str = "- [ ]") -> str:
    if not items:
        return "  _none_"
    lines = []
    for item in items:
        task = item.get("task", item) if isinstance(item, dict) else item
        ts = item.get("completed") or item.get("added", "") if isinstance(item, dict) else ""
        suffix = f" `{ts}`" if ts else ""
        lines.append(f"  {prefix} {task}{suffix}")
    return "\n".join(lines)
