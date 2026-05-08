"""Project-wide constants for ContextDrop."""

from pathlib import Path

VERSION = "0.2.0"

CTX_DIR = Path(".ctx")
BRAIN_FILE = CTX_DIR / "brain.md"
TASKS_FILE = CTX_DIR / "tasks.json"
HANDOFF_FILE = CTX_DIR / "handoff.md"
SYSTEM_PROMPT_FILE = CTX_DIR / "system_prompt.md"
CONFIG_FILE = CTX_DIR / "config.json"
WATCH_LOG = CTX_DIR / "watch.log"

TASK_BOARD_TEMPLATE = {
    "done": [],
    "in_progress": [],
    "todo": [],
    "blocked": [],
}

WATCH_IGNORE = {
    ".ctx",
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "dist",
    "build",
    ".next",
    ".DS_Store",
}

WATCH_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".jsx",
    ".tsx",
    ".go",
    ".rs",
    ".java",
    ".rb",
    ".css",
    ".html",
    ".json",
    ".md",
    ".sql",
    ".env",
}

DEFAULT_CONFIG = {
    "max_changed_files": 8,
    "max_diff_stat_lines": 8,
    "max_file_tree_entries": 60,
    "watch_interval_seconds": 3,
    "ignore": sorted(WATCH_IGNORE),
    "watch_extensions": sorted(WATCH_EXTENSIONS),
}
