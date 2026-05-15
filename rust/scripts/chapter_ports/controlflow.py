"""Port: controlflow — if, loop, match."""

from __future__ import annotations

import copy


def build(go: dict) -> dict:
    theory = """## Control flow in Rust

Rust has `if` **expressions**, `loop`, `while`, `for`, and **`match`** (exhaustive pattern matching, similar in spirit to `switch` but safer).

### `if`

```rust
let age = 20;
if age >= 18 {
    println!("Adult");
} else {
    println!("Minor");
}
```

### `match`

```rust
match day {
    1 => println!("Monday"),
    2 => println!("Tuesday"),
    _ => println!("Other"),
}
```

### Loops

`for i in 1..=5 { }`, `while cond { }`, `loop { break; }`.
"""

    exercises = [
        {
            "id": "controlflow_01",
            "title": "If expression",
            "description": "`age = 20`; print `Adult` if `>= 18` else `Minor`.",
            "starter_code": "fn main() {\n    let age = 20;\n}\n",
            "expected_output": "Adult",
            "hints": ["`if age >= 18 { ... } else { ... }`"],
            "solution": "fn main() {\n    let age = 20;\n    if age >= 18 {\n        println!(\"Adult\");\n    } else {\n        println!(\"Minor\");\n    }\n}\n",
        },
        {
            "id": "controlflow_02",
            "title": "For range",
            "description": "Print 1 through 5 inclusive, one per line.",
            "starter_code": "fn main() {\n    // for i in 1..=5\n}\n",
            "expected_output": "1\n2\n3\n4\n5",
            "hints": ["`for i in 1..=5`"],
            "solution": "fn main() {\n    for i in 1..=5 {\n        println!(\"{}\", i);\n    }\n}\n",
        },
        {
            "id": "controlflow_03",
            "title": "Match day",
            "description": "`day = 2`; match to print `Tuesday` for 2 (also arms 1,3, default `Unknown`).",
            "starter_code": "fn main() {\n    let day = 2;\n    // match day { ... }\n}\n",
            "expected_output": "Tuesday",
            "hints": ["`match day { 1 => ..., 2 => ..., _ => ... }`"],
            "solution": "fn main() {\n    let day = 2;\n    match day {\n        1 => println!(\"Monday\"),\n        2 => println!(\"Tuesday\"),\n        3 => println!(\"Wednesday\"),\n        _ => println!(\"Unknown\"),\n    }\n}\n",
        },
        {
            "id": "controlflow_04",
            "title": "For over vec",
            "description": "Iterate `[\"red\",\"green\",\"blue\"]` and print each color.",
            "starter_code": "fn main() {\n    let colors = vec![\"red\", \"green\", \"blue\"];\n}\n",
            "expected_output": "red\ngreen\nblue",
            "hints": ["`for c in colors`"],
            "solution": "fn main() {\n    let colors = vec![\"red\", \"green\", \"blue\"];\n    for c in colors {\n        println!(\"{}\", c);\n    }\n}\n",
        },
        {
            "id": "controlflow_05",
            "title": "Grade chain",
            "description": "`score = 85` print `A`/`B`/… same thresholds as Go exercise.",
            "starter_code": "fn main() {\n    let score = 85;\n}\n",
            "expected_output": "B",
            "hints": ["chain `if / else if`"],
            "solution": "fn main() {\n    let score = 85;\n    let grade = if score >= 90 {\n        \"A\"\n    } else if score >= 80 {\n        \"B\"\n    } else if score >= 70 {\n        \"C\"\n    } else if score >= 60 {\n        \"D\"\n    } else {\n        \"F\"\n    };\n    println!(\"{}\", grade);\n}\n",
        },
        {
            "id": "controlflow_07",
            "title": "Loop with break",
            "description": "Print 1..4 using `loop` and `break` when reaching 5.",
            "starter_code": "fn main() {\n    let mut i = 1;\n    loop {\n        // ...\n    }\n}\n",
            "expected_output": "1\n2\n3\n4",
            "hints": ["`if i >= 5 { break; }`"],
            "solution": "fn main() {\n    let mut i = 1;\n    loop {\n        if i >= 5 {\n            break;\n        }\n        println!(\"{}\", i);\n        i += 1;\n    }\n}\n",
        },
        {
            "id": "controlflow_06",
            "title": "Continue",
            "description": "Print odd numbers 1..=10 one per line.",
            "starter_code": "fn main() {\n    for i in 1..=10 {\n        // ...\n    }\n}\n",
            "expected_output": "1\n3\n5\n7\n9",
            "hints": ["`if i % 2 == 0 { continue; }`"],
            "solution": "fn main() {\n    for i in 1..=10 {\n        if i % 2 == 0 {\n            continue;\n        }\n        println!(\"{}\", i);\n    }\n}\n",
        },
    ]

    out = copy.deepcopy(go)
    out["description"] = "if / loop / while / for / match in Rust"
    out["theory"] = theory
    out["exercises"] = exercises
    out["exercise_count"] = len(exercises)
    return out
