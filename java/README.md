# LEARN-Java

Interactive **Java 17** course in the terminal: **`chapters/*.json`** (**[TUTORIAL_PLATFORM.md](../TUTORIAL_PLATFORM.md)**), **`javac`** + **`java`**, **trimmed stdout** checks.

The UI is **[Textual](https://textual.textualize.io/)** over **Python 3**; learner code is plain Java (`public class Main` …).

**Location:** **`java/`** in the **LEARN-LANGUAGES** monorepo.

## Platform

**Linux, macOS, and Windows** — **JDK 17+** (`javac`, `java`) and **Python 3.10+** for the TUI. See **[../README.md](../README.md#platform-support-v1)**.

## Requirements

### JDK 17+

**`javac`** and **`java`** must be on **`PATH`**.

Install from [Adoptium](https://adoptium.net/), your package manager, or [Oracle / OpenJDK](https://openjdk.org/) builds.

**Verify:**

```bash
javac -version
java -version
```

**Startup:** **`java -version`** before the UI loads; failure prints to **stderr** and exits **non-zero**.

**Grading:** writes **`*.java`** named after the **`public class`**, runs **`javac`** then **`java`** with that class name; trimmed **stdout** must match **`expected_output`**.

### Python (TUI host)

- **Python 3.10+** on **`PATH`** — installed with **`pip install -e ".[dev]"`** below.

### External editor (`e`)

Press **`e`** on the **code** screen. Set **`EDITOR`** before starting (e.g. `export EDITOR=nano`). If unset: **`nano`** → **`micro`** → **`vim`** → **`nvim`** → **`code`** → **`subl`**. Details: **[../README.md#course-tui-controls](../README.md#course-tui-controls)**.

### Optional: maintainers

**`python3 scripts/check_solutions.py`** needs **Python 3.10+** and the same **JDK** as the TUI.

## Install (editable)

**Hub (optional):** from the repo root, **`./scripts/setup-learn.sh`**, activate **`.venv`**, then **`learn-languages`** → **Java**. Or install only this track:

```bash
cd path/to/LEARN-LANGUAGES/java
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Run

```bash
python -m learn_java_tui
# or after install:
learn-java-tui
```

**Progress:** `~/.learn-java-tui/progress.json`

If **`chapters/`** is not beside the package:

```bash
export LEARN_JAVA_CHAPTERS=/absolute/path/to/chapters
```

See **[../README.md#finding-chapters](../README.md#finding-chapters)** for the full resolution order.

## Learner workflow

1. Start the TUI (**Run** above) or open **Java** from **`learn-languages`** (hub setup).
2. Pick a **chapter**, then an **exercise** (read **theory** if you want).
3. Press **`e`** — edit in **`$EDITOR`**, then **save and quit**.
4. Press **`r`** — compile/run and compare stdout.
5. On failure, press **`h`** for the next hint (up to two per exercise).
6. Repeat until correct; progress saves automatically.

## Keys (summary)

| Context | Keys |
|--------|------|
| Chapter list | **`j`** / **`k`**, **Enter**, **`/`** jump, **`?`** help, **`s`** stats, **`q`** quit |
| Theory | **`j`** / **`k`** scroll, **Enter** exercises, **`b`** back |
| Exercises | **`j`** / **`k`**, **Enter** open, **`b`** back |
| Code | **`r`** compile/run, **`e`** **`$EDITOR`**, **`b`** back |
| Result | **`h`** hint on failure, **`r`** re-run, **`b`** back |

## Course layout

Chapters live under **`chapters/*.json`** (filename order). Edit JSON in place. Schema: **[../TUTORIAL_PLATFORM.md](../TUTORIAL_PLATFORM.md)**.

**18** chapters, **124** exercises — loaded from **`chapters/*.json`** (filename order).

| # | Chapter | Exercises |
|---|---------|-----------|
| 1 | Variables and types | 7 |
| 2 | Values, references, and mutation | 3 |
| 3 | Control flow | 7 |
| 4 | Functions | 7 |
| 5 | Sequences and lists | 7 |
| 6 | Arrays and lists | 7 |
| 7 | Maps | 7 |
| 8 | Strings | 7 |
| 9 | Classes and records | 7 |
| 10 | Interfaces | 7 |
| 11 | Methods | 7 |
| 12 | Packages | 7 |
| 13 | References | 7 |
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

Default work dir: **`.check-java-work`**. Override: **`LEARN_JAVA_CHECK_WORK`**.

## Security

Writes source, compiles, and runs bytecode locally with **timeouts**; trust chapter snippets like any local compile-and-run educator.

## Tests (dev install)

```bash
python3 -m pytest tests/ -q
```
