"""Port: testing — #[test], cargo test (from LEARN-GO testing)."""

from __future__ import annotations

import copy


def build(go: dict) -> dict:
    theory = """## Tests in Rust

Mark unit tests with `#[test]` (usually in the same file under `#[cfg(test)] mod tests { ... }`).

Run them with `cargo test`. Assertions use `assert!`, `assert_eq!`, and `Result` returns from tests.

This course checks answers by running `cargo test` when your snippet contains `#[test]`. The expected line is `PASS` when all tests succeed.
"""

    exercises = [
        {
            "id": "testing_01",
            "title": "Basic test",
            "description": "Implement `sum(a, b: i32) -> i32`. Add a `#[test]` that checks `sum(2, 3) == 5`. Keep `fn main() {}` so the file is a binary crate.",
            "starter_code": "pub fn sum(a: i32, b: i32) -> i32 {\n    a + b\n}\n\n#[cfg(test)]\nmod tests {\n    use super::*;\n\n    #[test]\n    fn sum_two_and_three() {\n        // assert_eq!(...)\n    }\n}\n\nfn main() {}\n",
            "expected_output": "PASS",
            "hints": ["`assert_eq!(sum(2, 3), 5);`"],
            "solution": "pub fn sum(a: i32, b: i32) -> i32 {\n    a + b\n}\n\n#[cfg(test)]\nmod tests {\n    use super::*;\n\n    #[test]\n    fn sum_two_and_three() {\n        assert_eq!(sum(2, 3), 5);\n    }\n}\n\nfn main() {}\n",
        },
        {
            "id": "testing_02",
            "title": "Table-driven test",
            "description": "Table-test `multiply(a, b)` for `(2,3)->6`, `(0,5)->0`, `(-1,4)->-4` using a `Vec` of tuples in one `#[test]`.",
            "starter_code": "pub fn multiply(a: i32, b: i32) -> i32 {\n    a * b\n}\n\n#[cfg(test)]\nmod tests {\n    use super::*;\n\n    #[test]\n    fn multiply_cases() {\n        let cases = vec![\n            // (a, b, expected)\n        ];\n        for (a, b, expected) in cases {\n            assert_eq!(multiply(a, b), expected);\n        }\n    }\n}\n\nfn main() {}\n",
            "expected_output": "PASS",
            "hints": ["Push `(2, 3, 6)`, `(0, 5, 0)`, `(-1, 4, -4)`"],
            "solution": "pub fn multiply(a: i32, b: i32) -> i32 {\n    a * b\n}\n\n#[cfg(test)]\nmod tests {\n    use super::*;\n\n    #[test]\n    fn multiply_cases() {\n        let cases = vec![(2, 3, 6), (0, 5, 0), (-1, 4, -4)];\n        for (a, b, expected) in cases {\n            assert_eq!(multiply(a, b), expected);\n        }\n    }\n}\n\nfn main() {}\n",
        },
        {
            "id": "testing_03",
            "title": "Divide and error",
            "description": "Implement `divide(a, b: i32) -> Result<i32, &'static str>` returning `Err(\"division by zero\")` when `b == 0`. Add two tests: `10/2 == Ok(5)` and `10/0` is `Err`.",
            "starter_code": "pub fn divide(a: i32, b: i32) -> Result<i32, &'static str> {\n    if b == 0 {\n        return Err(\"division by zero\");\n    }\n    Ok(a / b)\n}\n\n#[cfg(test)]\nmod tests {\n    use super::*;\n\n    #[test]\n    fn divide_ok() {}\n\n    #[test]\n    fn divide_by_zero() {}\n}\n\nfn main() {}\n",
            "expected_output": "PASS",
            "hints": ["`assert_eq!(divide(10, 2), Ok(5));`", "`assert!(divide(10, 0).is_err());`"],
            "solution": "pub fn divide(a: i32, b: i32) -> Result<i32, &'static str> {\n    if b == 0 {\n        return Err(\"division by zero\");\n    }\n    Ok(a / b)\n}\n\n#[cfg(test)]\nmod tests {\n    use super::*;\n\n    #[test]\n    fn divide_ok() {\n        assert_eq!(divide(10, 2), Ok(5));\n    }\n\n    #[test]\n    fn divide_by_zero() {\n        assert!(divide(10, 0).is_err());\n    }\n}\n\nfn main() {}\n",
        },
        {
            "id": "testing_05",
            "title": "Hot path smoke test",
            "description": "Rust’s stable `#[bench]` lives behind a feature flag; instead, add a `#[test]` that calls `sum(2, 3)` in a tight loop many times so the optimizer still has real work to do (mirrors “measure this hot path” intent).",
            "starter_code": "pub fn sum(a: i32, b: i32) -> i32 {\n    a + b\n}\n\n#[cfg(test)]\nmod tests {\n    use super::*;\n\n    #[test]\n    fn sum_many_iterations() {\n        // for _ in 0..10_000 { assert_eq!(sum(2, 3), 5); }\n    }\n}\n\nfn main() {}\n",
            "expected_output": "PASS",
            "hints": ["Keep the assertion inside the loop or once after — both compile; loop stresses the call site."],
            "solution": "pub fn sum(a: i32, b: i32) -> i32 {\n    a + b\n}\n\n#[cfg(test)]\nmod tests {\n    use super::*;\n\n    #[test]\n    fn sum_many_iterations() {\n        for _ in 0..10_000 {\n            assert_eq!(sum(2, 3), 5);\n        }\n    }\n}\n\nfn main() {}\n",
        },
        {
            "id": "testing_04",
            "title": "Error message assertion",
            "description": "`validate(age: i32) -> Result<(), &'static str>`: negative age returns `Err(\"age cannot be negative\")`, age > 150 returns too-large, else `Ok(())`. Test that `-5` yields an error whose message contains `\"negative\"`.",
            "starter_code": "pub fn validate(age: i32) -> Result<(), &'static str> {\n    if age < 0 {\n        return Err(\"age cannot be negative\");\n    }\n    if age > 150 {\n        return Err(\"age is too large\");\n    }\n    Ok(())\n}\n\n#[cfg(test)]\nmod tests {\n    use super::*;\n\n    #[test]\n    fn validate_negative_age_message() {\n        let err = validate(-5).unwrap_err();\n        // assert!(err.contains(\"negative\"));\n    }\n}\n\nfn main() {}\n",
            "expected_output": "PASS",
            "hints": ["`&str` has `.contains` just like Go’s `strings.Contains` on the error string."],
            "solution": "pub fn validate(age: i32) -> Result<(), &'static str> {\n    if age < 0 {\n        return Err(\"age cannot be negative\");\n    }\n    if age > 150 {\n        return Err(\"age is too large\");\n    }\n    Ok(())\n}\n\n#[cfg(test)]\nmod tests {\n    use super::*;\n\n    #[test]\n    fn validate_negative_age_message() {\n        let err = validate(-5).unwrap_err();\n        assert!(err.contains(\"negative\"));\n    }\n}\n\nfn main() {}\n",
        },
    ]

    out = copy.deepcopy(go)
    out["title"] = "Testing"
    out["description"] = "Unit tests with #[test] and cargo test"
    out["theory"] = theory
    out["exercises"] = exercises
    out["exercise_count"] = len(exercises)
    return out
