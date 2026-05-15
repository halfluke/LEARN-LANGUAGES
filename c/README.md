# LEARN-C

Interactive **C** course in the terminal: JSON chapters (same schema as other LEARN-* courses / `LEARN-LANGUAGES/TUTORIAL_PLATFORM.md`), **compile and run** with **`cc`** or **`gcc`**, and **trimmed stdout** checks.

This repo uses a **Python** [Textual](https://textual.textualize.io/) TUI.

## Requirements

- **Python 3.10+**
- A **POSIX C compiler** on your **`PATH`**: **`cc`** (preferred) or **`gcc`**. Native **MSVC** is **not** supported in v1; use **WSL2**, **Linux**, **macOS**, or another environment where `cc`/`gcc` works.

**Startup check:** Before the Textual UI starts, the entrypoint runs **`cc --version`** or **`gcc --version`** (whichever is resolved first). If no compiler is found or the command fails, it prints an explanation to **stderr** and exits with code **1** (the TUI never starts).

**How exercises are checked:** The TUI does **not** only inspect your source. It writes **`solution.c`**, runs **`cc -std=c11 -Wall -Wextra -o …`** (and **`-lm`** when the snippet likely needs **libm**), then runs the binary with a **timeout**, and compares **trimmed stdout** to **`expected_output`**.

Optional: set **`EDITOR`** (otherwise the TUI tries `vim`, `nano`, etc. on `PATH`).

## Install (editable, from repo root)

```bash
cd /path/to/LEARN-C
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Run

```bash
python -m learn_c_tui
# or
learn-c-tui
```

Progress is stored under **`~/.learn-c-tui/progress.json`**.

If chapter JSON is not next to the package, set:

```bash
export LEARN_C_CHAPTERS=/absolute/path/to/chapters
```

## Keys (summary)

| Context | Keys |
|--------|------|
| Chapter list | `j` / `k`, `Enter`, `/` jump, `?` help, `s` stats, `q` quit |
| Theory | `j` / `k` scroll, `Enter` exercises, `b` back |
| Exercises | `j` / `k`, `Enter` open, `b` back |
| Code | `r` compile/run, `e` external editor, `b` back |
| Result | `h` hint (on failure), `r` re-run, `b` back to list |

## Verify solutions (CI / maintainers)

```bash
python3 scripts/check_solutions.py
```

By default the script reuses **`./.check-c-work`**. Override with **`LEARN_C_CHECK_WORK`**.

## Security

The TUI writes your code to disk, **compiles** it to a native binary, and **runs** it locally with **timeouts**. Use only with chapter content you trust. There is no extra sandbox beyond your normal user account.

## Tests

```bash
pytest -q
```
