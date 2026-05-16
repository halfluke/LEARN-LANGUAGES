# LEARN-C

Interactive **C** course in the terminal: **`chapters/*.json`** (**[TUTORIAL_PLATFORM.md](../TUTORIAL_PLATFORM.md)**), **compile & run** with **`cc`** or **`gcc`**, **trimmed stdout** checks.

The UI is **[Textual](https://textual.textualize.io/)** over **Python 3**.

**Location:** **`c/`** in the LEARN-LANGUAGES monorepo.

## Platform

**Linux and macOS** — **`cc`** or **`gcc`** on `PATH`. **Windows (native MSVC): not supported** in v1; use **WSL2** with a Linux toolchain. See **[../README.md](../README.md#platform-support-v1)**.

## Requirements

- **Python 3.10+** (runs the host TUI).
- **`cc`** (preferred) or **`gcc`** on **`PATH`** (POSIX; **native MSVC not supported** in v1 — use Linux, macOS, or **WSL2**).

Optional: **`EDITOR`** (`vim`, `nano`, `code --wait`, …).

**Startup:** probe **`cc --version`** or **`gcc --version`**; failures print to **stderr** and exit **`1`** (no UI).

**Grading:** write **`solution.c`**, **`cc -std=c11 -Wall -Wextra`** (plus **`-lm`** when needed), run under a timeout, compare trimmed stdout to **`expected_output`**.

**Maintainers:** **`python3 scripts/check_solutions.py`** (same **`cc`/`gcc`** toolchain as the TUI).

## Install (editable)

From the **`c/`** directory:

```bash
cd path/to/LEARN-LANGUAGES/c
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Run

```bash
python -m learn_c_tui
# or after install:
learn-c-tui
```

**Progress:** `~/.learn-c-tui/progress.json`

Alternate chapter path:

```bash
export LEARN_C_CHAPTERS=/absolute/path/to/chapters
```

## Keys (summary)

| Context | Keys |
|--------|------|
| Chapter list | **`j`** / **`k`**, **`Enter`**, **`/`** jump, **`?`** help, **`s`** stats, **`q`** quit |
| Theory | **`j`** / **`k`** scroll, **`Enter`** exercises, **`b`** back |
| Exercises | **`j`** / **`k`**, **`Enter`** open, **`b`** back |
| Code | **`r`** compile/run, **`e`** external editor, **`b`** back |
| Result | **`h`** hint on failure, **`r`** re-run, **`b`** back to list |

## Verify solutions

```bash
python3 scripts/check_solutions.py
```

Default **`./.check-c-work`**. Override: **`LEARN_C_CHECK_WORK`**.

## Curriculum

Edit **`chapters/`** in place. Shared outline: **[../CURRICULUM.md](../CURRICULUM.md)** · schema: **[../TUTORIAL_PLATFORM.md](../TUTORIAL_PLATFORM.md)**

## Security

Writes source, compiles natives, executes under timeouts — only use trusted chapter content.

## Tests

```bash
python3 -m pytest tests/ -q
```
