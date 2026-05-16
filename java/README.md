# LEARN-Java

Interactive **Java 17** course in the terminal: **`chapters/*.json`** shared with other LEARN-* tracks (**[TUTORIAL_PLATFORM.md](../../TUTORIAL_PLATFORM.md)**), **`javac` + java** execution, **trimmed stdout** checks.

The UI is Python + **Textual**; the learner code is plain Java (`public class Main` …).

Located under **`java/`** in the **LEARN-LANGUAGES** monorepo (`cd` here after cloning).

## Requirements

| Requirement | Notes |
|-------------|--------|
| **JDK 17+** | **`javac`** and **`java`** on **`PATH`** |
| **Python 3.10+** | For the TUI host (`pip install -e …` below) |

Optional: **`EDITOR`** for external editing (**`e`**) when solving exercises.

## Install (editable)

```bash
cd /path/to/LEARN-LANGUAGES/java
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Run

```bash
python -m learn_java_tui
# or (after editable install):
learn-java-tui
```

**Progress:** `~/.learn-java-tui/progress.json`

If `chapters/` is not beside the package:

```bash
export LEARN_JAVA_CHAPTERS=/absolute/path/to/chapters
```

**Startup:** validates **`java -version`** (or equivalent) before the UI loads.

**How grading works:** writes your snippet as **`*.java`** (named after the **`public class`**); runs **`javac`** then **`java`** with that class name; trimmed stdout must match **`expected_output`**.

## Keys (short)

| Screen | Actions |
|--------|---------|
| List | **`j`** / **`k`**, **`Enter`**, **`/`** jump, **`?`** help, **`s`** stats, **`q`** quit |
| Theory | **`j`** / **`k`** · **`Enter`** exercises · **`b`** back |
| Exercises | **`j`** / **`k`** · **`Enter`** open · **`b`** back |
| Code | **`r`** compile/run · **`e`** **`$EDITOR`** · **`b`** back |
| Result | **`h`** hints · **`r`** rerun · **`b`** back |

## Maintainer: verify bundled solutions

```bash
python3 scripts/check_solutions.py
python3 scripts/check_solutions.py --chapter variables
python3 scripts/check_solutions.py --list-failures-only
```

Default work dir: **`.check-java-work`**. Override: **`LEARN_JAVA_CHECK_WORK`**.

Edit chapter JSON under **`chapters/`** in place. Shared outline: **[../CURRICULUM.md](../CURRICULUM.md)** · schema: **[../TUTORIAL_PLATFORM.md](../TUTORIAL_PLATFORM.md)**

## Tests (dev install)

```bash
python3 -m pytest tests/ -q
```

## Security

Writes source, compiles, and runs bytecode locally with timeouts; trust chapter snippets like any local compile-and-run educator.
