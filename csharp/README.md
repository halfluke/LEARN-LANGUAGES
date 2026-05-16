# LEARN-C#

Interactive **C#** course in the terminal: **`chapters/*.json`** (**[TUTORIAL_PLATFORM.md](../TUTORIAL_PLATFORM.md)**), **`dotnet`** build/run, **trimmed stdout** checks.

The UI is **[Textual](https://textual.textualize.io/)** over **Python 3**.

**Location:** **`csharp/`** in the LEARN-LANGUAGES monorepo (no `#` in the path name — the old **`LEARN-C#`** wording referred to standalone repos).

## Platform

**Linux, macOS, and Windows** — [.NET SDK](https://dotnet.microsoft.com/download) plus **Python 3.10+** for the Textual TUI. See **[../README.md](../README.md#platform-support-v1)**.

## Requirements

### .NET SDK

Exercises run as small **SDK-style console** projects (**`dotnet build`** / **`dotnet run`**). You need the **.NET SDK** (not just the runtime): **`dotnet --version`** must succeed.

Install from **[Download .NET](https://dotnet.microsoft.com/download)** or your package manager. **SDK 6+** matches the template this course uses; **8** or **9** is fine.

**Linux (Debian / Ubuntu / Kali)** — if your distro ships a recent SDK package:

```bash
sudo apt update
sudo apt install dotnet-sdk-8.0
```

If that package is missing or too old, use Microsoft’s install guide for your distro: [Install .NET on Linux](https://learn.microsoft.com/en-us/dotnet/core/install/linux).

**Linux (Fedora):**

```bash
sudo dnf install dotnet-sdk-8.0
```

**macOS:**

```bash
brew install dotnet
```

Or install from [dotnet.microsoft.com/download](https://dotnet.microsoft.com/download).

**Windows:** install the **.NET SDK** from [dotnet.microsoft.com/download](https://dotnet.microsoft.com/download) or `winget install Microsoft.DotNet.SDK.8`.

**Verify:**

```bash
dotnet --version
dotnet --list-sdks
```

**Startup:** the TUI runs **`dotnet --version`** before the UI starts; failure prints to **stderr** and exits **1**.

First exercise run may **restore NuGet packages**; allow a minute on a cold machine.

### Python (TUI host)

- **Python 3.10+** on **`PATH`**.

### External editor (`e`)

Press **`e`** on the **code** screen to edit in **`$EDITOR`**. If unset: **`nano`** → **`micro`** → **`vim`** → **`nvim`** → **`code`** → **`subl`** (first on `PATH`). Example: `export EDITOR=nano`. Details: **[../README.md#course-tui-controls](../README.md#course-tui-controls)**.

Install with **`pip install -e ".[dev]"`** below (or the repo-root **`./scripts/setup-learn.sh`**, which installs this track into the root **`.venv`**).

## How exercises are run (TUI)

When you press **`r`** on an exercise:

1. Your code is written to **`Program.cs`** in a **session SDK console project** (created once per TUI run, reused for later exercises).
2. The app runs **`dotnet build`** (NuGet restore happens on the first build; later builds use **`--no-restore`**).
3. The app runs **`dotnet run --no-build`** on that project — the normal SDK host path learners expect, not a stripped-down shortcut.

Trimmed **stdout** is compared to **`expected_output`**.

## Install (editable)

**Hub (optional):** from the repo root, **`./scripts/setup-learn.sh`**, activate **`.venv`**, then **`learn-languages`** → **C#**. Or install only this track:

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

See **[../README.md#finding-chapters](../README.md#finding-chapters)** for the full resolution order.

## Learner workflow

1. Start the TUI (**Run** above) or open **C#** from **`learn-languages`** (hub setup).
2. Pick a **chapter**, then an **exercise** (read **theory** if you want).
3. Press **`e`** — edit in **`$EDITOR`**, then **save and quit**.
4. Press **`r`** — **`dotnet` build/run** and compare stdout.
5. On failure, press **`h`** for the next hint (up to two per exercise).
6. Repeat until correct; progress saves automatically.

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

| | TUI (learner) | `check_solutions.py` (maintainer) |
|--|----------------|-----------------------------------|
| Projects | One per session (reused) | **`--jobs 2`** → `worker-0/`, `worker-1/` (each reused across many exercises) |
| After build | **`dotnet run --no-build`** | **`dotnet run --no-build`** (same as TUI) |
| Goal | Match real **`dotnet run`** behavior | Bulk-verify all reference solutions (parallel workers) |

Work directory: **`.check-csharp-work`** (override **`LEARN_CSHARP_CHECK_WORK`**). Safe to delete; gitignored.

## Course layout

Chapters live under **`chapters/*.json`** (filename order). Edit JSON in place. Schema: **[../TUTORIAL_PLATFORM.md](../TUTORIAL_PLATFORM.md)**.

**18** chapters, **124** exercises — loaded from **`chapters/*.json`** (filename order).

| # | Chapter | Exercises |
|---|---------|-----------|
| 1 | Variables and types | 7 |
| 2 | References vs values | 3 |
| 3 | Control flow | 7 |
| 4 | Functions | 7 |
| 5 | Sequences and lists | 7 |
| 6 | Spans and arrays | 7 |
| 7 | Dictionaries | 7 |
| 8 | Strings | 7 |
| 9 | Structs and records | 7 |
| 10 | Interfaces | 7 |
| 11 | Methods | 7 |
| 12 | Namespaces and projects | 7 |
| 13 | Unsafe code | 7 |
| 14 | Errors and exceptions | 7 |
| 15 | Async and tasks | 7 |
| 16 | Testing | 5 |
| 17 | JSON | 9 |
| 18 | Date and time | 9 |


## Security

The TUI and checker **write your source to disk**, **compile** with **`dotnet`**, and **execute** the resulting program under timeouts. Treat chapter snippets like any local compile-and-run exercise.

## Tests (dev install)

```bash
python3 -m pytest tests/ -q
```
