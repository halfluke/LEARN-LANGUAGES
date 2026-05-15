# LEARN-* shared curriculum (Rust-led)

**Normative source:** this document defines **chapter themes**, **canonical chapter ids**, and **per-language coverage**. The JSON schema remains in [TUTORIAL_PLATFORM.md](TUTORIAL_PLATFORM.md).

**Non-normative:** historical “match LEARN-GO exercise-for-exercise” parity. Language repos may differ in **exercise count** and **wording** as long as outcomes for their column are met.

## Canonical chapter order (filenames)

Chapters load from `chapters/*.json` sorted by **filename**. Use prefixed names so **teaching order** is stable:

| # | Filename stem | `id` inside JSON | Focus |
|---|----------------|------------------|--------|
| 01 | `01_variables` | `variables` | bindings, types, printing |
| 02 | `02_ownership` | `ownership` | moves, copies, ownership (Rust); value/reference semantics (others) |
| 03 | `03_controlflow` | `controlflow` | branches, loops |
| 04 | `04_functions` | `functions` | functions, parameters, returns |
| 05 | `05_lifetimes` | `lifetimes` | lifetimes & borrowing depth (Rust); scope/RAII analogues where adapted |
| 06 | `06_arrays` | `arrays` | fixed-size aggregate |
| 07 | `07_slices` | `slices` | slices / views / `Span`-like ideas |
| 08 | `08_maps` | `maps` | associative containers |
| 09 | `09_strings` | `strings` | text, encoding, formatting |
| 10 | `10_structs` | `structs` | user-defined types |
| 11 | `11_interfaces` | `interfaces` | polymorphism (Go/Java-style interfaces; Rust traits; C# interfaces) |
| 12 | `12_methods` | `methods` | methods / receivers |
| 13 | `13_packages` | `packages` | modules, visibility, build layout |
| 14 | `14_pointers` | `pointers` | memory, references, unsafe/near-metal topics as appropriate |
| 15 | `15_errors` | `errors` | errors / `Result` / exceptions by language |
| 16 | `16_concurrency` | `concurrency` | threads / goroutines / async intro as appropriate |
| 17 | `17_testing` | `testing` | tests, tables, harness |
| 18 | `18_json` | `json` | parsing/serializing structured data |
| 19 | `19_time` | `time` | time and durations |

## Coverage matrix (v1 scope)

Legend: **Full** = first-class chapter in that language. **Adapted** = same slot, different emphasis (still real exercises). **N/A** = no dedicated chapter file; topic folded elsewhere or out of v1.

| id | Rust | Go | C# | C | Python | Java | Asm (ELF64 / NASM) |
|----|------|----|----|----|--------|------|---------------------|
| variables | Full | Full | Full | Full | Full | Full | Adapted (syscalls / libc only) |
| ownership | Full | Adapted | Adapted | Adapted | Adapted | Adapted | N/A |
| controlflow | Full | Full | Full | Full | Full | Full | Adapted (branch/jump) |
| functions | Full | Full | Full | Full | Full | Full | Adapted (calls, ABI preview) |
| lifetimes | Full | N/A | N/A | N/A | N/A | N/A | N/A |
| arrays | Full | Full | Full | Full | Full | Full | Adapted |
| slices | Full | Full | Full | Adapted | Full | Adapted | Adapted |
| maps | Full | Full | Full | Adapted | Full | Full | N/A |
| strings | Full | Full | Full | Full | Full | Full | Adapted |
| structs | Full | Full | Full | Full | Full | Full | Adapted |
| interfaces | Full | Full | Full | Adapted | Full | Full | N/A |
| methods | Full | Full | Full | Adapted | Full | Full | Adapted |
| packages | Full | Full | Full | N/A | Adapted | Adapted | N/A |
| pointers | Full | Adapted | Adapted | Full | Adapted | Adapted | Full |
| errors | Full | Full | Full | Adapted | Full | Full | N/A |
| concurrency | Full | Full | Full | Adapted | Full | Full | Adapted |
| testing | Full | Full | Full | Adapted | Adapted | Adapted | N/A |
| json | Full | Full | Full | Adapted | Full | Adapted | N/A |
| time | Full | Full | Full | Adapted | Full | Full | N/A |

## Pedagogical parity (normative)

**Pedagogical parity** means: for each shared exercise **`id`**, a learner who reads the chapter and completes the exercise practices the **same skill** as in the reference track (Rust-led themes), using **that language’s normal tools**—not another language’s vocabulary, and not merely reproducing golden stdout.

This applies to **solution code**, **descriptions / theory**, and **starters**. It is required for **merged** chapter JSON in every LEARN-* repo, alongside mechanical checks (`scripts/check_solutions.py`, language test harnesses).

### Solution code

Solutions must **derive** `expected_output` by running the mechanism the exercise teaches.

| Required | Forbidden (anti-patterns) |
|----------|---------------------------|
| Use idiomatic APIs for the language and chapter (**Full** or **Adapted** depth). | Printing or `fwrite`ing a **literal copy** of `expected_output` (or a near-copy) with no real computation, parsing, or I/O. |
| Match **trimmed stdout** (and any documented exceptions, e.g. Rust `PASS` + `cargo test`). | “Cheating” the checker: hard-coded answers, dead code paths, or stubs that only exist to pass CI. |
| Stay within the repo’s **execution model** (single file unless the language README documents otherwise; no undeclared third-party deps). | Copy-pasting the reference language’s solution with syntax edits only. |

**Adapted** chapters still require real code: e.g. C `json` may use `snprintf` and hand parsing instead of `serde`, but must still **build or parse** JSON-shaped text; C `time` must use **`time.h`** (or documented equivalents), not echo a fixed timestamp string.

**Asm** solutions use NASM + syscalls/libc as documented; parity is “same skill, assembly-level mechanism,” not identical exercise count to Rust.

### Descriptions and theory

Chapter **`theory`** and per-exercise **`description`** / **`title`** must read as **this language’s course**, not a port label.

| Required | Forbidden (anti-patterns) |
|----------|---------------------------|
| Name the language’s types, libraries, and idioms (`pthread`, `System.Text.Json`, `encoding/json`, `syscall`, …). | Leftover reference-track wording (`serde`, `chrono::`, `goroutine`, `Span`, …) unless explicitly called out as “Rust/Go uses X; here you use Y”. |
| For **Adapted** slots, state what is emphasized or simplified vs **Full** (e.g. “no time zones in v1”). | Instructions that say only “match expected stdout” or “print the answer”. |
| Align with what **starters** and **solutions** actually do. | Theory that describes APIs the starter/solution never uses. |

Shared exercise **`id`**s may keep **comparable outcomes** (same lines on stdout) while wording differs per language.

### Starters (`starter_code`)

Starters scaffold the **intended solution path**, not a blank comment that implies guessing the checker output.

| Required | Forbidden (anti-patterns) |
|----------|---------------------------|
| Includes correct **includes/imports**, section layout, or function shells for the task. | Empty `main` with only `/* Match expected stdout */` (or equivalent). |
| Leaves clear **holes** where the learner writes the skill (syscall args, loop body, format string, …). | A full working solution (that belongs in `solution`, revealed after hints). |
| Matches the **description** and **hints** (same registers, APIs, data layout). | Starter that teaches a different approach than the reference solution (e.g. libc `printf` starter but syscall-only solution) without saying so in the text. |

Hints remain **language-specific** and should point at real APIs, not at stdout shape alone (see [TUTORIAL_PLATFORM.md](TUTORIAL_PLATFORM.md)).

### CI (continuous integration)

Automated **`check_solutions`** (and language tests) verify **correctness** only. **Pedagogical parity** is a **content** requirement: reviewers and contributors enforce it when editing chapter JSON; optional lint scripts may be added later to catch obvious echo solutions.

A change that passes CI but violates this section is **not** curriculum-complete.

## Assessment (v1)

All LEARN-* v1 apps grade **trimmed stdout** (plus special cases documented per language, e.g. Rust `PASS` + `cargo test`). Topics that deserve richer grading (register state, sanitizer output) are flagged for **future harnesses**—see per-language README security notes.

## Progress migration

Chapter and exercise **ids** may change during realignment. Older `progress.json` entries may no longer match; learners should expect **stale progress** until a migration tool exists. Do not block curriculum fixes on silent migration.

## Porting workflow

When adding or refreshing a language repo:

1. Align **filename**, chapter **`id`**, and exercise **`id`**s with this document.
2. Author **theory**, **descriptions**, **starters**, and **solutions** to meet **Pedagogical parity** above—not stdout-only placeholders.
3. Run **`python3 scripts/check_solutions.py`** (and any language-specific tests) before merge.

Legacy chapters that still use echo solutions should be tracked and updated; do not add new exercises that rely on literal stdout copying.
