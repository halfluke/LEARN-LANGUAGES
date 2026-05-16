# LEARN-C

Interactive **C** course in the terminal: **`chapters/*.json`** (**[TUTORIAL_PLATFORM.md](../TUTORIAL_PLATFORM.md)**), **compile & run** with **`cc`** or **`gcc`**, **trimmed stdout** checks.

The UI is **[Textual](https://textual.textualize.io/)** over **Python 3**.

**Location:** **`c/`** in the LEARN-LANGUAGES monorepo.

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

Optional: **`EDITOR`** (`vim`, `nano`, `code --wait`, …) for **`e`** in the exercise screen.

Install the Textual app with **`pip install -e ".[dev]"`** below (or use the repo-root **`./scripts/setup-learn.sh`**, which installs this track into the root **`.venv`**).

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
