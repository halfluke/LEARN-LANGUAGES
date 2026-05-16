# LEARN-Python

Interactive **Python 3** course in the terminal: **`chapters/*.json`** (**[TUTORIAL_PLATFORM.md](../TUTORIAL_PLATFORM.md)**), **`python3`** execution, **trimmed stdout** checks.

The UI is **[Textual](https://textual.textualize.io/)** over **Python 3**.

**Location:** **`python/`** in the **LEARN-LANGUAGES** monorepo.

## Platform

**Linux, macOS, and Windows** — **Python 3.10+** on `PATH`. See **[../README.md](../README.md#platform-support-v1)**.

## Requirements

| Requirement | Notes |
|-------------|--------|
| **Python 3.10+** | On `PATH` as **`python3`** or **`python`** (TUI and checker prefer **`python3`**) |
| **Textual** | Installed by **`pip install -e ".[dev]"`** below |

**Startup:** **`python3 --version`** (or **`python`**) before the UI starts; failure prints to **stderr** and exits **non-zero**.

**Grading:** writes **`solution.py`**, runs **`python3 solution.py`** with a timeout, compares trimmed **stdout** to **`expected_output`**.

### External editor (`e`)

Press **`e`** on the **code** screen. Set **`EDITOR`** before starting (e.g. `export EDITOR=nano`). If unset: **`nano`** → **`micro`** → **`vim`** → **`nvim`** → **`code`** → **`subl`**. Details: **[../README.md#course-tui-controls](../README.md#course-tui-controls)**.

### Optional: maintainers

**`python3 scripts/check_solutions.py`** uses the same interpreter (no extra compiler).

## Install (editable)

**Hub (optional):** from the repo root, **`./scripts/setup-learn.sh`**, activate **`.venv`**, then **`learn-languages`** → **Python**. Or install only this track:

```bash
cd path/to/LEARN-LANGUAGES/python
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Run

```bash
python -m learn_python_tui
# or after install:
learn-python-tui
```

**Progress:** `~/.learn-python-tui/progress.json`

If **`chapters/`** is not beside the installed package:

```bash
export LEARN_PYTHON_CHAPTERS=/absolute/path/to/chapters
```

If unset, the TUI finds **`chapters/`** next to the package or cwd — see **[../README.md#finding-chapters](../README.md#finding-chapters)**.

## Learner workflow

1. Start the TUI (**Run** above) or open **Python** from **`learn-languages`** (hub setup).
2. Pick a **chapter**, then an **exercise** (read **theory** if you want).
3. Press **`e`** — edit in **`$EDITOR`**, then **save and quit**.
4. Press **`r`** — run and compare stdout.
5. On failure, press **`h`** for the next hint (up to two per exercise).
6. Repeat until correct; progress saves automatically.

## Keys (summary)

| Context | Keys |
|--------|------|
| Chapter list | **`j`** / **`k`**, **Enter**, **`/`** jump, **`?`** help, **`s`** stats, **`q`** quit |
| Theory | **`j`** / **`k`** scroll, **Enter** exercises, **`b`** back |
| Exercises | **`j`** / **`k`**, **Enter** open, **`b`** back |
| Code | **`r`** run, **`e`** **`$EDITOR`**, **`b`** back |
| Result | **`h`** hint on failure, **`r`** re-run, **`b`** back |

## Course layout

Chapters live under **`chapters/*.json`** (filename order). Edit JSON in place. Schema: **[../TUTORIAL_PLATFORM.md](../TUTORIAL_PLATFORM.md)**.

**18** chapters, **124** exercises — loaded from **`chapters/*.json`** (filename order).

| # | Chapter | Exercises |
|---|---------|-----------|
| 1 | Variables and types | 7 |
| 2 | Values, copies, and references | 3 |
| 3 | Control flow | 7 |
| 4 | Functions | 7 |
| 5 | Sequences and lists | 7 |
| 6 | Lists and slices | 7 |
| 7 | Dictionaries | 7 |
| 8 | Strings | 7 |
| 9 | Classes and data objects | 7 |
| 10 | Protocols and duck typing | 7 |
| 11 | Methods | 7 |
| 12 | Modules and packages | 7 |
| 13 | References and identity | 7 |
| 14 | Errors and exceptions | 7 |
| 15 | Concurrency | 7 |
| 16 | Testing | 5 |
| 17 | JSON | 9 |
| 18 | Date and time | 9 |


## Maintainer: verify bundled solutions

```bash
python3 scripts/check_solutions.py
python3 scripts/check_solutions.py --chapter variables
python3 scripts/check_solutions.py --list-failures-only
```

Default work dir: **`.check-python-work`**. Override: **`LEARN_PYTHON_CHECK_WORK`**.

## Security

Runs **your** code locally with **timeouts**; trust chapter content like any execute-snippet educator.

## Tests (dev install)

```bash
python3 -m pytest tests/ -q
```
