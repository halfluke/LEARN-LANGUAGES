"""Port: arrays — fixed-size [T; N] in Rust."""

from __future__ import annotations

import copy


def build(go: dict) -> dict:
    theory = """## Arrays in Rust

A fixed-size array has type `[T; N]` (for example `[i32; 5]`). The length is part of the type.

### Creating arrays

```rust
let zeros = [0_i32; 5];
let arr = [1, 2, 3, 4, 5];
```

### Iteration

```rust
for v in arr { println!("{}", v); }
```

### Multidimensional

```rust
let m = [[1, 2], [3, 4]];
```

`println!("{:?}", arr)` uses `Debug` formatting (includes commas), which is what these exercises expect.
"""

    exercises = [
        {
            "id": "arrays_01",
            "title": "Create array",
            "description": "Create `[1, 2, 3, 4, 5]` and print it with Debug formatting.",
            "starter_code": "fn main() {\n    // let arr = [1, 2, 3, 4, 5];\n}\n",
            "expected_output": "[1, 2, 3, 4, 5]",
            "hints": ["`let arr = [1, 2, 3, 4, 5];`", '`println!("{:?}", arr);`'],
            "solution": "fn main() {\n    let arr = [1, 2, 3, 4, 5];\n    println!(\"{:?}\", arr);\n}\n",
        },
        {
            "id": "arrays_02",
            "title": "Iterate array",
            "description": "Create `[10, 20, 30]` and print each element on its own line.",
            "starter_code": "fn main() {\n    let nums = [10, 20, 30];\n    // for ...\n}\n",
            "expected_output": "10\n20\n30",
            "hints": ["`for n in nums {`", '`println!("{}", n);`'],
            "solution": "fn main() {\n    let nums = [10, 20, 30];\n    for n in nums {\n        println!(\"{}\", n);\n    }\n}\n",
        },
        {
            "id": "arrays_03",
            "title": "Array length",
            "description": "Create `[1, 2, 3, 4]` and print `.len()`.",
            "starter_code": "fn main() {\n    let arr = [1, 2, 3, 4];\n}\n",
            "expected_output": "4",
            "hints": ["`arr.len()`"],
            "solution": "fn main() {\n    let arr = [1, 2, 3, 4];\n    println!(\"{}\", arr.len());\n}\n",
        },
        {
            "id": "arrays_04",
            "title": "Partial initialization",
            "description": "Create `[10, 20, 0, 0, 0]` using `[10, 20, 0, 0, 0]` literal and print Debug.",
            "starter_code": "fn main() {\n    // let arr = [10, 20, 0, 0, 0];\n}\n",
            "expected_output": "[10, 20, 0, 0, 0]",
            "hints": ["Trailing zeros can be written explicitly."],
            "solution": "fn main() {\n    let arr = [10, 20, 0, 0, 0];\n    println!(\"{:?}\", arr);\n}\n",
        },
        {
            "id": "arrays_05",
            "title": "2D array",
            "description": "Print `1`, `2`, `3`, `4` each on its own line from `[[1,2],[3,4]]`.",
            "starter_code": "fn main() {\n    let m = [[1, 2], [3, 4]];\n}\n",
            "expected_output": "1\n2\n3\n4",
            "hints": ["Nested `for` rows then values."],
            "solution": "fn main() {\n    let m = [[1, 2], [3, 4]];\n    for row in m {\n        for v in row {\n            println!(\"{}\", v);\n        }\n    }\n}\n",
        },
        {
            "id": "arrays_07",
            "title": "Sum array",
            "description": "Sum `[10, 20, 30, 40, 50]` and print the total.",
            "starter_code": "fn main() {\n    let arr = [10, 20, 30, 40, 50];\n}\n",
            "expected_output": "150",
            "hints": ["`let mut s = 0;` then add in loop."],
            "solution": "fn main() {\n    let arr = [10, 20, 30, 40, 50];\n    let mut s = 0;\n    for v in arr {\n        s += v;\n    }\n    println!(\"{}\", s);\n}\n",
        },
        {
            "id": "arrays_06",
            "title": "Index access",
            "description": "From `[100, 200, 300]` print first and last with spaces.",
            "starter_code": "fn main() {\n    let arr = [100, 200, 300];\n}\n",
            "expected_output": "100 300",
            "hints": ["`arr[0]` and `arr[2]`"],
            "solution": "fn main() {\n    let arr = [100, 200, 300];\n    println!(\"{} {}\", arr[0], arr[2]);\n}\n",
        },
    ]

    out = copy.deepcopy(go)
    out["description"] = "Fixed-size arrays `[T; N]` in Rust"
    out["theory"] = theory
    out["exercises"] = exercises
    out["exercise_count"] = len(exercises)
    return out
