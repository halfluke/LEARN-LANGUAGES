#!/usr/bin/env python3
"""Generate LEARN-RUST chapter JSON (same schema as LEARN-GO)."""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "chapters"

CHAPTERS = [
    (
        "arrays",
        "Arrays",
        "Fixed-size arrays [T; N] and when to use them",
        "## Arrays in Rust\n\nArrays `[T; N]` live on the stack and have a fixed length known at compile time.\n\nUse arrays for small, fixed collections; prefer `Vec` for dynamic length.",
    ),
    (
        "concurrency",
        "Concurrency",
        "Threads, message passing, and shared state",
        "## Concurrency\n\nRust uses threads (`std::thread`) and channels (`std::sync::mpsc`) for safe message passing.\n\nThe type system helps avoid data races at compile time.",
    ),
    (
        "controlflow",
        "Control Flow",
        "if / loop / while / for and pattern matching basics",
        "## Control flow\n\nRust has `if` expressions, `loop`, `while`, `for`, and `match`.\n\n`if` can return a value; `match` must be exhaustive.",
    ),
    (
        "errors",
        "Error Handling",
        "Result, Option, ?, and recoverable errors",
        "## Errors\n\nUse `Result<T, E>` for recoverable errors and the `?` operator to propagate them.\n\n`Option<T>` models absence without null pointers.",
    ),
    (
        "functions",
        "Functions",
        "fn, parameters, return types, and closures intro",
        "## Functions\n\nDefine functions with `fn name(args) -> ReturnType { ... }`.\n\nStatements vs expressions: the last expression can be the return value without `return`.",
    ),
    (
        "interfaces",
        "Traits",
        "Rust traits vs Go interfaces: shared behavior",
        "## Traits\n\nTraits describe behavior types can implement, similar in spirit to Go interfaces.\n\nUse `dyn Trait` for trait objects; generics monomorphize at compile time.",
    ),
    (
        "json",
        "JSON & serde",
        "Serialize and deserialize with serde_json",
        "## JSON\n\nThe ecosystem typically uses `serde` + `serde_json`.\n\nThis course uses `println!` exercises; in real projects you derive `Serialize`/`Deserialize`.",
    ),
    (
        "maps",
        "Hash Maps",
        "std::collections::HashMap",
        "## HashMap\n\n`HashMap<K, V>` stores key-value pairs with amortized O(1) lookup.\n\nKeys must implement `Eq` and `Hash`.",
    ),
    (
        "methods",
        "Methods & impl",
        "impl blocks, self, and associated functions",
        "## Methods\n\nImplement methods with `impl Type { fn method(&self, ...) }`.\n\n`self`, `&self`, and `&mut self` mirror Go receiver styles.",
    ),
    (
        "packages",
        "Modules & Crates",
        "mod, use, crate, and the module tree",
        "## Modules\n\n`mod` declares modules; `use` brings paths into scope.\n\nA binary crate has `fn main` in `src/main.rs` or `src/bin/*.rs`.",
    ),
    (
        "pointers",
        "References & Ownership",
        "Ownership, borrowing, and lifetimes overview",
        "## References\n\nRust tracks ownership and borrowing at compile time.\n\n`&T` is an immutable reference; `&mut T` is unique and mutable.",
    ),
    (
        "slices",
        "Slices",
        "&[T] views into contiguous sequences",
        "## Slices\n\nA slice `&[T]` is a fat pointer (pointer + length) into an array or `Vec`.\n\nString slices `&str` are UTF-8 byte views.",
    ),
    (
        "strings",
        "Strings & str",
        "String vs &str, formatting, and UTF-8",
        "## Strings\n\n`String` is an owned, growable UTF-8 buffer.\n\n`&str` is a borrowed string slice; string literals have type `&str`.",
    ),
    (
        "structs",
        "Structs",
        "Named fields, tuple structs, and struct update syntax",
        "## Structs\n\nStructs group related data with named fields or tuple-like layouts.\n\n`..` syntax can fill remaining fields from another value.",
    ),
    (
        "testing",
        "Testing",
        "#[test], assert!, and cargo test",
        "## Testing\n\nMark tests with `#[test]` and run them with `cargo test`.\n\nUse `assert!`, `assert_eq!`, and `Result` in tests.",
    ),
    (
        "time",
        "Time",
        "std::time for durations and instants (conceptual)",
        "## Time\n\n`std::time::Instant` and `Duration` model elapsed time.\n\nWall clocks need a crate like `chrono` in real apps.",
    ),
    (
        "variables",
        "Variables & Types",
        "let, mut, type annotations, and shadowing",
        "## Variables\n\nBind names with `let`; add `mut` for rebinding the value.\n\nType annotations look like `let x: i32 = 0;`",
    ),
]


def ex(cid: str, n: int, title: str, desc: str, starter: str, out: str, hints: list[str], sol: str):
    return {
        "id": f"{cid}_{n:02d}",
        "title": title,
        "description": desc,
        "starter_code": starter,
        "expected_output": out,
        "hints": hints,
        "solution": sol,
    }


def exercises_for(ch_id: str, title_word: str):
    """Four small println exercises per chapter (starter templates compile)."""
    tw = title_word
    return [
        ex(
            ch_id,
            1,
            f"Print a greeting ({tw})",
            "Print the line `hello` exactly (no extra spaces or lines).",
            "fn main() {\n    // println!(...)\n}\n",
            "hello",
            ["Use println!(\"hello\");"],
            "fn main() {\n    println!(\"hello\");\n}\n",
        ),
        ex(
            ch_id,
            2,
            f"Print a number ({tw})",
            "Print the integer `42` on its own line.",
            "fn main() {\n    // print 42\n}\n",
            "42",
            ["Use println!(\"{}\", 42); or println!(42);"],
            "fn main() {\n    println!(\"{}\", 42);\n}\n",
        ),
        ex(
            ch_id,
            3,
            f"Two lines ({tw})",
            "Print `a` then `b` on separate lines in that order.",
            "fn main() {\n}\n",
            "a\nb",
            ["Call println! twice."],
            "fn main() {\n    println!(\"a\");\n    println!(\"b\");\n}\n",
        ),
        ex(
            ch_id,
            4,
            f"Sum literal ({tw})",
            "Print the result of 7 + 5 (should be `12`).",
            "fn main() {\n}\n",
            "12",
            ["println!(\"{}\", 7 + 5);"],
            "fn main() {\n    println!(\"{}\", 7 + 5);\n}\n",
        ),
    ]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for cid, title, desc, theory in CHAPTERS:
        chapter = {
            "id": cid,
            "title": title,
            "description": desc,
            "theory": theory,
            "exercises": exercises_for(cid, title.split()[0]),
        }
        path = OUT / f"{cid}.json"
        path.write_text(json.dumps(chapter, indent=2) + "\n", encoding="utf-8")
        print("wrote", path)


if __name__ == "__main__":
    main()
