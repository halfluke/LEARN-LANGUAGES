# LEARN-C#

Interactive **C#** course in the terminal: **`chapters/*.json`** (**[TUTORIAL_PLATFORM.md](../TUTORIAL_PLATFORM.md)**), **`dotnet`** build/run, **trimmed stdout** checks.

The UI is **[Textual](https://textual.textualize.io/)** over **Python 3**.

**Location:** **`csharp/`** in the LEARN-LANGUAGES monorepo (no `#` in the path name — the old **`LEARN-C#`** wording referred to standalone repos).

## Requirements

- **Python 3.10+** (TUI driver).
- **.NET SDK** — **`dotnet --version`** must succeed.

Optional: **`EDITOR`** for **`e`** in the exercise editor.

**Startup:** **`dotnet --version`**; failures print to stderr and exit **1**.

**Grading:** your snippet becomes **`Program.cs`** in an SDK-style console project; the TUI uses **`dotnet build`** then **`dotnet run --no-build`** on that project (first run may restore NuGet packages). Trimmed stdout must match **`expected_output`**.

**Maintainers:** **`python3 scripts/check_solutions.py`** needs **Python 3.10+** and the same **.NET SDK**; it reuses one project under **`.check-csharp-work`** (override with **`LEARN_CSHARP_CHECK_WORK`**).

## Install (editable)

```bash
cd path/to/LEARN-LANGUAGES/csharp
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Run

```bash
python -m learn_cs_tui
# or after install:
learn-csharp-tui
```

**Progress:** `~/.learn-csharp-tui/progress.json`

```bash
export LEARN_CSHARP_CHAPTERS=/absolute/path/to/chapters
```

## Keys (summary)

| Context | Keys |
|--------|------|
| Chapter list | **`j`** / **`k`**, **`Enter`**, **`/`** jump, **`?`** help, **`s`** stats, **`q`** quit |
| Theory | **`j`** / **`k`** scroll, **`Enter`** exercises, **`b`** back |
| Exercises | **`j`** / **`k`**, **`Enter`** open, **`b`** back |
| Code | **`r`** run **`dotnet`**, **`e`** **`$EDITOR`**, **`b`** back |
| Result | **`h`** hint · **`r`** re-run · **`b`** back |

## Verify solutions

```bash
python3 scripts/check_solutions.py
```

Default **`./.check-csharp-work`** (one reused SDK project: **`dotnet build`** then **`dotnet run --no-build`** per solution). Override: **`LEARN_CSHARP_CHECK_WORK`**.

Edit chapter JSON under **`chapters/`** in place. Shared outline: **[../CURRICULUM.md](../CURRICULUM.md)** · schema: **[../TUTORIAL_PLATFORM.md](../TUTORIAL_PLATFORM.md)**

## Security

Creates a temp **`dotnet`** project and runs **`dotnet run`** locally with timeouts — treat chapter snippets like compiling any untrusted code.

## Tests

```bash
python3 -m pytest tests/ -q
```
