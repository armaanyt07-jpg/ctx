"""Implementation for `ctx parse`."""

from __future__ import annotations

import sys

from contextdrop.commands.tasks import load_tasks, now, save_tasks
from contextdrop.config import ensure_ctx
from contextdrop.constants import BRAIN_FILE
from contextdrop.services.parser import parse_ctx_update_blocks
from contextdrop.utils.formatting import ok, warn


def run() -> None:
    ensure_ctx()

    blocks = parse_ctx_update_blocks(sys.stdin.read())
    if not blocks:
        warn("No CTX-UPDATE blocks found in input.")
        return

    tasks = load_tasks()
    timestamp = now()

    for data in blocks:
        if data.get("done") and data["done"] not in ("none", ""):
            tasks.setdefault("done", []).append({"task": data["done"], "completed": timestamp, "auto": True})

        if data.get("next") and data["next"] not in ("none", ""):
            tasks.setdefault("todo", []).insert(0, {"task": data["next"], "added": timestamp, "priority": "high"})

        if data.get("decision") and data["decision"] not in ("none", ""):
            # Preserve the prototype's simple insertion behavior so decisions
            # still appear at the top of the existing Architecture section.
            brain = BRAIN_FILE.read_text(encoding="utf-8")
            decision_line = f"- [{timestamp}] {data['decision']}\n"
            brain = brain.replace("## Architecture decisions\n", f"## Architecture decisions\n{decision_line}")
            BRAIN_FILE.write_text(brain, encoding="utf-8")

    save_tasks(tasks)
    ok(f"Applied {len(blocks)} CTX-UPDATE block(s) from agent output.")
