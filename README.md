# ContextDrop

**Your project's brain. Never explain your codebase to an agent again.**

When a free-tier AI agent hits its token limit, all context dies. ContextDrop fixes that by keeping a living `.ctx/` folder in your project — stack decisions, task board, file tree, last session summary — and generating a ready-to-paste handoff prompt for the next agent.

---

## Install

```bash
git clone <this repo>
cd contextdrop
bash install.sh
```

Or just drop the `ctx` file anywhere and run it with `python3 ctx`.
KO
Requires: **Python 3.6+** (no dependencies, no pip install)

---

## Usage

### 1. Initialize a project

```bash
cd my-project
ctx init
```

This creates `.ctx/` with:
- `brain.md` — stack, decisions, file tree, conventions
- `tasks.json` — todo / in-progress / done / blocked
- `handoff.md` — last session summary
- `system_prompt.md` — paste this into every agent session

Auto-detects your stack (Node, Python, Go, Rust) from project files.

---

### 2. Paste the system prompt into your agent

Open `.ctx/system_prompt.md` and paste it at the **start** of every new agent conversation. This tells the agent to:
- Read the brain files before writing code
- Append a `CTX-UPDATE` block after every meaningful response

This means context saves **automatically on every reply** — not just when you remember to.

---

### 3. Save a session manually

```bash
ctx save
```

Asks you 4 quick questions:
- What was completed?
- Any decisions made?
- Any blockers?
- What should the next agent do first?

Updates `tasks.json` and writes a clean `handoff.md`.

---

### 4. Load context for a new agent

```bash
ctx load
```

Prints (and copies to clipboard) a compressed handoff prompt — all brain info under ~500 tokens. Paste it into your new agent window.

**That's it. The new agent knows everything.**

---

### 5. Manage tasks

```bash
ctx add "build the login page"        # add a todo
ctx done 1                            # mark todo #1 done
ctx done "login"                      # fuzzy match
ctx status                            # show full task board
```

---

### 6. Auto-parse agent CTX-UPDATE blocks

When your agent appends `CTX-UPDATE` blocks (because you used the system prompt), pipe the output through:

```bash
cat agent_output.txt | ctx parse
```

Or if you're using a wrapper/script that captures output:

```bash
my_agent_runner | ctx parse
```

This automatically:
- Marks tasks done
- Adds next tasks to todo
- Appends decisions to `brain.md`

---

### 7. Watch files (passive auto-track)

```bash
ctx watch
```

Runs in the background. Detects every file create/modify/delete and logs it to `.ctx/watch.log` and `tasks.json`. Gives you a full audit trail of what was built, even if the agent never ran `ctx save`.

Run it in a separate terminal while your agent session is active.

---

## The CTX-UPDATE format

When you use the system prompt, your agent will end responses like this:

```
---CTX-UPDATE---
done: Built Express routes for /todos CRUD
decision: Using raw SQL instead of ORM for simplicity
next: Build React frontend, connect to API on port 3000
bug: none
---END-CTX-UPDATE---
```

`ctx parse` reads these and updates the brain automatically.

---

## File structure

```
your-project/
  .ctx/
    brain.md          ← stack, decisions, file tree, conventions
    tasks.json        ← todo / in-progress / done / blocked
    handoff.md        ← last session summary + next task
    system_prompt.md  ← paste into every agent
    watch.log         ← file change audit trail (gitignored)
```

Commit `.ctx/` to git (except `watch.log`). Your project brain travels with the code.

---

## Example workflow

```bash
# Day 1 — start project
cd my-todo-app
ctx init
# paste .ctx/system_prompt.md into Claude
# ... build auth + DB with agent ...
ctx save
# → "built Express server + JWT auth, next: React frontend"

# Day 2 — new agent, fresh window
ctx load
# → copies handoff prompt to clipboard
# paste into new Claude window
# agent immediately knows the full project state
# ... build React frontend ...
ctx save

# Any time — check progress
ctx status
```

---

## Why not Graphify?

Graphify stores project structure as a graph you have to manually maintain. ContextDrop is:
- **Auto-updating** — via CTX-UPDATE blocks in every agent reply
- **Token-compressed** — `ctx load` outputs <500 tokens
- **Tool-agnostic** — works with Claude, Cursor, GPT-4, anything
- **Zero dependencies** — one Python file, runs anywhere
- **Git-native** — brain lives in your repo, versioned with your code
