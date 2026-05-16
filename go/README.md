# LEARN-Go

Interactive **Go** course in the terminal: **`chapters/*.json`** (**[TUTORIAL_PLATFORM.md](../TUTORIAL_PLATFORM.md)**), **`go run`** / **`go test`** in a temp module, **trimmed stdout** (or **all tests pass**) checks.

The UI is **Bubble Tea** (Go). Learner code opens in **`$EDITOR`** when you press **`e`**.

**Location:** **`go/`** in the **LEARN-LANGUAGES** monorepo.

## Platform

**Linux, macOS, and Windows** — **Go 1.20+** on **`PATH`**. See **[../README.md](../README.md#platform-support-v1)**.

## Requirements

### Go toolchain

Install a current stable release from [go.dev/dl](https://go.dev/dl/) (README targets **1.20+**).

**Verify:**

```bash
go version
```

**Startup:** before the UI starts, the binary runs **`go version`**. If Go is missing, it prints to **stderr** and exits **non-zero** (no TUI).

**Grading:** your editor buffer is turned into a small module under **`learnsnippet`** (see **Multi-file code** below). Most exercises use **`go run .`** and compare **stdout**; testing exercises use **`go test`** when **`expected_output`** is **`PASS`**.

### Multi-file code (packages & testing)

In one buffer you can use either:

- A line with only **`---`** between files (e.g. **`main.go`** above, **`main_test.go`** below), or  
- **`// File: path/to/file.go`** before each file (e.g. **`// File: utils/utils.go`**).

The TUI writes those files, adds **`go.mod`**, and runs **`go run .`** or **`go test`**. Import your packages as **`learnsnippet/utils`**, **`learnsnippet/counter`**, etc.

### External editor (`e`)

Press **`e`** on the **code** screen. Set **`EDITOR`** before starting (e.g. `export EDITOR=nano`). If unset: **`nano`** → **`micro`** → **`vim`** → **`nvim`** → **`code`** → **`subl`**. Details: **[../README.md#course-tui-controls](../README.md#course-tui-controls)**.

## Install

From **`go/`**:

```bash
cd path/to/LEARN-LANGUAGES/go
go build -o learn-go-tui .
```

**Hub:** the root **`learn-languages`** menu can open this track after you build the binary; the hub does **not** install Go for you.

## Run

```bash
./learn-go-tui
# or without installing a binary:
go run .
```

**Progress:** `~/.learn-go-tui/progress.json`

**Chapter directory:** auto-resolved (see **[../README.md#finding-chapters](../README.md#finding-chapters)**); override with **`LEARN_GO_CHAPTERS`**. Default when run from **`go/`**: **`chapters/`**.

## Learner workflow

1. Start the TUI (**Run** above) or pick **Go** from **`learn-languages`** (after **`go build`**).
2. Pick a **chapter**, then an **exercise** (scroll **theory** with **`j`** / **`k`** if you want).
3. Press **`e`** — edit in **`$EDITOR`**, then **save and quit**.
4. Press **`r`** — **`go run`** and stdout check.
5. On failure, press **`h`** for the next hint (up to two per exercise).
6. Repeat until correct; progress saves automatically.

## Keys (summary)

| Context | Keys |
|--------|------|
| Chapter list | **`j`** / **`k`** or **↑** / **↓**, **Enter**, **`/`** jump, **`?`** help, **`s`** stats, **`q`** or **Ctrl+C** quit |
| Theory | **`j`** / **`k`** or **↑** / **↓** scroll, **Enter** → exercises, **`b`** / **Esc** / **Backspace** back |
| Exercises | **`j`** / **`k`**, **Enter** open, **`b`** back |
| Code | **`r`** run, **`e`** **`$EDITOR`**, **`b`** back |
| Result | **`h`** hint on failure, **`r`** re-run, **`b`** back |

## Course layout

Chapters live under **`chapters/*.json`** (filename order). Edit JSON in place. Schema: **[../TUTORIAL_PLATFORM.md](../TUTORIAL_PLATFORM.md)**.

**18** chapters, **124** exercises — loaded from **`chapters/*.json`** (filename order).

| # | Chapter | Exercises |
|---|---------|-----------|
| 1 | Variables & Types | 7 |
| 2 | Values, copies, and references (Go) | 3 |
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


## Maintainer: verify bundled solutions

```bash
python3 scripts/check_solutions.py
python3 scripts/check_solutions.py --chapter variables
python3 scripts/check_solutions.py --list-failures-only
```

Default work dir: **`.check-go-work`**. Override: **`LEARN_GO_CHECK_WORK`**.

**Chapter path override:** **`LEARN_GO_CHAPTERS=/path/to/chapters`** (same resolution as the TUI — see **[../README.md#finding-chapters](../README.md#finding-chapters)**).

Loader smoke test: **`go test`** from **`go/`**.

## Security

Writes **`main.go`**, runs **`go run`** locally with **timeouts**. Trust chapter content like any local run-snippet educator.

## Tests

```bash
go test
```
