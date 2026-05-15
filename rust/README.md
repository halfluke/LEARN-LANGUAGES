# Learn Rust TUI

Terminal-based Rust course: chapters, short theory, hands-on exercises, and automatic checks against expected program output.

---

## What to install

### Rust toolchain (required)

You need **`rustc`** and **`cargo`** on your `PATH`.

- **Recommended:** [rustup](https://rustup.rs/) — install stable, then confirm:

  ```bash
  rustc --version
  cargo --version
  ```

- **Distro packages (e.g. Debian / Kali):** `sudo apt install rustc cargo` — versions vary; if anything fails to compile, prefer rustup.

**Startup check:** Before the full-screen TUI starts, the app runs **`rustc --version`**. If `rustc` is missing or the command fails, it prints an explanation to **stderr** and exits with a **non-zero status** (the TUI never starts). Some exercises still need **`cargo`** on your `PATH`; that is **not** probed at startup and would surface when you run those snippets.

The first time you build or run, Cargo will compile dependencies (ratatui, serde, etc.). That can take a minute; later runs are much faster. Build artifacts live in **`target/`** (ignored by Git).

### Text editor (required for exercises)

Exercises open in an external editor when you press **`e`**.

- Set **`EDITOR`** to something you like, for example:

  ```bash
  export EDITOR=nvim   # or vim, nano, micro, etc.
  ```

- If **`EDITOR`** is unset, the app looks for **`vim`**, **`nvim`**, **`nano`**, **`micro`**, **`code`**, or **`subl`** on your `PATH`.

For **VS Code** from the terminal, use wait mode so the TUI resumes after you close the tab:

```bash
export EDITOR="code --wait"
```

### Optional: Python (only for maintainers)

Regenerating or bulk-checking bundled chapter JSON uses **`python3`**. Learners using the shipped **`chapters/*.json`** do **not** need Python.

---

## How to run the app

Clone the repository and run from the **repository root** (the app loads **`chapters/`** relative to the current working directory):

```bash
git clone https://github.com/halfluke/learn-rust.git
cd learn-rust
cargo run
```

Release build (faster binary, same requirement to run from repo root):

```bash
cargo build --release
./target/release/learn-rust-tui
```

---

## How to work through exercises

1. **Start the TUI** (`cargo run` from the repo root).
2. **Pick a chapter**, then an **exercise**.
3. Read the **theory** screen if you want, then open the exercise.
4. Press **`e`** — your **`$EDITOR`** opens a temporary **`main.rs`** with starter code. Write a normal Rust program (usually with **`fn main()`**). Save and **quit the editor** to return to the TUI.
5. Press **`r`** — the app compiles and runs your code, then compares **standard output** (trimmed) to the exercise’s **expected output**.
6. If it fails, press **`h`** for a hint (up to two hints, then you can see the reference solution flow from the UI).

### How your code is run

So you know what environment to target:

| Your code | What runs |
|-----------|-----------|
| Typical std-only snippet | **`rustc`** on a single file, then the binary. |
| Uses **serde** / **serde_json** / **chrono** / **chrono_tz** (as in some later chapters) | **`cargo run`** in a small temporary project with those dependencies. |
| Contains **`#[test]`** (testing chapter) | **`cargo test`**; success is **all tests passing**, not matching a printed line. |

Warnings on stderr do **not** fail an exercise by themselves; **exit status** and **stdout** (where applicable) drive the check.

### Progress

Completed exercises are recorded in **`~/.learn-rust-tui/progress.json`**.

---

## Keyboard reference

### Navigation

| Key | Action |
|-----|--------|
| `↑/↓` or `k/j` | Move in chapter or exercise list |
| `Enter` | Open chapter or start exercise |
| `/` | Jump to chapter by number (`1`–`9`, `0` for chapter 10) |
| `Esc` / `Backspace` / `b` | Go back |
| `q` or `Ctrl+C` | Quit |
| `s` | Stats (from chapter list) |
| `?` | Help (from chapter list) |

### While solving

| Key | Action |
|-----|--------|
| `e` | Edit exercise in **`$EDITOR`** |
| `r` | Compile / run / check output |
| `h` | Next hint after a failed run |

---

## Course layout

There are **17** chapters under **`chapters/*.json`**, loaded in filename order, with **121** exercises total. Each exercise defines starter code, expected output, hints, and a reference solution used by the UI and maintainer scripts.

---

## Maintainer notes (optional)

- **Regenerate chapter JSON** from port scripts: `python3 scripts/forge_chapters.py` (see script header for inputs and paths).
- **Verify all reference solutions:** `python3 scripts/check_solutions.py` (uses **`.check-solutions-crate`** and **`.check-solutions-target`** under the repo; see script for flags).
- **Shared platform write-up** (schema, executor rules, design decisions): if you keep a **`LEARN-LANGUAGES`** tree next to this repo, see **`../TUTORIAL_PLATFORM.md`**.
