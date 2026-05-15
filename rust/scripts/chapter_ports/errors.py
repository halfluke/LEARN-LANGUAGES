"""Port: errors — Result, ? patterns, error sources."""

from __future__ import annotations

import copy


def build(go: dict) -> dict:
    theory = """## Errors in Rust

Recoverable failures use `Result<T, E>`. The `?` operator propagates errors.

For **dynamic** errors in small programs, `Box<dyn std::error::Error>` is common; here we stick to concrete `String` errors and `source()` where needed.

`Error::is` / `Error::cause` style checks are expressed with `downcast_ref` on trait objects in advanced code; this chapter uses string messages and `Result` matching.
"""

    exercises = [
        {
            "id": "errors_01",
            "title": "Return Result",
            "description": "`divide` returning `Err` on zero; handle and print `Error: division by zero`.",
            "starter_code": "fn divide(a: f64, b: f64) -> Result<f64, &'static str> {\n    Ok(0.0)\n}\n\nfn main() {\n}\n",
            "expected_output": "Error: division by zero",
            "hints": ["`Err(\"division by zero\")`"],
            "solution": "fn divide(a: f64, b: f64) -> Result<f64, &'static str> {\n    if b == 0.0 {\n        Err(\"division by zero\")\n    } else {\n        Ok(a / b)\n    }\n}\n\nfn main() {\n    match divide(10.0, 0.0) {\n        Ok(v) => println!(\"Result: {}\", v),\n        Err(e) => println!(\"Error: {}\", e),\n    }\n}\n",
        },
        {
            "id": "errors_02",
            "title": "Not-found Result",
            "description": "`find_user` returns `Err` unless name is `alice`; on `bob` print `User not found`.",
            "starter_code": "fn find_user(name: &str) -> Result<(), &'static str> {\n    Ok(())\n}\n\nfn main() {\n}\n",
            "expected_output": "User not found",
            "hints": ["`if name != \"alice\" { Err(\"not found\") }`"],
            "solution": "fn find_user(name: &str) -> Result<(), &'static str> {\n    if name != \"alice\" {\n        Err(\"not found\")\n    } else {\n        Ok(())\n    }\n}\n\nfn main() {\n    if find_user(\"bob\").is_err() {\n        println!(\"User not found\");\n    }\n}\n",
        },
        {
            "id": "errors_03",
            "title": "Map error",
            "description": "Wrap a base error string with prefix using `map_err`.",
            "starter_code": "fn wrap_error() -> Result<(), String> {\n    let base: Result<(), &str> = Err(\"base error\");\n    base.map_err(|e| format!(\"wrapped: {}\", e))\n}\n\nfn main() {\n}\n",
            "expected_output": "wrapped: base error",
            "hints": ["`map_err`"],
            "solution": "fn wrap_error() -> Result<(), String> {\n    let base: Result<(), &str> = Err(\"base error\");\n    base.map_err(|e| format!(\"wrapped: {}\", e))\n}\n\nfn main() {\n    let e = wrap_error().unwrap_err();\n    println!(\"{}\", e);\n}\n",
        },
        {
            "id": "errors_04",
            "title": "Downcast-style field",
            "description": "Return `ValidationError { field: email }` as `Box<dyn std::error::Error>`; print field.",
            "starter_code": "use std::error::Error;\nuse std::fmt;\n\n#[derive(Debug)]\nstruct ValidationError {\n    field: String,\n}\n\nimpl fmt::Display for ValidationError {\n    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {\n        write!(f, \"{}\", self.field)\n    }\n}\n\nimpl Error for ValidationError {}\n\nfn validate() -> Result<(), Box<dyn Error>> {\n    Ok(())\n}\n\nfn main() {}\n",
            "expected_output": "email",
            "hints": ["`Err(Box::new(ValidationError { field: \"email\".into() }))`", "`err.downcast_ref::<ValidationError>()`"],
            "solution": "use std::error::Error;\nuse std::fmt;\n\n#[derive(Debug)]\nstruct ValidationError {\n    field: String,\n}\n\nimpl fmt::Display for ValidationError {\n    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {\n        write!(f, \"invalid\")\n    }\n}\n\nimpl Error for ValidationError {}\n\nfn validate() -> Result<(), Box<dyn Error>> {\n    Err(Box::new(ValidationError {\n        field: \"email\".into(),\n    }))\n}\n\nfn main() {\n    let err = validate().unwrap_err();\n    if let Some(ve) = err.downcast_ref::<ValidationError>() {\n        println!(\"{}\", ve.field);\n    }\n}\n",
        },
        {
            "id": "errors_05",
            "title": "Ok branch",
            "description": "On success print quotient only.",
            "starter_code": "fn safe_divide(a: i32, b: i32) -> Result<i32, String> {\n    if b == 0 {\n        Err(\"cannot divide by zero\".into())\n    } else {\n        Ok(a / b)\n    }\n}\n\nfn main() {\n}\n",
            "expected_output": "5",
            "hints": ["`if let Ok(v) = ...`"],
            "solution": "fn safe_divide(a: i32, b: i32) -> Result<i32, String> {\n    if b == 0 {\n        Err(\"cannot divide by zero\".into())\n    } else {\n        Ok(a / b)\n    }\n}\n\nfn main() {\n    if let Ok(v) = safe_divide(10, 2) {\n        println!(\"{}\", v);\n    }\n}\n",
        },
        {
            "id": "errors_07",
            "title": "Inspect chain",
            "description": "Print formatted error then `Disk is full` if message contains `disk full`.",
            "starter_code": "fn read_file(name: &str) -> Result<(), String> {\n    Err(format!(\"reading {}: disk full\", name))\n}\n\nfn main() {\n}\n",
            "expected_output": "reading data.txt: disk full\nDisk is full",
            "hints": ["`contains(\"disk full\")`"],
            "solution": "fn read_file(name: &str) -> Result<(), String> {\n    Err(format!(\"reading {}: disk full\", name))\n}\n\nfn main() {\n    let err = read_file(\"data.txt\").unwrap_err();\n    println!(\"{}\", err);\n    if err.contains(\"disk full\") {\n        println!(\"Disk is full\");\n    }\n}\n",
        },
        {
            "id": "errors_06",
            "title": "Sentinel constant",
            "description": "Compare `Err` to `ERR_NOT_FOUND` constant using `==` on `&str`.",
            "starter_code": "const ERR_NOT_FOUND: &str = \"not found\";\n\nfn get_item(id: i32) -> Result<String, &'static str> {\n    Ok(\"item\".into())\n}\n\nfn main() {}\n",
            "expected_output": "not found",
            "hints": ["return `Err(ERR_NOT_FOUND)`"],
            "solution": "const ERR_NOT_FOUND: &str = \"not found\";\n\nfn get_item(id: i32) -> Result<&'static str, &'static str> {\n    if id < 0 {\n        Err(ERR_NOT_FOUND)\n    } else {\n        Ok(\"item\")\n    }\n}\n\nfn main() {\n    match get_item(-1) {\n        Err(e) if e == ERR_NOT_FOUND => println!(\"not found\"),\n        _ => {}\n    }\n}\n",
        },
    ]

    out = copy.deepcopy(go)
    out["description"] = "Result-based error handling in Rust"
    out["theory"] = theory
    out["exercises"] = exercises
    out["exercise_count"] = len(exercises)
    return out
