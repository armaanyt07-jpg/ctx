"""Small Git helpers used for automatic context summaries."""

from __future__ import annotations

import shutil
import subprocess

from contextdrop.config import load_config


def git_available() -> bool:
    return shutil.which("git") is not None


def is_git_repo() -> bool:
    if not git_available():
        return False
    result = _run_git(["rev-parse", "--is-inside-work-tree"])
    return result.returncode == 0 and result.stdout.strip() == "true"


def changed_files(limit: int = 8) -> list[str]:
    limit = int(load_config()["max_changed_files"]) if limit == 8 else limit
    if not is_git_repo():
        return []
    result = _run_git(["status", "--short"])
    if result.returncode != 0:
        return []

    files: list[str] = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        path = line[3:].strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        files.append(path)
        if len(files) >= limit:
            break
    return files


def diff_stat(limit: int = 8) -> str:
    limit = int(load_config()["max_diff_stat_lines"]) if limit == 8 else limit
    if not is_git_repo():
        return ""
    result = _run_git(["diff", "--stat"])
    if result.returncode != 0 or not result.stdout.strip():
        return ""
    return "\n".join(result.stdout.strip().splitlines()[:limit])


def branch_name() -> str:
    if not is_git_repo():
        return ""
    result = _run_git(["branch", "--show-current"])
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def _run_git(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], text=True, capture_output=True, check=False)
