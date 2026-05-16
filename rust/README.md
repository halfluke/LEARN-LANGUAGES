# LEARN-Rust

Interactive **Rust** course in the terminal: **`chapters/*.json`** (**[TUTORIAL_PLATFORM.md](../TUTORIAL_PLATFORM.md)**), **`rustc`** / **`cargo`** as needed, **trimmed stdout** (or **`cargo test`** for test exercises).

The UI is **ratatui** (Rust). Learner code is edited in **`$EDITOR`** when you press **`e`**.

**Location:** **`rust/`** in the **LEARN-LANGUAGES** monorepo.

## Platform

**Linux, macOS, and Windows** — **`rustc`** / **`cargo`** via [rustup](https://rustup.rs/) (or distro packages on Linux). See **[../README.md](../README.md#platform-support-v1)**.

## Requirements

### Rust toolchain

You need **`rustc`** and **`cargo`** on your **`PATH`**.

- **Recommended:** [rustup](https://rustup.rs/) — install stable, then confirm:

  ```bash
  rustc --version
  cargo --version
  ```

- **Distro packages (e.g. Debian / Kali):** `sudo apt install rustc cargo` — if builds fail, prefer rustup.

**Startup:** the app runs **`rustc --version`** before the TUI starts. On failure it prints to **stderr** and exits **non-zero** (no UI). Some exercises need **`cargo`** at run time; that is not probed at startup.

The first **`cargo run`** / build compiles dependencies (ratatui, serde, …) and may take a minute; later runs are faster. Artifacts live in **`target/`** (gitignored).

### External editor (`e`)

Press **`e`** on the **code** screen. Set **`EDITOR`** before starting (e.g. `export EDITOR=nano`). If unset: **`nano`** → **`micro`** → **`vim`** → **`nvim`** → **`code`** → **`subl`**. VS Code: `export EDITOR="code --wait"`. Save/quit details: **[../README.md#course-tui-controls](../README.md#course-tui-controls)**.

### Optional: Python (maintainers only)

**`python3 scripts/check_solutions.py`** — learners do not need Python.

## How exercises are checked

| Your code | What runs |
|-----------|-----------|
| Typical std-only snippet | **`rustc`** on one file, then the binary |
| Uses **serde** / **serde_json** / **chrono** / **chrono_tz** | **`cargo run`** in a small temp project with those deps |
| Contains **`#[test]`** | **`cargo test`** — success = all tests pass, not stdout match |

Warnings on **stderr** do not fail an exercise by themselves; **exit status** and **stdout** (where applicable) drive the check. Trimmed **stdout** is compared to **`expected_output`** when applicable.

## Install

From **`rust/`** (directory with **`Cargo.toml`** and **`chapters/`**):

```bash
cd path/to/LEARN-LANGUAGES/rust
cargo build --release   # optional; first build downloads crates
```

**Hub:** the root **`learn-languages`** menu lists this track, but you still install Rust yourself (above). The hub does not install rustup.

## Run

```bash
cargo run
# or:
./target/release/learn-rust-tui
```

**Progress:** `~/.learn-rust-tui/progress.json`

**Chapter directory:** auto-resolved; override with **`LEARN_RUST_CHAPTERS`**. See **[../README.md#finding-chapters](../README.md#finding-chapters)**. Default when run from **`rust/`**: **`chapters/`** next to **`Cargo.toml`**.

## Learner workflow

1. Start the TUI (**Run** above) or pick **Rust** from **`learn-languages`** at the repo root (after building this crate).
2. Pick a **chapter**, then an **exercise** (read **theory** if you want).
3. Press **`e`** — edit **`main.rs`** (starter code provided). **Save and quit** the editor.
4. Press **`r`** — compile/run/check.
5. On failure, press **`h`** for the next hint (up to two per exercise).
6. Repeat until correct; progress saves automatically.

## Keys (summary)

| Context | Keys |
|--------|------|
| Chapter list | **`j`** / **`k`** or **↑** / **↓**, **Enter**, **`/`** jump (`1`–`9`, **`0`** = ch. 10), **`?`** help, **`s`** stats, **`q`** or **Ctrl+C** quit |
| Theory | **`j`** / **`k`** or **↑** / **↓** scroll, **Enter** → exercises, **`b`** / **Esc** / **Backspace** back |
| Exercises | **`j`** / **`k`**, **Enter** open, **`b`** back |
| Code | **`r`** compile/run, **`e`** **`$EDITOR`**, **`b`** back |
| Result | **`h`** hint on failure, **`r`** re-run, **`b`** back |

## Course layout

Chapters live under **`chapters/*.json`** (filename order). Edit JSON in place. Schema: **[../TUTORIAL_PLATFORM.md](../TUTORIAL_PLATFORM.md)**.

**19** chapters, **127** exercises — loaded from **`chapters/*.json`** (filename order).

| # | Chapter | Exercises |
|---|---------|-----------|
| 1 | Variables & Types | 7 |
| 2 | Ownership, moves, and copies | 3 |
| 3 | Control Flow | 7 |
| 4 | Functions | 7 |
| 5 | Lifetimes (basics) | 3 |
| 6 | Arrays | 7 |
| 7 | Slices | 7 |
| 8 | Maps | 7 |
| 9 | Strings & Unicode | 7 |
| 10 | Structs | 7 |
| 11 | Traits | 7 |
| 12 | Methods | 7 |
| 13 | Packages | 7 |
| 14 | Pointers | 7 |
| 15 | Error Handling | 7 |
| 16 | Concurrency | 7 |
| 17 | Testing | 5 |
| 18 | JSON | 9 |
| 19 | Time | 9 |


## Maintainer: verify bundled solutions

```bash
python3 scripts/check_solutions.py
python3 scripts/check_solutions.py --chapter variables
python3 scripts/check_solutions.py --list-failures-only
```

Uses **`.check-solutions-crate`** / **`.check-solutions-target`** under **`rust/`** (see script for flags).

## Security

Writes source, compiles, and runs binaries locally with **timeouts**. Trust chapter content like any local compile-and-run course.

## Tests

```bash
cargo test
```
