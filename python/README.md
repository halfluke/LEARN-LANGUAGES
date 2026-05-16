# LEARN-Python

Interactive **Python 3** course in the terminal: **`chapters/*.json`** shared with other LEARN-* tracks (**[TUTORIAL_PLATFORM.md](../TUTORIAL_PLATFORM.md)**), **`python3`** execution, **trimmed stdout** checks.

Located under **`python/`** in the **LEARN-LANGUAGES** monorepo (`cd` here after cloning).

## Requirements

| Requirement | Notes |
|-------------|--------|
| **Python 3.10+** | On `PATH` as `python3` or `python` (the TUI and checker prefer **`python3`**) |
| **Textual** | Pulled in by `pip install -e ".[dev]"` below |

Optional: **`EDITOR`** (otherwise the TUI tries `vim`, `nano`, … on `PATH`) for **`e`** in the code screen.

## Install (editable)

```bash
cd /path/to/LEARN-LANGUAGES/python
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Run

```bash
python -m learn_python_tui
# or (after editable install):
learn-python-tui
```

**Progress:** `~/.learn-python-tui/progress.json`

If `chapters/` is not beside the installed package:

```bash
export LEARN_PYTHON_CHAPTERS=/absolute/path/to/chapters
```

**Startup:** the entrypoint verifies **`python3 --version`** (or resolves **`python`**) before the UI starts.

**How grading works:** the app writes **`solution.py`**, runs **`python3 solution.py`** with a timeout, and compares trimmed **stdout** to **`expected_output`**.

**Maintainers:** **`python3 scripts/check_solutions.py`** uses the same interpreter (no extra compiler).

## Keys (short)

| Screen | Actions |
|--------|---------|
| List | **`j`** / **`k`**, **`Enter`**, **`/`** jump, **`?`** help, **`s`** stats, **`q`** quit |
| Theory | **`j`** / **`k`** scroll · **`Enter`** exercises · **`b`** back |
| Exercises | **`j`** / **`k`** · **`Enter`** open · **`b`** back |
| Code | **`r`** run · **`e`** `$EDITOR` · **`b`** back |
| Result | **`h`** hints on failure · **`r`** rerun · **`b`** back |

## Maintainer: verify bundled solutions

```bash
python3 scripts/check_solutions.py
python3 scripts/check_solutions.py --chapter variables
python3 scripts/check_solutions.py --list-failures-only
```

Default work dir: **`.check-python-work`**. Override: **`LEARN_PYTHON_CHECK_WORK`**.

Edit chapter JSON under **`chapters/`** in place. Shared outline: **[../CURRICULUM.md](../CURRICULUM.md)** · schema: **[../TUTORIAL_PLATFORM.md](../TUTORIAL_PLATFORM.md)**

## Tests (dev install)

```bash
python3 -m pytest tests/ -q
```

## Security

Runs **your** code locally with timeouts; trust chapter content like any tool that executes snippets on your machine.
