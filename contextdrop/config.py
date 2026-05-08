"""Runtime configuration helpers."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from .constants import CONFIG_FILE, CTX_DIR, DEFAULT_CONFIG
from .utils.formatting import err


def project_root() -> Path:
    """Return the directory where the user invoked ctx.

    Original prototype behavior was cwd-relative, so this intentionally does
    not search parent directories for .ctx.
    """
    return Path.cwd()


def project_name() -> str:
    return project_root().name


def ensure_ctx() -> None:
    if not CTX_DIR.is_dir():
        err("No .ctx/ found. Run: ctx init")


def load_config() -> dict:
    config = copy.deepcopy(DEFAULT_CONFIG)
    if not CONFIG_FILE.exists():
        return config
    try:
        data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except Exception:
        return config
    if not isinstance(data, dict):
        return config
    for key, value in data.items():
        if key in config:
            config[key] = value
    return normalize_config(config)


def normalize_config(config: dict) -> dict:
    normalized = copy.deepcopy(DEFAULT_CONFIG)
    normalized.update(config)
    normalized["max_changed_files"] = _positive_int(normalized.get("max_changed_files"), 8)
    normalized["max_diff_stat_lines"] = _positive_int(normalized.get("max_diff_stat_lines"), 8)
    normalized["max_file_tree_entries"] = _positive_int(normalized.get("max_file_tree_entries"), 60)
    normalized["watch_interval_seconds"] = _positive_int(normalized.get("watch_interval_seconds"), 3)
    normalized["ignore"] = _string_list(normalized.get("ignore"), DEFAULT_CONFIG["ignore"])
    normalized["watch_extensions"] = _string_list(
        normalized.get("watch_extensions"),
        DEFAULT_CONFIG["watch_extensions"],
    )
    return normalized


def _positive_int(value: object, default: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return parsed if parsed > 0 else default


def _string_list(value: object, default: list[str]) -> list[str]:
    if not isinstance(value, list):
        return list(default)
    return [str(item) for item in value if str(item)]
