# Tutorial platform (LEARN-* TUI model)

**Location:** This file lives under **`LEARN-LANGUAGES/`** next to your **`LEARN-*`** repos (e.g. under `Downloads/`). It is **not** inside any language git tree so every tutorial project can reference **one canonical** copy—edit it here, then `@LEARN-LANGUAGES/TUTORIAL_PLATFORM.md` (or the full path) from any root in your workspace.

This document captures the **architecture and decisions** for the **LEARN-*** terminal courses: JSON chapters, local compile/run, and stdout-first grading.

**Curriculum source of truth:** chapter **themes**, **ordering**, **per-language coverage**, and **pedagogical parity** (solutions, theory/descriptions, starters) live in **[CURRICULUM.md](CURRICULUM.md)**. Historical “mirror LEARN-GO exercise-for-exercise” parity is **not** normative; each language course owns its pedagogy while sharing this **schema** and **platform mechanics**.

**Scope:** JSON-driven chapters, local compile/run, stdout comparison, optional `cargo`/multi-file patterns (Rust), `dotnet` (C#), `cc`/`gcc` (C), `nasm`/`ld`/`gcc` (asm). Paths below often cite **LEARN-RUST** as the first implementation reference.

---

## 1. Product goal

- **Language-first outcomes** guided by **[CURRICULUM.md](CURRICULUM.md)** (Rust-led outline; other languages **Full / Adapted / N/A** per chapter).
- **Chapter content** must satisfy **[CURRICULUM.md](CURRICULUM.md) pedagogical parity**: solutions derive output via real APIs; theory/descriptions use target-language idioms; starters scaffold the intended path (no stdout-only placeholders).
- **Hints** are **language-specific**; they should teach the target language, not the checker.
- **Solutions** must compile and produce **`expected_output`** (trimmed) under the same rules the TUI uses (see §5–§6), including documented exceptions (e.g. Rust `PASS` + `cargo test`). Passing **`check_solutions`** alone does not excuse anti-patterns listed in the curriculum.

---

## 2. Chapter JSON schema

Bundled content lives in **`chapters/<chapter_id>.json`**. Each chapter has:

| Field | Role |
|--------|------|
| `id` | Stable id (e.g. `variables`, `json`) — align with **[CURRICULUM.md](CURRICULUM.md)** canonical ids. |
| `title`, `description`, `theory` | UI copy; theory is Markdown-ish text. Must follow **[CURRICULUM.md](CURRICULUM.md) pedagogical parity** (language-appropriate, aligned with starter/solution). |
| `exercises` | Array of exercises. |
| `exercise_count` | Optional; forge sets it to `len(exercises)`. |

Each **exercise**:

| Field | Role |
|--------|------|
| `id` | Stable id (e.g. `json_01`) — stable within the course; align with **CURRICULUM.md** when sharing cross-language exercise numbering. |
| `title`, `description` | Shown in UI. |
| `starter_code` | Initial editor buffer (single “file” unless you extend the app). Scaffolds the real task per **CURRICULUM.md** (not “match stdout” stubs). |
| `expected_output` | Compared to **trimmed stdout** after a successful run (see exceptions below). |
| `hints` | List of strings; shown progressively on failed runs (TUI hint budget). |
| `solution` | Reference answer; used after hints exhausted; validated by **`scripts/check_solutions.py`** and must **derive** output per **CURRICULUM.md** (no literal echo of `expected_output`). |

**Special output token:** `expected_output` **`PASS`** means: for **test-only** snippets (Rust: `#[test]` + `cargo test`), success is **exit code 0**, not a literal stdout line `PASS`.

---

## 3. Regenerating / porting chapters

- **Legacy path (optional):** `LEARN-RUST/scripts/forge_chapters.py` can still consume upstream JSON as a **convenience** when porting; **CURRICULUM.md** is the normative target shape (prefixed filenames, language-specific depth).
- **Transform:** Python modules under **`LEARN-RUST/scripts/chapter_ports/`** export **`BUILDERS`** when the forge pipeline is used.
- **Output:** `LEARN-RUST/chapters/<prefixed_name>.json` (see **CURRICULUM.md** for ordering).

**Workflow:** align chapter JSON with **CURRICULUM.md** → run **`python3 scripts/check_solutions.py`** (see §7).

**Python:** chapter port files must be valid Python strings (do **not** use Rust-style `r#"..."#` raw delimiters in Python — they are invalid).

---

## 4. Exercise ordering

Preserve **intentional non-sequential ids** inside a chapter when pedagogy requires it (e.g. `interfaces_05`, `interfaces_07`, `interfaces_06`). Document the reason in the chapter `theory` or exercise `description` if non-obvious.

---

## 5. Execution model (Rust TUI)

Implemented in **`LEARN-RUST/src/executor.rs`** / **`LEARN-RUST/src/validator.rs`**.

**Routing (first match wins):**

1. **`#[test]` in source** → **`cargo test --quiet`** in a **temporary binary crate** with a fixed **`Cargo.toml`** (serde, serde_json, chrono, chrono-tz). Longer timeout than `rustc`.
2. Else if snippet “needs crates” heuristics → **`cargo run --quiet`** in the same temp crate:
   - `serde_json::`
   - `serde::`
   - `chrono::`
   - `chrono_tz::`
3. Else → **`rustc`** single file → run binary (std-only, fast).

**Validation:**

- If run was **`cargo test`** and expected is **`PASS`**: pass iff **exit 0** (stdout ignored).
- Else: pass iff **exit 0** and **stdout.trim() == expected_output.trim()**.

**Timeouts:** separate limits for `rustc` vs `cargo` (see code).

---

## 6. Design choices worth preserving

### Stable output

- **Maps:** use **`BTreeMap`** in solutions when **`Debug` / iteration order** must match checker text.
- **Concurrency:** avoid races in **expected stdout** (join order, sleep ordering, sort received lines, etc.).
- **Pointers:** avoid printing raw addresses; use deterministic values.

### JSON / serde

- **`serde_json::Value`** round-trip **key order** in `to_string` may **differ** from input JSON. Set **`expected_output`** to the **canonical** serialized form (or avoid `Value` string compare if you need exact input order).

### Strings / formatting

- If the exercise expects **one line** with spaces (e.g. `true true`), avoid emitting **two lines** accidentally (e.g. two `println!` calls); use one formatted line or adjust **`expected_output`** deliberately.

### Testing chapter (Rust)

- Exercises use **`#[cfg(test)]`** + **`#[test]`** + empty **`fn main() {}`** so the crate stays a **binary**.
- **`PASS`** semantics tied to **`cargo test`** (see §5).

### Time chapter (Rust)

- **Replace** non-deterministic “now + sleep” exercises with **fixed instants** + duration math where needed so CI and local checks stay reproducible.

---

## 7. Offline verification script

- **Script:** `LEARN-RUST/scripts/check_solutions.py`
- **Purpose:** Every non-empty **`solution`** compiles and matches **`expected_output`** using the **same classification** as the executor (`#[test]` / crate heuristics / `rustc`).
- **Performance:** Reuses **one** crate under **`.check-solutions-crate`** and **`CARGO_TARGET_DIR`** under **`.check-solutions-target`** (overridable via `LEARN_RUST_CHECK_CRATE` / `LEARN_RUST_CHECK_TARGET`).
- **Gitignore:** those dirs + **`target/`** + **`**/__pycache__/`**.

Run after forging or editing JSON:

```bash
python3 scripts/check_solutions.py
```

---

## 8. Tooling notes (Linux / Kali)

- **`cargo clippy`** may require **`sudo apt install rust-clippy`** when using distro `rustc`/`cargo` without rustup.
- First **`cargo run`** / check pass **compiles dependencies**; **`target/`** is large and **gitignored**.

---

## 9. Cursor / workspace (operational)

- **Multi-root:** add folders (LEARN-GO, LEARN-RUST, **LEARN-LANGUAGES**, …) and **save** a **`.code-workspace`** file to reopen the same set of roots.
- **Reopening the workspace file does not embed chat history.** Treat **this file** + per-repo **rules** as the durable “why we did X.”
- For new languages: **`@LEARN-LANGUAGES/TUTORIAL_PLATFORM.md`** plus **`@`** reference files (`LEARN-RUST/src/executor.rs`, `forge_chapters.py`, etc.) in the first prompt.

---

## 10. Porting another language (expectations)

Same **JSON schema** can drive another TUI; swap **`executor`** for:

| Language | Typical run | Friction |
|----------|-------------|----------|
| **Python** | `python3 file.py` | venv/deps; less compile-time catching. |
| **C#** | `dotnet run` on small csproj | project file + TFMs; heavier cold start. |
| **C** | `cc` / `clang` + binary | UB can “pass” stdout checks; sanitizers optional. |
| **x86-64 asm** | assembler + linker | ABI, syntax dialect, linking; grading often needs a harness, not only stdout. |

The **forge** pattern (canonical structured input + **language-specific builder** → generated JSON) still applies when you want automation, but the **canonical curriculum** lives in **CURRICULUM.md**—not necessarily any single existing repo.

---

## 11. Related files (reference: LEARN-RUST)

| Area | Path (under `LEARN-RUST/`) |
|------|----------------------------|
| Run / compile | `src/executor.rs`, `src/validator.rs` |
| Chapter load | `src/chapter.rs` |
| Forge | `scripts/forge_chapters.py`, `scripts/chapter_ports/*.py` |
| Solution CI | `scripts/check_solutions.py` |
| User-facing | `README.md` |

This **`TUTORIAL_PLATFORM.md`** is the **single canonical** platform doc; other repos should link or `@` it here rather than duplicating.
