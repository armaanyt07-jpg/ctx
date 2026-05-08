# ContextDrop

ContextDrop is a tiny CLI that creates a `.ctx/` folder in any project and keeps a simple project brain there: decisions, tasks, handoff notes, and a reusable prompt for the next AI session.

The simplest way to use it does **not** require installation.

## Quick Start

From the `contextdrop` folder:

```powershell
python ctx.py --help
```

Or on Windows:

```powershell
.\ctx.cmd --help
```

To make `ctx` work from anywhere, run this once:

```powershell
cd "C:\Users\armaa\OneDrive\Desktop\contextdrop"
.\install.ps1
```

Then close and reopen PowerShell:

```powershell
ctx --help
ctx save
```

Use it inside another project by passing the full path to `ctx.py`:

```powershell
cd path\to\your-project
python "C:\Users\armaa\OneDrive\Desktop\contextdrop\ctx.py" init
python "C:\Users\armaa\OneDrive\Desktop\contextdrop\ctx.py" status
```

If you installed the PATH launcher, the same commands become:

```powershell
cd path\to\your-project
ctx init
ctx status
ctx save
```

If you want the shorter `ctx` command later:

```powershell
cd "C:\Users\armaa\OneDrive\Desktop\contextdrop"
python -m pip install -e .
ctx --help
```

## Commands

```powershell
python ctx.py init
python ctx.py save
python ctx.py load
python ctx.py status
python ctx.py add "build the login page"
python ctx.py done 1
python ctx.py parse
python ctx.py watch
python ctx.py report
```

When installed, replace `python ctx.py` with `ctx`.

`save` is automatic by default. It writes `.ctx/handoff.md` from your current task board and brain files without asking questions.

If you want to manually add session notes:

```powershell
python ctx.py save --interactive
```

## What Gets Created

Running `init` inside a project creates:

```text
.ctx/
  brain.md
  tasks.json
  handoff.md
  system_prompt.md
```

Commit `.ctx/brain.md`, `.ctx/tasks.json`, `.ctx/handoff.md`, and `.ctx/system_prompt.md` if you want the project brain to travel with the code. `.ctx/watch.log` is ignored.

## Project Layout

```text
contextdrop/
  ctx.py                  # no-install launcher
  pyproject.toml          # optional install metadata
  README.md
  contextdrop/
    cli.py                # small argparse command router
    constants.py
    config.py
    commands/             # command behavior
    services/             # clipboard, filesystem, parsing helpers
    core/                 # prompt/report builders
    utils/                # logging and formatting
  tests/
```

## For Developers

Compile-check the package:

```powershell
python -m compileall contextdrop
```

Run without installing:

```powershell
python -m contextdrop --help
```

Install only when you want a global/local `ctx` command:

```powershell
python -m pip install -e .
```
