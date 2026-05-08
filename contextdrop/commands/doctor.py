"""Health checks for ContextDrop setup and project state."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

from contextdrop.config import load_config
from contextdrop.constants import BRAIN_FILE, CONFIG_FILE, CTX_DIR, HANDOFF_FILE, SYSTEM_PROMPT_FILE, TASKS_FILE, VERSION
from contextdrop.services import git as git_service
from contextdrop.utils.formatting import err, head, ok, warn


def run() -> None:
    head("ctx doctor")
    issues = 0

    print(f"ContextDrop: {VERSION}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Project: {Path.cwd()}")
    print()

    if shutil.which("python"):
        ok("python is available")
    else:
        warn("python was not found on PATH")
        issues += 1

    if shutil.which("ctx") or shutil.which("ctx.cmd"):
        ok("ctx launcher is available on PATH")
    else:
        warn("ctx is not on PATH yet; run install.ps1 or use python path\\to\\ctx.py")

    if git_service.git_available():
        ok("git is available")
        if git_service.is_git_repo():
            branch = git_service.branch_name()
            ok(f"inside a git repository{f' on {branch}' if branch else ''}")
        else:
            warn("not inside a git repository; git-aware save summaries will be limited")
    else:
        warn("git is not available; save still works without changed-file summaries")

    if not CTX_DIR.exists():
        warn("no .ctx folder found; run ctx init in this project")
        issues += 1
    else:
        ok(".ctx folder exists")
        for path in [BRAIN_FILE, TASKS_FILE, HANDOFF_FILE, SYSTEM_PROMPT_FILE, CONFIG_FILE]:
            if path.exists():
                ok(f"{path} exists")
            else:
                warn(f"{path} is missing")
                issues += 1
        issues += _check_tasks_file()
        issues += _check_config_file()

    if issues:
        err(f"Doctor found {issues} issue(s).")
    ok("Doctor found no blocking issues.")


def _check_tasks_file() -> int:
    if not TASKS_FILE.exists():
        return 0
    try:
        data = json.loads(TASKS_FILE.read_text(encoding="utf-8"))
    except Exception:
        warn(f"{TASKS_FILE} is not valid JSON")
        return 1

    issues = 0
    for key in ["done", "in_progress", "todo", "blocked"]:
        if key not in data:
            warn(f"{TASKS_FILE} is missing '{key}'")
            issues += 1
        elif not isinstance(data[key], list):
            warn(f"{TASKS_FILE} field '{key}' should be a list")
            issues += 1
    return issues


def _check_config_file() -> int:
    if not CONFIG_FILE.exists():
        return 0
    try:
        config = load_config()
    except Exception:
        warn(f"{CONFIG_FILE} could not be loaded")
        return 1
    issues = 0
    for key in ["max_changed_files", "max_diff_stat_lines", "max_file_tree_entries", "watch_interval_seconds"]:
        if not isinstance(config.get(key), int) or config[key] <= 0:
            warn(f"{CONFIG_FILE} field '{key}' should be a positive number")
            issues += 1
    for key in ["ignore", "watch_extensions"]:
        if not isinstance(config.get(key), list):
            warn(f"{CONFIG_FILE} field '{key}' should be a list")
            issues += 1
    return issues
