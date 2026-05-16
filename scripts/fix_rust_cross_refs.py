#!/usr/bin/env python3
"""Remove Go cross-references and boilerplate from Rust chapter JSON."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHAPTERS = ROOT / "rust" / "chapters"

THEORY_REPLACEMENTS: dict[str, str] = {
    "variables": """## Variables in Rust

Rust binds names with `let`. Bindings are **immutable by default**; use `let mut` when the value may change.

### Bindings

```rust
let name = "Alice";
let age: i32 = 25;
```

### Basic types

Common scalar types include `i32`, `i64`, `u32`, `f64`, `bool`, `char`, and `&str` / `String`.

### Type ascription and inference

Types are often inferred; you can write them explicitly (`let x: f64 = 10.0;`).

### Shadowing

You may redeclare with `let` to shadow a name (even changing type).

### Constants

```rust
const MAX_SCORE: i32 = 100;
```

### Tuples for multiple values

```rust
let (a, b) = (5, 10);
```

Work through the exercises below to practice binding, conversion, and Rust’s zero values.
""",
    "json": """## JSON in Rust

The ecosystem standard is **`serde`** for serialization traits and **`serde_json`** for JSON text.

### Encode and decode

- `serde_json::to_string` / `to_vec` — serialize to JSON text or bytes
- `serde_json::from_str` / `from_slice` — deserialize from JSON

Derive `Serialize` and `Deserialize` on your structs, or implement the traits manually for custom shapes.

### Field attributes

Use Serde’s field attributes to control JSON shape:

- `#[serde(rename = "field")]` — emit a different key name
- `#[serde(skip_serializing_if = "Option::is_none")]` — omit `None` fields (like “omit empty” in other ecosystems)

### Streaming

For multiple JSON values in one buffer, `serde_json::Deserializer::from_str(...).into_iter::<T>()` decodes value by value without loading one giant document into memory first.
""",
    "time": """## Time in Rust

The **`chrono`** crate models calendar dates, time zones, and durations. Pair it with **`chrono_tz`** when you need named zones such as `Asia::Tokyo`.

### Building instants

- `Utc.with_ymd_and_hms(year, month, day, h, m, s)` — construct a UTC `DateTime`
- `NaiveDateTime::parse_from_str` + `.and_utc()` — parse a naive timestamp, then attach UTC

### Durations and arithmetic

- `Duration::hours`, `minutes`, `seconds`, `milliseconds` — build lengths of time
- `signed_duration_since`, `checked_add_signed` — subtract instants and add durations safely
- `num_days`, `num_hours` — read components from a `Duration`

### Deterministic exercises

Several exercises use **fixed** instants instead of the system clock so your output matches the checker on every machine. In production you would call `Utc::now()`, but fixed times keep automated grading stable.
""",
}

# (pattern, replacement) applied to description, title, hints, starter_code, solution
TEXT_RULES: list[tuple[str, str]] = [
    (r"Use the same exercise ids as the Go course for easy cross-reference\.\n?", ""),
    (r"\(mirrors Go['\u2019]s zero-value demo\)", "(each type’s default value)"),
    (r"mirrors Go['\u2019]s zero-value demo", "shows each type’s default value"),
    (r"same thresholds as Go exercise", "grade thresholds: 90+ A, 80+ B, 70+ C, 60+ D, else F"),
    (r"Same three checks as Go exercise on", "On"),
    (r"Upper then lower for `Go Programming`", "Upper then lower for `Rust Programming`"),
    (r"set only title `Go Programming`", "set only title `Rust Programming`"),
    (r"Go Programming", "Rust Programming"),
    (r"like Go `Stringer`", "using the `std::fmt::Display` trait"),
    (r"like Go['\u2019]s `fmt\.Print\(n, \" \", string\(b\)\)`", "as `5 hello` (length, space, payload)"),
    (r"\(same idea as Go['\u2019]s `fmt\.Print[^)]+\)\)", "(length, space, then UTF-8 text)"),
    (r"print like the Go type switch", "with a `match` on enum variants"),
    (r"Same as Go empty-interface slice:", "Model a heterogeneous list with"),
    (r"`\{:\.2\}` matches Go['\u2019]s default `%f` style here", "Use `println!(\"float64: {:.2}\", v)` for two decimal places"),
    (r"Same as Go: print value through reference", "Bind with `&value` and print `*r`"),
    (r"Mirror Go tags:", "Use `#[serde(rename = \"...\")]` on each field for snake_case JSON keys."),
    (r"Model Go['\u2019]s `,omitempty`", "Use `Option<T>` with `skip_serializing_if = \"Option::is_none\"`"),
    (r"to match the Go exercise\)", "in the expected JSON)"),
    (r"matching Go['\u2019]s field names", "with PascalCase JSON keys (`Street`, `City`, `Name`, `Address`)"),
    (r"match the Go JSON keys", "match the expected PascalCase JSON keys"),
    (r"same output as the Go decoder loop", "one `Name Age` line per person"),
    (r"just like Go['\u2019]s `strings\.Contains`", "with `.contains` on the error string"),
    (r"same labels as the Go exercise\)", "shown in `expected_output`)"),
    (r"in Go-style `HhMmMs`", "as `2h30m0s` (hours/minutes/seconds)"),
    (r"in Go-style hours", "as `720h0m0s`"),
    (r"from the Go exercise", "shown in `expected_output`"),
    (r"same idea as Go['\u2019]s `Before`", "compare instants with `<` and `>`"),
    (r"Go used `time\.Now` \+ `Sleep`\. Here:", "Use a fixed instant (no wall clock):"),
    (r"similar to Go['\u2019]s `time` package\)", "for calendar time and zones)"),
    (r"Go['\u2019]s `time\.Now` \+ `Sleep` exercise is replaced here with a \*\*fixed clock\*\* so your output still matches the checker when you submit\.\n?", ""),
    (r"mirror Go struct tags \(`json:\"name,omitempty\"`\)", "such as `#[serde(rename)]` and `skip_serializing_if`"),
    (r"closer to \*\*Java interfaces\*\* than to subclassing", "like interface-style contracts in many languages, but without inheritance"),
    (r"fmt_go_style", "fmt_product"),
    (r"interface\{\{\}\}", "`dyn Trait` or enums"),
]


def scrub(text: str) -> str:
    if not text:
        return text
    out = text
    for pattern, repl in TEXT_RULES:
        out = re.sub(pattern, repl, out)
    return out


def patch_chapter(path: Path) -> bool:
    data = json.loads(path.read_text(encoding="utf-8"))
    changed = False
    chapter_id = data.get("id", "")
    if chapter_id in THEORY_REPLACEMENTS and data.get("theory") != THEORY_REPLACEMENTS[chapter_id]:
        data["theory"] = THEORY_REPLACEMENTS[chapter_id]
        changed = True
    else:
        new_theory = scrub(data.get("theory", ""))
        if new_theory != data.get("theory"):
            data["theory"] = new_theory
            changed = True

    for ex in data.get("exercises", []):
        for field in ("title", "description", "starter_code", "solution", "expected_output"):
            if field not in ex:
                continue
            old = ex[field]
            if not isinstance(old, str):
                continue
            new = scrub(old)
            if new != old:
                ex[field] = new
                changed = True
        hints = ex.get("hints")
        if isinstance(hints, list):
            new_hints = [scrub(h) if isinstance(h, str) else h for h in hints]
            if new_hints != hints:
                ex["hints"] = new_hints
                changed = True

    if changed:
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return changed


def main() -> int:
    n = sum(1 for p in sorted(CHAPTERS.glob("*.json")) if patch_chapter(p))
    print(f"rust: updated {n} chapter files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
