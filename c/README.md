# LEARN-C

Interactive **C** course in the terminal: **`chapters/*.json`** (**[TUTORIAL_PLATFORM.md](../TUTORIAL_PLATFORM.md)**), **compile & run** with **`cc`** or **`gcc`**, **trimmed stdout** checks.

The UI is **[Textual](https://textual.textualize.io/)** over **Python 3**.

**Location:** **`c/`** in the **LEARN-LANGUAGES** monorepo.

## Platform

**Linux and macOS** — **`cc`** or **`gcc`** on `PATH`. **Windows (native MSVC): not supported** in v1; use **WSL2** with a Linux toolchain. See **[../README.md](../README.md#platform-support-v1)**.

## Requirements

### C compiler (`cc` or `gcc`)

Exercises are compiled with **`cc`** (if present) or **`gcc`**, C11, **`-Wall -Wextra`**, and **`-lm`** when the math library is needed. **Native Windows MSVC is not supported** in v1 — use **Linux**, **macOS**, or **WSL2**.

**Linux (Debian / Ubuntu / Kali and derivatives):**

```bash
sudo apt update
sudo apt install build-essential
```

`build-essential` pulls in **gcc**, **g++**, and usually a **`cc`** symlink. On minimal images you can install **`gcc`** alone.

**Linux (Fedora / RHEL-style):**

```bash
sudo dnf install gcc
```

**macOS:** install Apple’s command-line tools (provides **`clang`** as **`cc`**):

```bash
xcode-select --install
```

Or install GCC via [Homebrew](https://brew.sh/): `brew install gcc` (you may need to set **`CC=gcc-14`** or similar if **`cc`** still points at clang — either compiler is fine for this course).

**Windows:** use **WSL2** and the **Linux** packages above inside your Linux distro.

**Verify** (at least one should print a version):

```bash
cc --version
gcc --version
```

**Startup:** the TUI runs the same check; if both fail, it prints to **stderr** and exits **1** (no UI).

### Python (TUI host)

- **Python 3.10+** on **`PATH`** as **`python3`** (or **`python`**).

### External editor (`e`)

Press **`e`** on the **code** screen to edit in **`$EDITOR`**. If unset: **`nano`** → **`micro`** → **`vim`** → **`nvim`** → **`code`** → **`subl`** (first on `PATH`). Example: `export EDITOR=nano` or `export EDITOR="code --wait"`. Details: **[../README.md#course-tui-controls](../README.md#course-tui-controls)**.

Install the Textual app with **`pip install -e ".[dev]"`** below (or use the repo-root **`./scripts/setup-learn.sh`**, which installs this track into the root **`.venv`**).

**Grading:** write **`solution.c`**, **`cc -std=c11 -Wall -Wextra`** (plus **`-lm`** when needed), run under a timeout, compare trimmed stdout to **`expected_output`**.

**Maintainers:** **`python3 scripts/check_solutions.py`** (same **`cc`/`gcc`** toolchain as the TUI).

## Install (editable)

**Hub (optional):** from the repo root, **`./scripts/setup-learn.sh`**, activate **`.venv`**, then **`learn-languages`** → **C**. Or install only this track:

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

See **[../README.md#finding-chapters](../README.md#finding-chapters)** for the full resolution order.

## Learner workflow

1. Start the TUI (**Run** above) or open **C** from **`learn-languages`** (hub setup).
2. Pick a **chapter**, then an **exercise** (read **theory** if you want).
3. Press **`e`** — edit in **`$EDITOR`**, then **save and quit**.
4. Press **`r`** — compile/run and compare stdout.
5. On failure, press **`h`** for the next hint (up to two per exercise).
6. Repeat until correct; progress saves automatically.

## Keys (summary)

| Context | Keys |
|--------|------|
| Chapter list | **`j`** / **`k`**, **`Enter`**, **`/`** jump, **`?`** help, **`s`** stats, **`q`** quit |
| Theory | **`j`** / **`k`** scroll, **`Enter`** exercises, **`b`** back |
| Exercises | **`j`** / **`k`**, **`Enter`** open, **`b`** back |
| Code | **`r`** compile/run, **`e`** external editor, **`b`** back |
| Result | **`h`** hint on failure, **`r`** re-run, **`b`** back to list |

## Course layout

Chapters live under **`chapters/*.json`** (filename order). Edit JSON in place. Schema: **[../TUTORIAL_PLATFORM.md](../TUTORIAL_PLATFORM.md)**.

**17** chapters, **117** exercises — loaded from **`chapters/*.json`** (filename order).

| # | Chapter | Exercises |
|---|---------|-----------|
| 1 | Variables and types | 7 |
| 2 | Aliasing and memory | 3 |
| 3 | Control flow | 7 |
| 4 | Functions | 7 |
| 5 | Arrays | 7 |
| 6 | Pointers and array views | 7 |
| 7 | Associative data | 7 |
| 8 | Strings | 7 |
| 9 | Structs | 7 |
| 10 | Polymorphism in C | 7 |
| 11 | Methods as functions | 7 |
| 12 | Pointers | 7 |
| 13 | Error handling | 7 |
| 14 | Concurrency | 7 |
| 15 | Testing | 5 |
| 16 | JSON | 9 |
| 17 | Time | 9 |


## Maintainer: verify bundled solutions

```bash
python3 scripts/check_solutions.py
python3 scripts/check_solutions.py --chapter variables
python3 scripts/check_solutions.py --list-failures-only
```

Default work dir: **`.check-c-work`**. Override: **`LEARN_C_CHECK_WORK`**.

## Security

Writes source, compiles natives, and runs them locally with **timeouts** — only use trusted chapter content.

## Tests (dev install)

```bash
python3 -m pytest tests/ -q
```
