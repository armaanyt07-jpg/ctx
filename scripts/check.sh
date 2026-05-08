#!/usr/bin/env sh
set -eu

python -m compileall contextdrop
python -m unittest discover -s tests
python ctx.py --help >/dev/null
python ctx.py --version >/dev/null

echo "[ok] ContextDrop checks passed."
