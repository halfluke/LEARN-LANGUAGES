# LEARN-LANGUAGES

![LEARN-LANGUAGES main menu — pick a language, then open that track’s course TUI](docs/assets/tui-screenshot.svg)

> **Testing status:** Chapter reference solutions have been checked with each track’s automated **`check_solutions`** (and related tooling where present). The courses have **not** been manually play-tested end-to-end yet—expect rough edges in UI copy, exercise ordering, or platform-specific behavior until a full human pass.

Monorepo of interactive terminal courses that share one **chapter JSON schema**, per-track **chapter tables** in each **`README`**, and **[TUTORIAL_PLATFORM.md](TUTORIAL_PLATFORM.md)** rules (grading, hints, authoring quality).

Clone once; each track lives in its own subdirectory with its own TUI/toolchain.

## Main menu (recommended)

### First-time setup (one root `.venv`)

From the **repository root**, run **one** of:

| Script | Who | What it installs |
|--------|-----|------------------|
| **`./scripts/setup-learn.sh`** | Learners | Hub + **C / C# / Python / Java** with `pip install -e .` (runtime only: Textual, etc.) |
| **`./scripts/setup-dev.sh`** | Contributors | Same, but `pip install -e ".[dev]"` — adds **pytest** for each Python track’s tests |

**Why two modes?**  
- **`pip install -e .`** installs only **`[project] dependencies`** — what you need to **run** the TUIs.  
- **`pip install -e ".[dev]"`** also installs **`[dev]` optional extras** (e.g. **pytest**) — for **`python -m pytest`** / `check_solutions` workflows, **not** required to study the courses.

Both scripts create or reuse **`.venv`** at the repo root and register the **`learn-languages`** command there. They do **not** install **Rust**, **Go**, or **asm** toolchains.

```bash
cd path/to/LEARN-LANGUAGES
./scripts/setup-learn.sh          # or: python3 scripts/bootstrap.py --learn
source .venv/bin/activate         # Windows: .venv\Scripts\activate
learn-languages
```

**Enter** opens the selected course; **q** quits the hub. When you quit a course, you return to this menu.

## Course TUI controls

Each track is a full-screen terminal UI. **Detailed key tables** live in that track’s **`README`** (look for **Keys** or **Keyboard reference**). The same actions appear everywhere with small binding differences:

| What you want | Keys (typical) |
|---------------|----------------|
| Move in a list | **`j`** / **`k`** or **↑** / **↓** |
| Open selection | **Enter** |
| Jump to chapter *N* | **`/`** then a digit (`1`–`9`, sometimes `0` = chapter 10) |
| Go back one screen | **`b`**, **Esc**, or **Backspace** |
| Quit the **course** (not the hub) | **`q`** (Rust/Go/asm also accept **Ctrl+C**) |
| Run / check your code | **`r`** |
| Edit in an external program | **`e`** (on the **code** screen) |
| Next hint after a failed run | **`h`** |
| Progress stats / help | **`s`** / **`?`** (from chapter list; Textual tracks) |

Usual flow: pick a chapter → read theory (optional) → pick an exercise → **`e`** to edit → **`r`** to run → **`h`** for hints if the output does not match.

### External editor (`$EDITOR`)

On the **code** screen, **`e`** opens a temp source file in your editor. The course **releases the terminal** while you edit (Textual tracks use **suspend**; Rust/Go/asm restore normal terminal mode). **Save and quit the editor** to return to the course. Quitting the editor is **not** the same as pressing **`q`** in the course (which exits the whole TUI).

**Set your editor** in the **same shell** before you run `learn-languages` or a track:

```bash
export EDITOR=nano              # good default if you are new to vim
export EDITOR=vim               # or nvim, micro, …
export EDITOR="code --wait"     # VS Code — must include --wait
```

To keep that every session, add the `export` line to `~/.bashrc` or `~/.zshrc`.

**If `EDITOR` is unset**, every track picks the **first** of these that exists on your **`PATH`** (same order everywhere):

**`nano`** → **`micro`** → **`vim`** → **`nvim`** → **`code`** → **`subl`**

**Leaving the editor:**

| Editor | Save and return to the course |
|--------|-------------------------------|
| **nano** | **Ctrl+O** (write), then **Ctrl+X** (exit) |
| **vim** / **nvim** | **Esc** (normal mode), then **`:wq`** + **Enter**. Use **`:q!`** + **Enter** to quit without saving. **ZZ** (two capital Z’s) also saves and quits. |

**Rust**, **Go**, and **asmx64** still need their compilers on `PATH` (see per-track READMEs). Manual alternative: `pip install -e .` at root plus `pip install -e .` in each Python track directory.

| Track | Directory | Direct run (without hub) |
|-------|-----------|---------------------------|
| Rust | [`rust/`](rust/) | `cargo run` |
| Go | [`go/`](go/) | `go run .` |
| C | [`c/`](c/) | `python -m learn_c_tui` |
| C# | [`csharp/`](csharp/) | `python -m learn_cs_tui` |
| Python | [`python/`](python/) | `python -m learn_python_tui` |
| Java | [`java/`](java/) | `python -m learn_java_tui` |
| x86-64 asm (NASM / ELF64) | [`asmx64/`](asmx64/) | `cargo run --release` |

## Runtime requirements (summary)

Each track’s **`README`** is authoritative. At a glance:

| Track | Run the TUI | Grade / execute learner code | Optional |
|-------|-------------|------------------------------|----------|
| **Rust** | `rustc`, `cargo` (on `PATH`) | same + temp `rustc` / `cargo` per exercise rules | `EDITOR`; **`python3`** only for `scripts/check_solutions.py` |
| **Go** | **Go 1.20+** (`go version` at startup) | `go run` on a temp `main.go` | `EDITOR`; **`python3`** for `scripts/check_solutions.py` |
| **C** | **Python 3.10+**, Textual (`pip install -e …`) | **`cc`** or **`gcc`** (C11) | `EDITOR` |
| **C#** | **Python 3.10+**, Textual | **.NET SDK** — TUI: `build` + `run --no-build`; checker: parallel `exec` (see **`csharp/README`**) | `EDITOR`; **`python3`** for `scripts/check_solutions.py` |
| **Python** | **Python 3.10+** (also runs learner code) | same interpreter | `EDITOR` |
| **Java** | **Python 3.10+**, Textual | **JDK 17+** (`javac`, `java`) | `EDITOR` |
| **asmx64** | **Rust** (`cargo` to build the TUI) | **nasm**, **ld**, **gcc** (Linux / WSL2) | **`python3`** for `scripts/check_solutions.py` |

## Platform support (v1)

Legend: **Yes** = supported for the course TUI and exercise checks; **WSL** = use Windows Subsystem for Linux; **No** = not supported in v1.

| Track | Linux | macOS | Windows (native) | Notes |
|-------|:-----:|:-----:|:----------------:|-------|
| **Rust** | Yes | Yes | Yes | [rustup](https://rustup.rs/) on all three |
| **Go** | Yes | Yes | Yes | `go` on `PATH` |
| **C** | Yes | Yes | No | **`cc`/`gcc`** (POSIX); **not** MSVC — use **WSL2** on Windows |
| **C#** | Yes | Yes | Yes | [.NET SDK](https://dotnet.microsoft.com/download) |
| **Python** | Yes | Yes | Yes | Python 3.10+ |
| **Java** | Yes | Yes | Yes | JDK 17+ |
| **asmx64** | Yes | No | No | **ELF64 / NASM / GNU `ld`** — Linux only; on Windows use **WSL2** |

Details and caveats: each track **`README`** (sections **Platform** or **Requirements**).

## Finding chapters

Each track loads exercise JSON from a **`chapters/`** directory. Resolution order (all tracks):

1. **`LEARN_<TRACK>_CHAPTERS`** — absolute path you set (override for forks or custom trees).
2. **`./chapters`** under the **current working directory** (must contain at least one `*.json`).
3. **Auto-locate** — walk upward from the running binary (Rust, Go, asmx64) or from the installed Python package directory (C, C#, Python, Java).
4. Fallback: literal **`chapters`** (works when cwd is the track directory).

| Track | Override env var |
|-------|------------------|
| Rust | `LEARN_RUST_CHAPTERS` |
| Go | `LEARN_GO_CHAPTERS` |
| C | `LEARN_C_CHAPTERS` |
| C# | `LEARN_CSHARP_CHAPTERS` |
| Python | `LEARN_PYTHON_CHAPTERS` |
| Java | `LEARN_JAVA_CHAPTERS` |
| asmx64 | `LEARN_ASMX64_CHAPTERS` |

**What to do in practice**

- **Easiest:** `cd` into the track (e.g. `go/`) and run its TUI, or pick the course from **`learn-languages`** (the hub always runs with cwd = that track).
- **pip-installed Textual courses:** often work without the env var because the app finds **`chapters/`** next to the editable checkout via the package path.
- **Custom layout:** set the env var in the same shell before starting the TUI or checker, e.g. `export LEARN_GO_CHAPTERS=/path/to/my/chapters`.

Regenerate README chapter tables after editing JSON: **`python3 scripts/sync_readme_chapter_tables.py`**.

### Per-track README outline

Every course under **`rust/`**, **`go/`**, **`c/`**, … uses the same section order where it applies: **Platform** → **Requirements** (toolchain, **startup** check, **grading**, **`$EDITOR`**) → **Install** / **Run** → **Learner workflow** → **Keys (summary)** → **Course layout** → **Maintainer: verify bundled solutions** (if present) → **Security** → **Tests** (if present). Track-specific caveats (e.g. **WSL2** for C/asm, **`cargo test`** vs **`go test`**) stay in that track’s file.

## Shared docs

| Doc | Contents |
|-----|----------|
| **Each track `README`** | Chapter list table (`#`, title, exercise count) from `chapters/*.json` |
| **[TUTORIAL_PLATFORM.md](TUTORIAL_PLATFORM.md)** | JSON schema, stdout checks, authoring rules |

**VS Code / Cursor:** **File → Open Workspace from File…** and choose **[`learn-languages.code-workspace`](learn-languages.code-workspace)** at the repo root (folder path is **`.`**, portable across machines).

## Authoring

Chapter JSON lives in **`./chapters/`** under each language directory (sorted by filename). Edit those files in place for that track; there is no repo-root generator that copies chapters from another language.

Each track’s **`scripts/check_solutions.py`** verifies bundled reference solutions. See that track’s **`README`** for flags and work directories.

**Maintainers:** from the repo root after **`./scripts/setup-dev.sh`**, run the full matrix (pytest, `go test`, `cargo test`/build, JSON parse, parallel **`check_solutions`**) with:

```bash
./scripts/verify-all.sh
```

Use **`./scripts/verify-all.sh --skip-check-solutions`** for a faster pass without grading every reference solution. The script resolves **`PYTHON`** to an absolute path (default: **`.venv/bin/python`**) so parallel track runs never break on `cd`.

**Pedagogical quality** (real computation in solutions, scaffolds in starters, language-appropriate theory) is required; see **TUTORIAL_PLATFORM.md**.
