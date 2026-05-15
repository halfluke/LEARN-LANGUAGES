# LEARN-LANGUAGES

Monorepo of interactive terminal courses that share one **chapter JSON schema**, a single **[CURRICULUM.md](CURRICULUM.md)** outline, and **[TUTORIAL_PLATFORM.md](TUTORIAL_PLATFORM.md)** rules (grading, hints, parity).

Clone once; each track lives in its own subdirectory with its own TUI/toolchain.

| Track | Directory | Typical run |
|-------|-----------|-------------|
| Rust | [`rust/`](rust/) | `cargo run` |
| Go | [`go/`](go/) | `go run .` |
| C | [`c/`](c/) | `python -m learn_c_tui` |
| C# | [`csharp/`](csharp/) | `python -m learn_cs_tui` |
| Python | [`python/`](python/) | `python -m learn_python_tui` |
| Java | [`java/`](java/) | `python -m learn_java_tui` |
| x86-64 asm (NASM / ELF64) | [`asmx64/`](asmx64/) | `cargo run` |

## Shared docs

| Doc | Contents |
|-----|----------|
| **[CURRICULUM.md](CURRICULUM.md)** | Chapter order (`01_` … `19_`), ids, coverage matrix |
| **[TUTORIAL_PLATFORM.md](TUTORIAL_PLATFORM.md)** | JSON schema, stdout checks, authoring rules |

Workspace file: **[`learn-languages.code-workspace`](learn-languages.code-workspace)**.

## Authoring and regeneration

Chapter JSON lives in **`./chapters/`** under each language directory (sorted by filename). Cross-track parity for some languages uses scripts under **`scripts/`** at the repo root (for example `scripts/regenerate_cs_c_parity.py`, `scripts/regenerate_py_java_parity.py`); track-specific tooling also lives under each track’s **`scripts/`**. Each track **`README`** lists verifier commands (`check_solutions`, etc.).

**Pedagogical parity** (solutions derive real computation, starters are scaffolds, not echoed stdout-only strings) is required for merged chapters; see **CURRICULUM.md**.
