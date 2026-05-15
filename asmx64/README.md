# LEARN-ASMx64

Interactive **Linux x86-64** assembly course in the terminal: **NASM**, **Intel syntax**, **ELF64**. Exercises are checked by assembling, linking, and running your program locally, comparing trimmed **stdout** to the expected text.

## Prerequisites (Linux)

Install a toolchain that can build ELF64 user programs:

- **nasm** — assembler (`apt install nasm` / `dnf install nasm`)
- **binutils** — GNU **ld** (`apt install binutils` / `dnf install binutils`)
- **gcc** — used when an exercise uses **`extern`** libc symbols; also handy for reading compiler output (`apt install build-essential` or `gcc`)

Smoke-check versions:

```bash
nasm -v
ld --version
gcc --version
```

The TUI refuses to start if any of these commands are missing or fail: it prints an explanation to **stderr** and exits with a **non-zero status** before the alternate-screen UI starts.

## Windows users (v1)

Native **Windows PE** build/run is **not** supported in v1. Use **WSL2** with a Linux distribution (e.g. Ubuntu), install the same packages inside that Linux environment, and run the TUI there. From the app’s perspective the course remains **Linux-only**.

## Intel syntax and AT&T

All exercises you **write** use **Intel syntax** with **NASM**. **AT&T** syntax appears often in **`gcc -S`** listings and default **`objdump`** disassembly. When you need Intel mnemonics in disassembly, use:

```bash
objdump -d -M intel ./your_binary
```

## Running the TUI

From the repository root:

```bash
cargo run --release
```

Progress is stored under `~/.learn-asmx64-tui/` (e.g. `progress.json`).

Typical keys match other LEARN-* tutorials: open the in-app help for the exact bindings (chapter list, run, edit, hints).

## Verifying reference solutions (CI / maintainers)

```bash
python3 scripts/check_solutions.py
```

Optional: `python3 scripts/check_solutions.py --chapter variables`  
Failures only: `python3 scripts/check_solutions.py --list-failures-only`

To reuse one build directory instead of per-exercise temp dirs:

```bash
export LEARN_ASMX64_CHECK_WORK="$PWD/.check-asm-crate"
python3 scripts/check_solutions.py
```

## Security and trust

This tool **writes your assembly to disk**, **assembles and links** it, then **executes the resulting binary** on your machine, with **timeouts** to limit runaway programs. It is intended for **trusted local learning** on your own workstation. Do not point it at untrusted chapter JSON from unknown sources without review. There is **no** sandbox beyond normal user permissions; treat course content like source code you would compile.

## Content layout

Chapter JSON lives under `chapters/*.json` (sorted by filename). The catalog follows the shared [LEARN-LANGUAGES/CURRICULUM.md](../CURRICULUM.md) **Asm** column: only **Adapted / Full** slots are present (for example there is no dedicated `json` chapter in v1). The schema matches other LEARN-* courses (`starter_code`, `expected_output`, `hints`, `solution`, etc.); see [TUTORIAL_PLATFORM.md](../TUTORIAL_PLATFORM.md) if you author new chapters.

## License

See project policy for your fork; the course text and code are for learning purposes.
