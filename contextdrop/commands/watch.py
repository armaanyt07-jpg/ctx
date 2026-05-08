"""Implementation for `ctx watch`."""

from __future__ import annotations

import time

from contextdrop.commands.tasks import load_tasks, now, save_tasks
from contextdrop.config import ensure_ctx
from contextdrop.constants import WATCH_LOG
from contextdrop.services.filesystem import get_watch_snapshot
from contextdrop.utils.formatting import B, D, G, R, X, Y


def run() -> None:
    ensure_ctx()
    print(f"{B}ctx watch{X} - watching for file changes (Ctrl+C to stop)\n")

    prev = get_watch_snapshot()
    tasks = load_tasks()

    try:
        while True:
            time.sleep(3)
            curr = get_watch_snapshot()

            new_files = [p for p in curr if p not in prev]
            changed_files = [p for p in curr if p in prev and curr[p] != prev[p]]
            deleted_files = [p for p in prev if p not in curr]

            if new_files or changed_files or deleted_files:
                timestamp = now()
                log_lines = []

                for file_name in new_files:
                    msg = f"[{timestamp}] CREATED: {file_name}"
                    print(f"  {G}+{X} {file_name}")
                    log_lines.append(msg)
                    tasks.setdefault("done", []).append(
                        {"task": f"Created {file_name}", "completed": timestamp, "auto": True}
                    )

                for file_name in changed_files:
                    msg = f"[{timestamp}] MODIFIED: {file_name}"
                    print(f"  {Y}~{X} {file_name}")
                    log_lines.append(msg)

                for file_name in deleted_files:
                    msg = f"[{timestamp}] DELETED: {file_name}"
                    print(f"  {R}-{X} {file_name}")
                    log_lines.append(msg)

                WATCH_LOG.write_text(
                    WATCH_LOG.read_text(encoding="utf-8") + "\n".join(log_lines) + "\n"
                    if WATCH_LOG.exists()
                    else "\n".join(log_lines) + "\n",
                    encoding="utf-8",
                )

                save_tasks(tasks)
                prev = curr

    except KeyboardInterrupt:
        print(f"\n{D}ctx watch stopped.{X}")
