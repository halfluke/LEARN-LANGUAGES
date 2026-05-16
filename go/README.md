# Learn Go TUI

An interactive terminal-based Go learning platform with chapters, exercises, code validation, and progress tracking.

**Monorepo layout:** this tree is **`go/`** inside **LEARN-LANGUAGES** (`cd path/to/LEARN-LANGUAGES/go`).

## Platform

**Linux, macOS, and Windows** — install **Go 1.20+** from [go.dev/dl](https://go.dev/dl/). See **[../README.md](../README.md#platform-support-v1)**.

---

## Requirements

- **Go** toolchain on your **`PATH`** (the README targets **Go 1.20+**; use a current stable release from [go.dev/dl](https://go.dev/dl/)).
- **Text editor** for exercises: set **`EDITOR`** if you like; otherwise the app tries **`vim`**, **`nano`**, **`code`**, and **`subl`** on your `PATH` (same idea as LEARN-RUST).

**Startup check:** Before the Bubble Tea UI starts, the binary runs **`go version`** (trying `go` on `PATH` and a few common install locations). If Go is not available, it prints an explanation to **stderr** and exits with a **non-zero status** (the TUI never starts). When Go is found, you may see one **success line on stderr** before the UI loads.

**How exercises are checked:** The TUI does **not** only lint your source. It writes your code to a temporary **`main.go`** and runs **`go run`** on that file (with a timeout), then compares trimmed **stdout** to the exercise’s **`expected_output`**.

There is **no** bundled `check_solutions.py` in this track—only the Go toolchain and an editor are required to learn.

## Install

From the **`go/`** directory (repository root layout):

```bash
cd path/to/LEARN-LANGUAGES/go
go build -o learn-go-tui .
./learn-go-tui
```

Or run without a separate binary:

```bash
go run .
```

## How to Use

### Navigation

| Key | Action |
|-----|--------|
| `↑/↓` or `k/j` | Navigate chapter/exercise list |
| `Enter` | Select chapter/exercise |
| `/` | Jump to a chapter by number |
| `←` / `Esc` / `Backspace` / `b` | Go back |
| `q` or `Ctrl+C` | Quit |

### Exercises

| Key | Action |
|-----|--------|
| `e` | Open $EDITOR to write code |
| `r` | Run and validate your code |
| `h` | Get a hint (up to 2 hints per exercise) |

### Workflow

1. Select a chapter from the main menu
2. Choose an exercise
3. Press `e` to open your editor
4. Write your solution, save & close
5. Press `r` to run and validate
6. If incorrect, press `h` for hints
7. Repeat until correct

### Progress

Progress is saved automatically to `~/.learn-go-tui/progress.json`.

## Chapters

Chapters load from `chapters/*.json` in **lexicographic filename order** (prefixed names like `01_variables.json` … `19_time.json`). The canonical outline lives in **[../CURRICULUM.md](../CURRICULUM.md)**. There is **no** `05_lifetimes.json` in Go (lifetimes are **N/A** for Go in the shared matrix). Shared schema and grading rules: **[../TUTORIAL_PLATFORM.md](../TUTORIAL_PLATFORM.md)**.

| # | Chapter | Exercises |
|---|---------|-----------|
| 1 | Variables & Types | 7 |
| 2 | Ownership (Go: values, copies, references) | 3 |
| 3 | Control Flow | 7 |
| 4 | Functions | 7 |
| 5 | Arrays | 7 |
| 6 | Slices | 7 |
| 7 | Maps | 7 |
| 8 | Strings & Runes | 7 |
| 9 | Structs | 7 |
| 10 | Interfaces | 7 |
| 11 | Methods | 7 |
| 12 | Packages | 7 |
| 13 | Pointers | 7 |
| 14 | Error Handling | 7 |
| 15 | Concurrency | 7 |
| 16 | Testing | 5 |
| 17 | JSON | 9 |
| 18 | Time | 9 |
