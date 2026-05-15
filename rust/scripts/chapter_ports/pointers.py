"""Port: pointers — references, mut pointers, Box."""

from __future__ import annotations

import copy


def build(go: dict) -> dict:
    theory = """## References in Rust

Rust uses `&T` and `&mut T` instead of Go pointers for safe aliasing rules.

`Box<T>` allocates on the heap when you need owned indirection.

**Note:** Exercise 1 prints the **value** through a reference (addresses are not stable for automated checks).
"""

    exercises = [
        {
            "id": "pointers_01",
            "title": "Borrow and read",
            "description": "`x = 42`, `r = &x`, print `*r` (dereference).",
            "starter_code": "fn main() {\n    let x = 42;\n    // let r = &x;\n}\n",
            "expected_output": "42",
            "hints": ["`*r`"],
            "solution": "fn main() {\n    let x = 42;\n    let r = &x;\n    println!(\"{}\", *r);\n}\n",
        },
        {
            "id": "pointers_02",
            "title": "Dereference",
            "description": "Same as Go: print value through reference.",
            "starter_code": "fn main() {\n    let value = 100;\n}\n",
            "expected_output": "100",
            "hints": ["`let r = &value;`"],
            "solution": "fn main() {\n    let value = 100;\n    let r = &value;\n    println!(\"{}\", *r);\n}\n",
        },
        {
            "id": "pointers_03",
            "title": "Mutate through mut ref",
            "description": "`modify(p: &mut i32)` doubles value; print after.",
            "starter_code": "fn modify(_p: &mut i32) {}\n\nfn main() {\n    let mut num = 5;\n}\n",
            "expected_output": "10",
            "hints": ["`*p *= 2;`"],
            "solution": "fn modify(p: &mut i32) {\n    *p *= 2;\n}\n\nfn main() {\n    let mut num = 5;\n    modify(&mut num);\n    println!(\"{}\", num);\n}\n",
        },
        {
            "id": "pointers_04",
            "title": "Box allocation",
            "description": "`Box::new` an `i32`, set to 99, print dereferenced.",
            "starter_code": "fn main() {\n}\n",
            "expected_output": "99",
            "hints": ["`let mut b = Box::new(0);`"],
            "solution": "fn main() {\n    let mut b = Box::new(0);\n    *b = 99;\n    println!(\"{}\", *b);\n}\n",
        },
        {
            "id": "pointers_05",
            "title": "Struct through reference",
            "description": "`Person { name }` via `&mut` set to Bob, print name.",
            "starter_code": "struct Person {\n    name: String,\n}\n\nfn main() {\n}\n",
            "expected_output": "Bob",
            "hints": ["`p.name = \"Bob\".into();`"],
            "solution": "struct Person {\n    name: String,\n}\n\nfn main() {\n    let mut p = Person {\n        name: String::new(),\n    };\n    p.name = \"Bob\".into();\n    println!(\"{}\", p.name);\n}\n",
        },
        {
            "id": "pointers_07",
            "title": "Option None",
            "description": "Print `nil` equivalent: Rust uses `Option` — print `none` when `None`.",
            "starter_code": "fn main() {\n    let o: Option<i32> = None;\n}\n",
            "expected_output": "nil",
            "hints": ["`match o { None => ...`"],
            "solution": "fn main() {\n    let o: Option<i32> = None;\n    match o {\n        None => println!(\"nil\"),\n        Some(v) => println!(\"{}\", v),\n    }\n}\n",
        },
        {
            "id": "pointers_06",
            "title": "Swap via references",
            "description": "`swap(a: &mut i32, b: &mut i32)` then print `x y`.",
            "starter_code": "fn swap(_a: &mut i32, _b: &mut i32) {}\n\nfn main() {\n    let mut x = 5;\n    let mut y = 10;\n}\n",
            "expected_output": "10 5",
            "hints": ["`std::mem::swap(a, b);`"],
            "solution": "fn swap(a: &mut i32, b: &mut i32) {\n    std::mem::swap(a, b);\n}\n\nfn main() {\n    let mut x = 5;\n    let mut y = 10;\n    swap(&mut x, &mut y);\n    println!(\"{} {}\", x, y);\n}\n",
        },
    ]

    out = copy.deepcopy(go)
    out["description"] = "References, mutability, and Box in Rust"
    out["theory"] = theory
    out["exercises"] = exercises
    out["exercise_count"] = len(exercises)
    return out
