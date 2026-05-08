"""Dependency-free CLI entrypoint for ContextDrop.

The package still supports an installed `ctx` command through pyproject.toml,
but this module intentionally uses only the Python standard library so new
users can also run `python ctx.py ...` without installing dependencies first.
"""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from contextdrop.commands import init as init_command
from contextdrop.commands import doctor as doctor_command
from contextdrop.commands import load as load_command
from contextdrop.commands import parse as parse_command
from contextdrop.commands import save as save_command
from contextdrop.commands import tasks as tasks_command
from contextdrop.commands import watch as watch_command
from contextdrop.constants import VERSION
from contextdrop.utils.logging import configure_logging


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ctx",
        description="ContextDrop CLI - your project's brain for agent handoffs.",
    )
    parser.add_argument("--version", action="store_true", help="Show ContextDrop version.")

    subparsers = parser.add_subparsers(dest="command", metavar="command")
    subparsers.add_parser("init", help="Set up .ctx/ in this project.")
    save_parser = subparsers.add_parser("save", help="Save current session state.")
    save_parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="Ask manual session questions before writing the handoff.",
    )
    subparsers.add_parser("load", help="Print the handoff prompt for a new agent.")
    subparsers.add_parser("report", help="Generate CONTEXT.md.")
    subparsers.add_parser("status", help="Show the task board.")
    subparsers.add_parser("watch", help="Watch files and update the project brain.")
    subparsers.add_parser("parse", help="Read CTX-UPDATE blocks from stdin.")
    subparsers.add_parser("doctor", help="Check ContextDrop setup and project health.")

    add_parser = subparsers.add_parser("add", help="Add a todo.")
    add_parser.add_argument("task_text", nargs="+", help="Task description.")

    done_parser = subparsers.add_parser("done", help="Mark a todo as done.")
    done_parser.add_argument("identifier", help="Task number or keyword.")

    return parser


def main(argv: Sequence[str] | None = None) -> None:
    configure_logging()
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.version:
        print(f"ContextDrop {VERSION}")
        return

    if args.command == "init":
        init_command.run()
    elif args.command == "save":
        save_command.run(interactive=args.interactive)
    elif args.command == "load":
        load_command.run()
    elif args.command == "report":
        load_command.report()
    elif args.command == "status":
        tasks_command.status()
    elif args.command == "add":
        tasks_command.add(" ".join(args.task_text))
    elif args.command == "done":
        tasks_command.done(args.identifier)
    elif args.command == "watch":
        watch_command.run()
    elif args.command == "parse":
        parse_command.run()
    elif args.command == "doctor":
        doctor_command.run()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
