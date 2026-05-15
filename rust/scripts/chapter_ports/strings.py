"""Port: strings — &str, char, Unicode, formatting."""

from __future__ import annotations

import copy


def build(go: dict) -> dict:
    theory = """## Strings in Rust

`&str` is an UTF-8 string slice; `String` is an owned buffer. Iterate with `chars()` for Unicode scalar values.

Formatting uses `format!` / `println!` with `{}`, `{:?}`, `{:.2}` etc.
"""

    exercises = [
        {
            "id": "strings_01",
            "title": "String literal",
            "description": "Print `Hello, Rust!`.",
            "starter_code": "fn main() {\n}\n",
            "expected_output": "Hello, Rust!",
            "hints": ['`println!("Hello, Rust!");`'],
            "solution": "fn main() {\n    println!(\"Hello, Rust!\");\n}\n",
        },
        {
            "id": "strings_02",
            "title": "char vs code point",
            "description": "Print `Character: A` then `Code Point: 65` for `'A'`.",
            "starter_code": "fn main() {\n    let ch = 'A';\n}\n",
            "expected_output": "Character: A\nCode Point: 65",
            "hints": ["`ch as u32`"],
            "solution": "fn main() {\n    let ch = 'A';\n    println!(\"Character: {}\", ch);\n    println!(\"Code Point: {}\", ch as u32);\n}\n",
        },
        {
            "id": "strings_03",
            "title": "contains / replace / split",
            "description": "Same three checks as Go exercise on `Hello, World!` and `a,b,c`.",
            "starter_code": "fn main() {\n    let text = \"Hello, World!\";\n}\n",
            "expected_output": "Contains: true\nReplaced: Hello, Rust!\nFirst: a",
            "hints": ["`contains`", "`replace`", "`split`"],
            "solution": "fn main() {\n    let text = \"Hello, World!\";\n    println!(\"Contains: {}\", text.contains(\"Hello\"));\n    let replaced = text.replace(\"World\", \"Rust\");\n    println!(\"Replaced: {}\", replaced);\n    let first = \"a,b,c\".split(',').next().unwrap();\n    println!(\"First: {}\", first);\n}\n",
        },
        {
            "id": "strings_04",
            "title": "format!",
            "description": "Print two lines: formatted name/age and `Pi is 3.14`.",
            "starter_code": "fn main() {\n    let name = \"Alice\";\n    let age = 30;\n    let pi = 3.14159_f64;\n}\n",
            "expected_output": "Alice is 30 years old\nPi is 3.14",
            "hints": ["`format!`", "`{:.2}`"],
            "solution": "fn main() {\n    let name = \"Alice\";\n    let age = 30;\n    let pi = 3.14159_f64;\n    println!(\"{} is {} years old\", name, age);\n    println!(\"Pi is {:.2}\", pi);\n}\n",
        },
        {
            "id": "strings_05",
            "title": "Case fold",
            "description": "Upper then lower for `Go Programming`.",
            "starter_code": "fn main() {\n    let s = \"Go Programming\";\n}\n",
            "expected_output": "GO PROGRAMMING\ngo programming",
            "hints": ["`to_uppercase()`", "`to_lowercase()`"],
            "solution": "fn main() {\n    let s = \"Go Programming\";\n    println!(\"{}\", s.to_uppercase());\n    println!(\"{}\", s.to_lowercase());\n}\n",
        },
        {
            "id": "strings_07",
            "title": "Reverse chars",
            "description": "Reverse `hello` by chars.",
            "starter_code": "fn main() {\n    let s = \"hello\";\n}\n",
            "expected_output": "olleh",
            "hints": ["`chars().rev().collect::<String>()`"],
            "solution": "fn main() {\n    let s = \"hello\";\n    let rev: String = s.chars().rev().collect();\n    println!(\"{}\", rev);\n}\n",
        },
        {
            "id": "strings_06",
            "title": "starts_with / ends_with",
            "description": "Print `true true` for `https://example.com` (one line, space between the two booleans).",
            "starter_code": "fn main() {\n    let url = \"https://example.com\";\n}\n",
            "expected_output": "true true",
            "hints": ["`starts_with`", "`ends_with`"],
            "solution": "fn main() {\n    let url = \"https://example.com\";\n    println!(\n        \"{} {}\",\n        url.starts_with(\"https://\"),\n        url.ends_with(\".com\")\n    );\n}\n",
        },
    ]

    out = copy.deepcopy(go)
    out["title"] = "Strings & Unicode"
    out["description"] = "Rust strings, chars, and formatting"
    out["theory"] = theory
    out["exercises"] = exercises
    out["exercise_count"] = len(exercises)
    return out
