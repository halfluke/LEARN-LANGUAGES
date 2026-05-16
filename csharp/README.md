# LEARN-C#

Interactive **C#** course in the terminal: **`chapters/*.json`** (**[TUTORIAL_PLATFORM.md](../TUTORIAL_PLATFORM.md)**), **`dotnet`** build/run, **trimmed stdout** checks.

The UI is **[Textual](https://textual.textualize.io/)** over **Python 3**.

**Location:** **`csharp/`** in the LEARN-LANGUAGES monorepo (no `#` in the path name — the old **`LEARN-C#`** wording referred to standalone repos).

## Platform

**Linux, macOS, and Windows** — [.NET SDK](https://dotnet.microsoft.com/download) plus **Python 3.10+** for the Textual TUI. See **[../README.md](../README.md#platform-support-v1)**.

## Requirements

- **Python 3.10+** (TUI driver).
- **.NET SDK** — **`dotnet --version`** must succeed.

Optional: **`EDITOR`** for **`e`** in the exercise editor.

**Startup:** **`dotnet --version`**; failures print to stderr and exit **1**.

## How exercises are run (TUI)

When you press **`r`** on an exercise:

1. Your code is written to **`Program.cs`** in a **session SDK console project** (created once per TUI run, reused for later exercises).
2. The app runs **`dotnet build`** (NuGet restore happens on the first build; later builds use **`--no-restore`**).
3. The app runs **`dotnet run --no-build`** on that project — the normal SDK host path learners expect, not a stripped-down shortcut.

Trimmed **stdout** is compared to **`expected_output`**.

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

## Maintainer: verify bundled solutions

Requires **Python 3.10+** and the same **.NET SDK** as the TUI.

```bash
python3 scripts/check_solutions.py
python3 scripts/check_solutions.py --chapter methods
python3 scripts/check_solutions.py --jobs 1
python3 scripts/check_solutions.py --list-failures-only
```

The checker is **faster** than the TUI path on purpose; it is not identical subprocess wiring:

| | TUI (learner) | `check_solutions.py` (maintainer) |
|--|----------------|-----------------------------------|
| Projects | One per session | **`--jobs 2`** by default → `worker-0/`, `worker-1/` under the work dir |
| After build | **`dotnet run --no-build`** | **`dotnet exec`** on the built DLL |
| Goal | Match real **`dotnet run`** behavior | Bulk-verify all reference solutions quickly |

Work directory: **`./.check-csharp-work`** (override **`LEARN_CSHARP_CHECK_WORK`**). Safe to delete; it is gitignored.

Edit chapter JSON under **`chapters/`** in place. Shared outline: **[../CURRICULUM.md](../CURRICULUM.md)** · schema: **[../TUTORIAL_PLATFORM.md](../TUTORIAL_PLATFORM.md)**

## Security

The TUI and checker **write your source to disk**, **compile** with **`dotnet`**, and **execute** the resulting program under timeouts. Treat chapter snippets like any local compile-and-run exercise.

## Tests

```bash
python3 -m pytest tests/ -q
```
