# LEARN-LANGUAGES

Monorepo of interactive terminal courses that share one chapter schema, curriculum outline, and platform rules.

| Track | Directory | Run (see each README) |
|-------|-----------|------------------------|
| Rust | [`rust/`](rust/) | `cargo run` from `rust/` |
| Go | [`go/`](go/) | `go run .` from `go/` |
| C | [`c/`](c/) | `python -m learn_c_tui` from `c/` |
| C# | [`csharp/`](csharp/) | `python -m learn_csharp_tui` from `csharp/` |
| x86-64 asm (NASM) | [`asmx64/`](asmx64/) | `cargo run` from `asmx64/` |

## Shared docs

- **[CURRICULUM.md](CURRICULUM.md)** — chapter order, ids, and per-language coverage matrix
- **[TUTORIAL_PLATFORM.md](TUTORIAL_PLATFORM.md)** — JSON schema, executors, grading rules

Open the whole tree in VS Code/Cursor with [`learn-languages.code-workspace`](learn-languages.code-workspace).

## Authoring

Chapter JSON lives under each track’s `chapters/` directory. Regenerator scripts are in [`scripts/`](scripts/) and language-specific `scripts/` folders; paths are relative to this monorepo root.
