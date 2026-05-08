$ErrorActionPreference = "Stop"

python -m compileall contextdrop
python -m unittest discover -s tests
python ctx.py --help | Out-Null
python ctx.py --version | Out-Null

Write-Host "[ok] ContextDrop checks passed."
