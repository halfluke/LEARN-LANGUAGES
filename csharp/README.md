# LEARN-C#

Interactive **C#** course in the terminal: JSON chapters (same schema as other LEARN-* courses / `LEARN-LANGUAGES/TUTORIAL_PLATFORM.md`), **`dotnet`** build/run, and **trimmed stdout** checks.

This repo uses a **Python** [Textual](https://textual.textualize.io/) TUI (aligned with using Python for host tooling across LEARN-* apps).

## Requirements

- **Python 3.10+**
- **.NET SDK** (`dotnet --version` must succeed)

**Startup check:** Before the Textual UI starts, the entrypoint runs **`dotnet --version`**. If the SDK is missing or the command fails, it prints an explanation to **stderr** and exits with code **1** (the TUI never starts).

Optional: set **`EDITOR`** (otherwise the TUI tries `vim`, `nano`, etc. on `PATH`).

## Install (editable, from repo root)

Path contains `#`; quote the directory in the shell.

```bash
cd "/path/to/LEARN-C#"
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Run

```bash
python -m learn_cs_tui
# or
learn-csharp-tui
```

Progress is stored under **`~/.learn-csharp-tui/progress.json`**.

If chapter JSON is not next to the package (e.g. non-editable install), set:

```bash
export LEARN_CSHARP_CHAPTERS=/absolute/path/to/chapters
```

## Keys (summary)

| Context | Keys |
|--------|------|
| Chapter list | `j` / `k`, `Enter`, `/` jump, `?` help, `s` stats, `q` quit |
| Theory | `j` / `k` scroll, `Enter` exercises, `b` back |
| Exercises | `j` / `k`, `Enter` open, `b` back |
| Code | `r` run, `e` external editor, `b` back |
| Result | `h` hint (on failure), `r` re-run, `b` back to list |

## Verify solutions (CI / maintainers)

```bash
python3 scripts/check_solutions.py
```

By default the script reuses **`./.check-csharp-work`**. Override with **`LEARN_CSHARP_CHECK_WORK`** if you want a different directory.

## Security

The TUI writes your code to a **temporary .NET project** and runs **`dotnet run`**. Use only on machines where you trust the chapter content (same model as other LEARN-* courses). Builds are subject to a **timeout**; there is no network sandbox beyond your normal user environment.

## Tests

```bash
pytest -q
```
