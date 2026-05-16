# LEARN-LANGUAGES

Monorepo of interactive terminal courses that share one **chapter JSON schema**, a single **[CURRICULUM.md](CURRICULUM.md)** outline, and **[TUTORIAL_PLATFORM.md](TUTORIAL_PLATFORM.md)** rules (grading, hints, authoring quality).

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

## Authoring

Chapter JSON lives in **`./chapters/`** under each language directory (sorted by filename). Edit those files in place for that track; there is no repo-root generator that copies chapters from another language.

Each track’s **`scripts/check_solutions.py`** verifies bundled reference solutions. See that track’s **`README`** for flags and work directories.

**Pedagogical quality** (real computation in solutions, scaffolds in starters, language-appropriate theory) is required; see **CURRICULUM.md**.
