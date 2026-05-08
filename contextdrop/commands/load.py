"""Implementation for `ctx load` and `ctx report`."""

from __future__ import annotations

from contextdrop.commands.tasks import load_tasks
from contextdrop.config import ensure_ctx
from contextdrop.constants import BRAIN_FILE, HANDOFF_FILE
from contextdrop.core.context_builder import build_load_prompt, build_report_markdown
from contextdrop.services.clipboard import copy_to_clipboard
from contextdrop.utils.formatting import B, head, ok


def read_optional(path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def run() -> None:
    ensure_ctx()

    brain = read_optional(BRAIN_FILE)
    handoff = read_optional(HANDOFF_FILE)
    prompt = build_load_prompt(brain, handoff, load_tasks())

    head("Paste this into your new agent:")
    print(prompt)

    if copy_to_clipboard(prompt):
        ok("Also copied to clipboard!")


def report() -> None:
    ensure_ctx()

    md = build_report_markdown(read_optional(BRAIN_FILE), read_optional(HANDOFF_FILE), load_tasks())
    output_file = "CONTEXT.md"
    from pathlib import Path

    Path(output_file).write_text(md, encoding="utf-8")
    ok(f"Generated: {output_file}")
    print(f"\n  Drag this file into any AI agent (Claude, Cursor, ChatGPT)\n  or paste its contents at the start of a new session.\n")
