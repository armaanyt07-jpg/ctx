"""Implementation for `ctx save`."""

from __future__ import annotations

import re

from contextdrop.commands.tasks import load_tasks, now, save_tasks
from contextdrop.config import ensure_ctx, project_name
from contextdrop.constants import BRAIN_FILE, HANDOFF_FILE
from contextdrop.core.summarizer import format_tasks_summary
from contextdrop.services.git import changed_files, diff_stat
from contextdrop.services.parser import extract_section
from contextdrop.utils.formatting import B, C, X, ok


def run(interactive: bool = False) -> None:
    ensure_ctx()

    if interactive:
        _run_interactive()
        return

    timestamp = now()
    tasks = load_tasks()
    save_tasks(tasks)

    brain = BRAIN_FILE.read_text(encoding="utf-8") if BRAIN_FILE.exists() else ""
    done_items = tasks.get("done", [])[-3:]
    todo_items = tasks.get("todo", [])
    blocked_items = tasks.get("blocked", [])
    changed = changed_files()
    stat = diff_stat()

    what_done = _build_auto_summary(done_items, changed, stat)
    decisions = extract_section(brain, "Architecture decisions") or "(none)"
    blockers = _task_list(blocked_items) or "(none)"
    next_task = _first_task(todo_items) or "(not specified)"

    _write_handoff(timestamp, what_done, decisions, blockers, next_task, tasks)
    _touch_brain(timestamp)

    ok("Context saved automatically.")
    ok(f"Handoff written to {HANDOFF_FILE}")
    print(f"\n  Run {B}ctx load{X} to get the prompt for your next agent.\n")


def _run_interactive() -> None:
    print(f"""
{B}ctx save{X} - saving session state

Answer these questions (press Enter to skip any):
""")

    what_done = input(f"  {C}What was completed this session?{X}\n  > ").strip()
    decisions = input(f"\n  {C}Any architecture/tech decisions made?{X}\n  > ").strip()
    blockers = input(f"\n  {C}Any blockers or known bugs?{X}\n  > ").strip()
    next_task = input(f"\n  {C}What should the next agent do first?{X}\n  > ").strip()

    timestamp = now()
    tasks = load_tasks()
    if what_done:
        tasks["done"].append({"task": what_done, "completed": timestamp})
    if next_task:
        tasks["todo"].insert(0, {"task": next_task, "added": timestamp, "priority": "high"})
    save_tasks(tasks)

    _write_handoff(timestamp, what_done or "(not recorded)", decisions or "(none)", blockers or "(none)", next_task or "(not specified)", tasks)
    _touch_brain(timestamp)

    ok("Session saved.")
    ok(f"Handoff written to {HANDOFF_FILE}")
    print(f"\n  Run {B}ctx load{X} to get the prompt for your next agent.\n")


def _write_handoff(timestamp: str, what_done: str, decisions: str, blockers: str, next_task: str, tasks: dict) -> None:
    handoff = f"""# Handoff - {project_name()}
_Saved: {timestamp}_

## What was done this session
{what_done}

## Decisions made
{decisions}

## Known blockers / bugs
{blockers}

## Next task for new agent
{next_task}

## Task board
{format_tasks_summary(tasks)}
"""
    HANDOFF_FILE.write_text(handoff, encoding="utf-8")


def _touch_brain(timestamp: str) -> None:
    brain = BRAIN_FILE.read_text(encoding="utf-8")
    brain = re.sub(r"_Last updated:.*?_", f"_Last updated: {timestamp}_", brain)
    BRAIN_FILE.write_text(brain, encoding="utf-8")


def _task_list(items: list) -> str:
    lines = []
    for item in items:
        task = item.get("task", item) if isinstance(item, dict) else item
        lines.append(f"- {task}")
    return "\n".join(lines)


def _first_task(items: list) -> str:
    if not items:
        return ""
    item = items[0]
    return item.get("task", item) if isinstance(item, dict) else item


def _build_auto_summary(done_items: list, changed: list[str], stat: str) -> str:
    sections = []
    done = _task_list(done_items)
    if done:
        sections.append(done)
    if changed:
        files = "\n".join(f"- {path}" for path in changed)
        sections.append(f"Changed files:\n{files}")
    if stat:
        sections.append(f"Diff stat:\n```text\n{stat}\n```")
    return "\n\n".join(sections) or "Saved current project context snapshot."
