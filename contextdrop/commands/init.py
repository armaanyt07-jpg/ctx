"""Implementation for `ctx init`."""

from __future__ import annotations

import json
from pathlib import Path

from contextdrop.config import project_name
from contextdrop.constants import BRAIN_FILE, CONFIG_FILE, CTX_DIR, DEFAULT_CONFIG, HANDOFF_FILE, SYSTEM_PROMPT_FILE, TASKS_FILE
from contextdrop.core.context_builder import build_system_prompt
from contextdrop.services.filesystem import get_file_tree
from contextdrop.services.parser import extract_section
from contextdrop.utils.formatting import B, D, X, ok, warn


def now() -> str:
    import datetime as dt

    return dt.datetime.now().strftime("%Y-%m-%d %H:%M")


def detect_stack() -> str:
    stack_hints: list[str] = []
    package_json = Path("package.json")

    if package_json.exists():
        try:
            pkg = json.loads(package_json.read_text(encoding="utf-8"))
            deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
            if "react" in deps:
                stack_hints.append("React")
            if "next" in deps:
                stack_hints.append("Next.js")
            if "vue" in deps:
                stack_hints.append("Vue")
            if "express" in deps:
                stack_hints.append("Express")
            if "fastify" in deps:
                stack_hints.append("Fastify")
            if "typescript" in deps:
                stack_hints.append("TypeScript")
            if not stack_hints:
                stack_hints.append("Node.js")
        except Exception:
            stack_hints.append("Node.js")

    if Path("requirements.txt").exists() or Path("pyproject.toml").exists():
        stack_hints.append("Python")
    if Path("go.mod").exists():
        stack_hints.append("Go")
    if Path("Cargo.toml").exists():
        stack_hints.append("Rust")
    if not stack_hints:
        stack_hints.append("Unknown - fill in manually")

    return ", ".join(stack_hints)


def run() -> None:
    if CTX_DIR.is_dir():
        warn(".ctx/ already exists. Re-initializing metadata only.")
    CTX_DIR.mkdir(exist_ok=True)

    name = project_name()
    stack = detect_stack()
    tree = get_file_tree()

    if not BRAIN_FILE.exists():
        brain = f"""# Project: {name}
_Last updated: {now()}_

## Stack
{stack}

## Architecture decisions
<!-- Key choices made: DB, auth method, patterns, why you chose X over Y -->
- 

## Key files
{tree}

## Environment / config
<!-- Important env vars, ports, external services -->
- 

## Naming conventions
<!-- How you name things: camelCase? snake_case? file structure? -->
- 
"""
        BRAIN_FILE.write_text(brain, encoding="utf-8")
        ok(f"Created {BRAIN_FILE}")
    else:
        ok(f"{BRAIN_FILE} exists - skipped")

    if not TASKS_FILE.exists():
        TASKS_FILE.write_text(
            json.dumps({"done": [], "in_progress": [], "todo": [], "blocked": []}, indent=2),
            encoding="utf-8",
        )
        ok(f"Created {TASKS_FILE}")
    else:
        ok(f"{TASKS_FILE} exists - skipped")

    if not HANDOFF_FILE.exists():
        HANDOFF_FILE.write_text(f"# Handoff - {name}\n\n_No sessions saved yet. Run: ctx save_\n", encoding="utf-8")
        ok(f"Created {HANDOFF_FILE}")
    else:
        ok(f"{HANDOFF_FILE} exists - skipped")

    if not CONFIG_FILE.exists():
        CONFIG_FILE.write_text(json.dumps(DEFAULT_CONFIG, indent=2), encoding="utf-8")
        ok(f"Created {CONFIG_FILE}")
    else:
        ok(f"{CONFIG_FILE} exists - skipped")

    SYSTEM_PROMPT_FILE.write_text(build_system_prompt(name), encoding="utf-8")
    ok(f"Created {SYSTEM_PROMPT_FILE}")

    gitignore_path = Path(".gitignore")
    note = "# ContextDrop watch log\n.ctx/watch.log\n"
    if gitignore_path.exists():
        content = gitignore_path.read_text(encoding="utf-8")
        if "watch.log" not in content:
            gitignore_path.write_text(content + "\n" + note, encoding="utf-8")
            ok("Updated .gitignore (watch.log excluded, brain tracked)")
    else:
        gitignore_path.write_text(note, encoding="utf-8")
        ok("Created .gitignore")

    print(f"""
{B}ContextDrop initialized for {name}{X}

{D}Next steps:{X}
  1. Edit {BRAIN_FILE} - fill in your stack + decisions
  2. Use the system prompt in {SYSTEM_PROMPT_FILE} at the start of every agent session
  3. Run {B}ctx save{X} at the end of each session (or mid-session)
  4. Run {B}ctx load{X} to get the handoff prompt for a new agent

{D}Auto-save tip:{X}
  Paste the system prompt into your agent - it will auto-append CTX-UPDATE
  blocks that ctx save will pick up automatically.
""")


__all__ = ["run", "detect_stack", "extract_section"]
