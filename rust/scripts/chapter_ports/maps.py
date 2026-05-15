"""Port: maps — HashMap / BTreeMap."""

from __future__ import annotations

import copy


def build(go: dict) -> dict:
    theory = """## Maps in Rust

Use `std::collections::HashMap<K, V>` for average *O*(1) lookup, or `BTreeMap` for sorted keys and deterministic iteration.

### Insert / get

```rust
use std::collections::HashMap;
let mut m: HashMap<&str, i32> = HashMap::new();
m.insert("Alice", 25);
```

These exercises use `BTreeMap` where iteration or `Debug` output must be stable.
"""

    exercises = [
        {
            "id": "maps_01",
            "title": "Create map",
            "description": "Build a `BTreeMap` with `Alice -> 25`, `Bob -> 30` and print `{:?}`.",
            "starter_code": "use std::collections::BTreeMap;\n\nfn main() {\n    // let mut ages = BTreeMap::new();\n}\n",
            "expected_output": "{\"Alice\": 25, \"Bob\": 30}",
            "hints": ["`ages.insert(\"Alice\", 25);`"],
            "solution": "use std::collections::BTreeMap;\n\nfn main() {\n    let mut ages = BTreeMap::new();\n    ages.insert(\"Alice\", 25);\n    ages.insert(\"Bob\", 30);\n    println!(\"{:?}\", ages);\n}\n",
        },
        {
            "id": "maps_02",
            "title": "Lookup",
            "description": "Print the Math score from a `BTreeMap` of scores.",
            "starter_code": "use std::collections::BTreeMap;\n\nfn main() {\n    let mut scores = BTreeMap::new();\n    scores.insert(\"Math\", 95);\n    scores.insert(\"Physics\", 88);\n}\n",
            "expected_output": "95",
            "hints": ["`scores[\"Math\"]`"],
            "solution": "use std::collections::BTreeMap;\n\nfn main() {\n    let mut scores = BTreeMap::new();\n    scores.insert(\"Math\", 95);\n    scores.insert(\"Physics\", 88);\n    println!(\"{}\", scores[\"Math\"]);\n}\n",
        },
        {
            "id": "maps_03",
            "title": "Insert entries",
            "description": "Empty `BTreeMap`, insert `1 -> One`, `2 -> Two`, print Debug.",
            "starter_code": "use std::collections::BTreeMap;\n\nfn main() {\n    let mut names: BTreeMap<&str, &str> = BTreeMap::new();\n}\n",
            "expected_output": "{\"1\": \"One\", \"2\": \"Two\"}",
            "hints": ["`names.insert(\"1\", \"One\");`"],
            "solution": "use std::collections::BTreeMap;\n\nfn main() {\n    let mut names: BTreeMap<&str, &str> = BTreeMap::new();\n    names.insert(\"1\", \"One\");\n    names.insert(\"2\", \"Two\");\n    println!(\"{:?}\", names);\n}\n",
        },
        {
            "id": "maps_04",
            "title": "Remove",
            "description": "Remove key `b` from map `a,b,c` and print Debug.",
            "starter_code": "use std::collections::BTreeMap;\n\nfn main() {\n    let mut data = BTreeMap::new();\n    data.insert(\"a\", 1);\n    data.insert(\"b\", 2);\n    data.insert(\"c\", 3);\n}\n",
            "expected_output": "{\"a\": 1, \"c\": 3}",
            "hints": ["`data.remove(\"b\");`"],
            "solution": "use std::collections::BTreeMap;\n\nfn main() {\n    let mut data = BTreeMap::new();\n    data.insert(\"a\", 1);\n    data.insert(\"b\", 2);\n    data.insert(\"c\", 3);\n    data.remove(\"b\");\n    println!(\"{:?}\", data);\n}\n",
        },
        {
            "id": "maps_05",
            "title": "Key presence",
            "description": "If `bananas` missing from inventory print `not found`.",
            "starter_code": "use std::collections::BTreeMap;\n\nfn main() {\n    let mut inventory = BTreeMap::new();\n    inventory.insert(\"apples\", 5);\n    inventory.insert(\"oranges\", 3);\n}\n",
            "expected_output": "not found",
            "hints": ["`inventory.get(\"bananas\")`"],
            "solution": "use std::collections::BTreeMap;\n\nfn main() {\n    let mut inventory = BTreeMap::new();\n    inventory.insert(\"apples\", 5);\n    inventory.insert(\"oranges\", 3);\n    if inventory.contains_key(\"bananas\") {\n        println!(\"exists\");\n    } else {\n        println!(\"not found\");\n    }\n}\n",
        },
        {
            "id": "maps_07",
            "title": "Length",
            "description": "Print `len()` of three-entry map.",
            "starter_code": "use std::collections::BTreeMap;\n\nfn main() {\n    let counts = BTreeMap::from([(\"one\", 1), (\"two\", 2), (\"three\", 3)]);\n}\n",
            "expected_output": "3",
            "hints": ["`counts.len()`"],
            "solution": "use std::collections::BTreeMap;\n\nfn main() {\n    let counts = BTreeMap::from([(\"one\", 1), (\"two\", 2), (\"three\", 3)]);\n    println!(\"{}\", counts.len());\n}\n",
        },
        {
            "id": "maps_06",
            "title": "Iterate",
            "description": "Print each `key value` on its own line for grades map (BTree order).",
            "starter_code": "use std::collections::BTreeMap;\n\nfn main() {\n    let grades = BTreeMap::from([(\"A\", 90), (\"B\", 80), (\"C\", 70)]);\n}\n",
            "expected_output": "A 90\nB 80\nC 70",
            "hints": ["`for (k, v) in &grades`"],
            "solution": "use std::collections::BTreeMap;\n\nfn main() {\n    let grades = BTreeMap::from([(\"A\", 90), (\"B\", 80), (\"C\", 70)]);\n    for (k, v) in &grades {\n        println!(\"{} {}\", k, v);\n    }\n}\n",
        },
    ]

    out = copy.deepcopy(go)
    out["description"] = "Hash maps and ordered maps in Rust"
    out["theory"] = theory
    out["exercises"] = exercises
    out["exercise_count"] = len(exercises)
    return out
