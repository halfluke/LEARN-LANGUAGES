"""Port: slices — Vec and slice operations."""

from __future__ import annotations

import copy


def build(go: dict) -> dict:
    theory = """## Slices and `Vec` in Rust

A `Vec<T>` owns a growable buffer. A slice `&[T]` is a borrowed view.

### Creating

```rust
let mut v = vec![1, 2, 3];
v.push(4);
```

### Length and capacity

```rust
v.len();
v.capacity();
```

### Slicing

```rust
let s = &v[1..4]; // indices 1..3 inclusive-exclusive
```

### Copying

`v.clone()` duplicates data; `copy_from_slice` copies between same-length slices.

Debug-printing a `Vec` uses `{:?}` (comma-separated), matching these exercises.
"""

    exercises = [
        {
            "id": "slices_01",
            "title": "Create vector",
            "description": "Make a `Vec<i32>` of length 3 with values 1,2,3 and print it with `{:?}`.",
            "starter_code": "fn main() {\n    // let mut v = vec![0; 3];\n}\n",
            "expected_output": "[1, 2, 3]",
            "hints": ["`let mut v = vec![0; 3];` then assign indices", "Or `vec![1,2,3]`"],
            "solution": "fn main() {\n    let v = vec![1, 2, 3];\n    println!(\"{:?}\", v);\n}\n",
        },
        {
            "id": "slices_02",
            "title": "Push elements",
            "description": "Start with `vec![1,2]`, push `3`, `4`, `5`, print `{:?}`.",
            "starter_code": "fn main() {\n    let mut v = vec![1, 2];\n}\n",
            "expected_output": "[1, 2, 3, 4, 5]",
            "hints": ["`v.push(3);` etc."],
            "solution": "fn main() {\n    let mut v = vec![1, 2];\n    v.push(3);\n    v.push(4);\n    v.push(5);\n    println!(\"{:?}\", v);\n}\n",
        },
        {
            "id": "slices_03",
            "title": "Length and capacity",
            "description": "`Vec` with `with_capacity(10)` then `resize(3, 0)` — print len and capacity.",
            "starter_code": "fn main() {\n    let mut v = Vec::with_capacity(10);\n    v.resize(3, 0);\n}\n",
            "expected_output": "3 10",
            "hints": ["`v.len()`, `v.capacity()`"],
            "solution": "fn main() {\n    let mut v = Vec::with_capacity(10);\n    v.resize(3, 0);\n    println!(\"{} {}\", v.len(), v.capacity());\n}\n",
        },
        {
            "id": "slices_04",
            "title": "Slice length",
            "description": "Create `vec![\"apple\", \"banana\", \"cherry\"]` and print `len()`.",
            "starter_code": "fn main() {\n    let fruits = vec![\"apple\", \"banana\", \"cherry\"];\n}\n",
            "expected_output": "3",
            "hints": ["`fruits.len()`"],
            "solution": "fn main() {\n    let fruits = vec![\"apple\", \"banana\", \"cherry\"];\n    println!(\"{}\", fruits.len());\n}\n",
        },
        {
            "id": "slices_05",
            "title": "Slicing",
            "description": "From `1..=5` collect to vec, slice to middle `[2,3,4]` via `&v[1..4]`, print `{:?}`.",
            "starter_code": "fn main() {\n    let v: Vec<i32> = (1..=5).collect();\n}\n",
            "expected_output": "[2, 3, 4]",
            "hints": ["`&v[1..4]`"],
            "solution": "fn main() {\n    let v: Vec<i32> = (1..=5).collect();\n    let s = &v[1..4];\n    println!(\"{:?}\", s);\n}\n",
        },
        {
            "id": "slices_07",
            "title": "Extend slice",
            "description": "`a = [1,2]`, `b = [3,4,5]`, extend `a` with `b` and print `a`.",
            "starter_code": "fn main() {\n    let mut a = vec![1, 2];\n    let b = vec![3, 4, 5];\n}\n",
            "expected_output": "[1, 2, 3, 4, 5]",
            "hints": ["`a.extend(b);`"],
            "solution": "fn main() {\n    let mut a = vec![1, 2];\n    let b = vec![3, 4, 5];\n    a.extend(b);\n    println!(\"{:?}\", a);\n}\n",
        },
        {
            "id": "slices_06",
            "title": "Clone then append",
            "description": "Clone `vec![1,2,3]`, push `4` on clone, print original then clone (two lines).",
            "starter_code": "fn main() {\n    let original = vec![1, 2, 3];\n}\n",
            "expected_output": "[1, 2, 3]\n[1, 2, 3, 4]",
            "hints": ["`let mut c = original.clone();`"],
            "solution": "fn main() {\n    let original = vec![1, 2, 3];\n    let mut c = original.clone();\n    c.push(4);\n    println!(\"{:?}\", original);\n    println!(\"{:?}\", c);\n}\n",
        },
    ]

    out = copy.deepcopy(go)
    out["description"] = "Vectors, slices, len/cap, and borrowing in Rust"
    out["theory"] = theory
    out["exercises"] = exercises
    out["exercise_count"] = len(exercises)
    return out
