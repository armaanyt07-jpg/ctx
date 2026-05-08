"""Console formatting helpers kept compatible with the prototype output."""

import sys

G = "\033[32m"
Y = "\033[33m"
C = "\033[36m"
R = "\033[31m"
B = "\033[1m"
D = "\033[2m"
X = "\033[0m"


def ok(msg: str) -> None:
    print(f"{G}[ok]{X} {msg}")


def warn(msg: str) -> None:
    print(f"{Y}!{X} {msg}")


def err(msg: str) -> None:
    print(f"{R}[x]{X} {msg}")
    raise SystemExit(1)


def head(msg: str) -> None:
    print(f"\n{B}{C}{msg}{X}\n")
