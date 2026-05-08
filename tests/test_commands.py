from __future__ import annotations

import contextlib
import io
import json
import os
import shutil
import uuid
import unittest
from pathlib import Path

from contextdrop.cli import main
from contextdrop.config import load_config
from contextdrop.commands.tasks import load_tasks, normalize_tasks


class CommandTests(unittest.TestCase):
    def test_init_add_done_save_and_report(self) -> None:
        with temp_cwd() as workdir:
            main(["init"])
            self.assertTrue((workdir / ".ctx" / "brain.md").exists())
            self.assertTrue((workdir / ".ctx" / "config.json").exists())
            self.assertTrue((workdir / ".ctx" / "tasks.json").exists())

            main(["add", "write", "tests"])
            tasks = json.loads((workdir / ".ctx" / "tasks.json").read_text(encoding="utf-8"))
            self.assertEqual(tasks["todo"][0]["task"], "write tests")

            main(["done", "1"])
            tasks = json.loads((workdir / ".ctx" / "tasks.json").read_text(encoding="utf-8"))
            self.assertEqual(tasks["done"][0]["task"], "write tests")
            self.assertEqual(tasks["todo"], [])

            main(["save"])
            handoff = (workdir / ".ctx" / "handoff.md").read_text(encoding="utf-8")
            self.assertIn("write tests", handoff)

            main(["report"])
            self.assertTrue((workdir / "CONTEXT.md").exists())

    def test_parse_ctx_update_block(self) -> None:
        with temp_cwd() as workdir:
            main(["init"])
            update = """---CTX-UPDATE---
done: parsed task
decision: keep it simple
next: next task
bug: none
---END-CTX-UPDATE---
"""
            with patched_stdin(update):
                main(["parse"])

            tasks = json.loads((workdir / ".ctx" / "tasks.json").read_text(encoding="utf-8"))
            self.assertEqual(tasks["done"][0]["task"], "parsed task")
            self.assertEqual(tasks["todo"][0]["task"], "next task")
            brain = (workdir / ".ctx" / "brain.md").read_text(encoding="utf-8")
            self.assertIn("keep it simple", brain)

    def test_load_tasks_recovers_missing_or_bad_fields(self) -> None:
        self.assertEqual(normalize_tasks({"todo": "bad"})["todo"], [])
        with temp_cwd() as workdir:
            (workdir / ".ctx").mkdir()
            (workdir / ".ctx" / "tasks.json").write_text('{"todo": [{"task": "x"}]}', encoding="utf-8")
            tasks = load_tasks()
            self.assertEqual(tasks["todo"][0]["task"], "x")
            self.assertEqual(tasks["done"], [])

    def test_doctor_reports_missing_ctx_as_issue(self) -> None:
        with temp_cwd():
            with self.assertRaises(SystemExit):
                main(["doctor"])

    def test_config_controls_defaults_and_normalizes_bad_values(self) -> None:
        with temp_cwd() as workdir:
            main(["init"])
            config_path = workdir / ".ctx" / "config.json"
            config = json.loads(config_path.read_text(encoding="utf-8"))
            self.assertEqual(config["max_changed_files"], 8)

            config_path.write_text(
                json.dumps(
                    {
                        "max_changed_files": "2",
                        "watch_interval_seconds": 0,
                        "ignore": "bad",
                    }
                ),
                encoding="utf-8",
            )
            loaded = load_config()
            self.assertEqual(loaded["max_changed_files"], 2)
            self.assertEqual(loaded["watch_interval_seconds"], 3)
            self.assertIsInstance(loaded["ignore"], list)


@contextlib.contextmanager
def temp_cwd():
    previous = Path.cwd()
    root = Path(__file__).resolve().parent / "_tmp"
    root.mkdir(exist_ok=True)
    path = root / uuid.uuid4().hex
    path.mkdir()
    os.chdir(path)
    try:
        yield path
    finally:
        os.chdir(previous)
        shutil.rmtree(path, ignore_errors=True)


@contextlib.contextmanager
def patched_stdin(text: str):
    old_stdin = os.sys.stdin
    os.sys.stdin = io.StringIO(text)
    try:
        yield
    finally:
        os.sys.stdin = old_stdin


if __name__ == "__main__":
    unittest.main()
