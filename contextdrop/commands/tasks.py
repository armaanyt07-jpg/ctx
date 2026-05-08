"""Task board commands and persistence."""

from __future__ import annotations

import copy
import datetime as dt
import json

from contextdrop.config import ensure_ctx
from contextdrop.constants import TASKS_FILE, TASK_BOARD_TEMPLATE
from contextdrop.utils.formatting import C, D, G, R, X, Y, err, head, ok


def now() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M")


def load_tasks() -> dict:
    if not TASKS_FILE.exists():
        return copy.deepcopy(TASK_BOARD_TEMPLATE)
    try:
        data = json.loads(TASKS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return copy.deepcopy(TASK_BOARD_TEMPLATE)
    return normalize_tasks(data)


def normalize_tasks(data: object) -> dict:
    tasks = copy.deepcopy(TASK_BOARD_TEMPLATE)
    if not isinstance(data, dict):
        return tasks
    for key in TASK_BOARD_TEMPLATE:
        value = data.get(key, [])
        tasks[key] = value if isinstance(value, list) else []
    return tasks


def save_tasks(tasks: dict) -> None:
    TASKS_FILE.write_text(json.dumps(tasks, indent=2), encoding="utf-8")


def add(task_text: str) -> None:
    ensure_ctx()
    tasks = load_tasks()
    tasks.setdefault("todo", []).append({"task": task_text, "added": now()})
    save_tasks(tasks)
    ok(f"Added to TODO: {task_text}")


def done(identifier: str) -> None:
    ensure_ctx()
    tasks = load_tasks()
    todo = tasks.get("todo", [])

    try:
        idx = int(identifier) - 1
        if 0 <= idx < len(todo):
            item = todo.pop(idx)
            item["completed"] = now()
            tasks.setdefault("done", []).append(item)
            save_tasks(tasks)
            ok(f"Marked done: {item.get('task', item)}")
            return
    except ValueError:
        pass

    for i, item in enumerate(todo):
        task = item.get("task", item) if isinstance(item, dict) else item
        if identifier.lower() in task.lower():
            item = todo.pop(i)
            if isinstance(item, dict):
                item["completed"] = now()
            else:
                item = {"task": item, "completed": now()}
            tasks.setdefault("done", []).append(item)
            save_tasks(tasks)
            ok(f"Marked done: {item.get('task', item)}")
            return

    err(f"Couldn't find task matching: {identifier}")


def status() -> None:
    from contextdrop.config import project_name
    from contextdrop.constants import BRAIN_FILE, HANDOFF_FILE
    from contextdrop.services.parser import extract_saved_timestamp
    from contextdrop.utils.formatting import B

    ensure_ctx()
    tasks = load_tasks()

    head(f"ctx status - {project_name()}")

    sections = [
        ("In progress", "in_progress", C),
        ("TODO", "todo", Y),
        ("Done", "done", G),
        ("Blocked", "blocked", R),
    ]

    for label, key, color in sections:
        items = tasks.get(key, [])
        print(f"{B}{color}{label}{X} ({len(items)})")
        for item in items[-8:]:
            task = item.get("task", item) if isinstance(item, dict) else item
            print(f"  {D}-{X} {task}")
        print()

    if HANDOFF_FILE.exists():
        saved = extract_saved_timestamp(HANDOFF_FILE.read_text(encoding="utf-8"))
        if saved:
            print(f"{D}Last saved: {saved}{X}")

    print(f"\n{D}Files: {BRAIN_FILE} | {TASKS_FILE} | {HANDOFF_FILE}{X}\n")
