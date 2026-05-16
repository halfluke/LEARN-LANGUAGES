# LEARN-ASMx64

Interactive **Linux x86-64** assembly course in the terminal: **NASM**, **Intel syntax**, **ELF64**. Exercises are assembled, linked, and run locally; **trimmed stdout** is compared to the expected text.

The UI is **ratatui** (Rust). Learner code opens in **`$EDITOR`** when you press **`e`**.

**Location:** **`asmx64/`** in the **LEARN-LANGUAGES** monorepo.

## Platform

**Linux only** (v1) for exercise binaries (**ELF64**, NASM, GNU **`ld`**). **macOS and Windows (native): not supported** — on Windows use **WSL2** (below). See **[../README.md](../README.md#platform-support-v1)**.

## Requirements

### Run the TUI (host)

- **Rust toolchain** — **`cargo`** and **`rustc`** on **`PATH`** ([rustup](https://rustup.rs/) recommended).

### Assemble and run learner programs

- **nasm** — `apt install nasm` / `dnf install nasm`
- **binutils** — GNU **ld** (`apt install binutils` / `dnf install binutils`)
- **gcc** — libc **`extern`** symbols and compiler listings (`apt install build-essential` or `gcc`)

**Verify:**

```bash
nasm -v
ld --version
gcc --version
```

**Startup:** if **nasm**, **ld**, or **gcc** is missing or fails, the app prints to **stderr** and exits **non-zero** before the TUI starts.

**Grading:** assemble/link/run your program with **timeouts**; compare trimmed **stdout** to **`expected_output`**.

### External editor (`e`)

Press **`e`** on the **code** screen. Set **`EDITOR`** before starting (e.g. `export EDITOR=nano`). If unset: **`nano`** → **`micro`** → **`vim`** → **`nvim`** → **`code`** → **`subl`**. Details: **[../README.md#course-tui-controls](../README.md#course-tui-controls)**.

### Optional: Python (maintainers)

**`python3 scripts/check_solutions.py`** — same **nasm** / **ld** / **gcc** toolchain as the TUI.

## Windows users (v1)

Native **Windows PE** is **not** supported. Use **WSL2** (e.g. Ubuntu), install the Linux packages above inside WSL, and run the TUI there.

## Intel syntax and AT&T

Exercises you **write** use **Intel syntax** with **NASM**. **AT&T** often appears in **`gcc -S`** and default **`objdump`** output. For Intel disassembly:

```bash
objdump -d -M intel ./your_binary
```

## Install

From **`asmx64/`** ( **`Cargo.toml`** + **`chapters/`** ):

```bash
cd path/to/LEARN-LANGUAGES/asmx64
cargo build --release
```

**Hub:** the root menu lists this track; you must install **Rust**, **nasm**, **ld**, and **gcc** yourself (the hub does not install them).

## Run

```bash
cargo run --release
# or:
./target/release/learn-asmx64-tui
```

**Progress:** `~/.learn-asmx64-tui/progress.json`

**Chapter directory:** auto-resolved; override with **`LEARN_ASMX64_CHAPTERS`**. See **[../README.md#finding-chapters](../README.md#finding-chapters)**.

## Learner workflow

1. Start the TUI (**Run** above) or pick **asmx64** from **`learn-languages`** (after building this crate, on **Linux** or **WSL2**).
2. Pick a **chapter**, then an **exercise** (read **theory** if you want).
3. Press **`e`** — edit assembly in **`$EDITOR`**, then **save and quit**.
4. Press **`r`** — assemble/link/run and compare stdout.
5. On failure, press **`h`** for the next hint (up to two per exercise).
6. Repeat until correct; progress saves automatically.

## Keys (summary)

| Context | Keys |
|--------|------|
| Chapter list | **`j`** / **`k`** or **↑** / **↓**, **Enter**, **`/`** jump, **`?`** help, **`s`** stats, **`q`** or **Ctrl+C** quit |
| Theory | **`j`** / **`k`** or **↑** / **↓** scroll, **Enter** → exercises, **`b`** back |
| Exercises | **`j`** / **`k`**, **Enter** open, **`b`** back |
| Code | **`r`** assemble/run, **`e`** **`$EDITOR`**, **`b`** back |
| Result | **`h`** hint on failure, **`r`** re-run, **`b`** back |

## Course layout

Chapters live under **`chapters/*.json`** (filename order). Edit JSON in place. Schema: **[../TUTORIAL_PLATFORM.md](../TUTORIAL_PLATFORM.md)**.

**10** chapters, **41** exercises — loaded from **`chapters/*.json`** (filename order).

| # | Chapter | Exercises |
|---|---------|-----------|
| 1 | Variables & Syscalls | 5 |
| 2 | Control flow | 4 |
| 3 | Functions & calls | 4 |
| 4 | Arrays in .data | 4 |
| 5 | Pointer + length | 4 |
| 6 | Strings & bytes | 4 |
| 7 | Struct layout | 4 |
| 8 | Method-style calls | 4 |
| 9 | Pointers & memory | 4 |
| 10 | Atomic update | 4 |


## Maintainer: verify bundled solutions

```bash
python3 scripts/check_solutions.py
python3 scripts/check_solutions.py --chapter variables
python3 scripts/check_solutions.py --list-failures-only
```

Reuse one build tree:

```bash
export LEARN_ASMX64_CHECK_WORK="$PWD/.check-asm-crate"
python3 scripts/check_solutions.py
```

## Security

Writes assembly, assembles, links, and **executes** the binary locally with **timeouts**. No sandbox beyond your user account — trust chapter content like any compile-and-run educator.

## Tests

```bash
cargo test
```
