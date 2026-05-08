"""Markdown and CTX-UPDATE parsing helpers."""

from __future__ import annotations

import re


def extract_section(text: str, heading: str) -> str | None:
    """Extract content under a markdown ## heading."""
    pattern = rf"## {re.escape(heading)}\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None


def extract_saved_timestamp(handoff: str) -> str:
    match = re.search(r"_Saved: (.+?)_", handoff)
    return match.group(1) if match else ""


def parse_ctx_update_blocks(text: str) -> list[dict[str, str]]:
    pattern = r"---CTX-UPDATE---\s*(.*?)\s*---END-CTX-UPDATE---"
    blocks = re.findall(pattern, text, re.DOTALL)
    parsed: list[dict[str, str]] = []

    for block in blocks:
        data: dict[str, str] = {}
        for line in block.strip().splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                data[key.strip().lower()] = value.strip()
        parsed.append(data)

    return parsed
