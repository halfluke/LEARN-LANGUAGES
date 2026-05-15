"""Port: json — serde / serde_json (from LEARN-GO encoding/json)."""

from __future__ import annotations

import copy


def build(go: dict) -> dict:
    theory = """## JSON in Rust

The ecosystem standard is **`serde`** for serialization traits and **`serde_json`** for JSON.

- `serde_json::to_string` / `to_vec` — encode to JSON text or bytes  
- `serde_json::from_str` / `from_slice` — decode  
- Field renaming and `skip_serializing_if` mirror Go struct tags (`json:"name,omitempty"`).

Streaming decode of multiple values from one buffer uses `serde_json::Deserializer::from_str(...).into_iter::<T>()`.
"""

    exercises = [
        {
            "id": "json_01",
            "title": "Serialize a struct",
            "description": "`Person { Name, Age }` with `Serialize`. Build `Person { Name: \"Alice\", Age: 30 }`, serialize with `serde_json::to_string`, print it.",
            "starter_code": "use serde::Serialize;\n\n#[derive(Serialize)]\nstruct Person {\n    Name: String,\n    Age: i32,\n}\n\nfn main() {\n}\n",
            "expected_output": "{\"Name\":\"Alice\",\"Age\":30}",
            "hints": ["`serde_json::to_string(&p).unwrap()`"],
            "solution": "use serde::Serialize;\n\n#[derive(Serialize)]\nstruct Person {\n    Name: String,\n    Age: i32,\n}\n\nfn main() {\n    let p = Person {\n        Name: \"Alice\".into(),\n        Age: 30,\n    };\n    println!(\"{}\", serde_json::to_string(&p).unwrap());\n}\n",
        },
        {
            "id": "json_02",
            "title": "Deserialize JSON",
            "description": "Deserialize `{\"Name\":\"Bob\",\"Age\":25}` into `Person` with `Deserialize`. Print name and age separated by a space (one line: `Bob 25`).",
            "starter_code": "use serde::Deserialize;\n\n#[derive(Deserialize)]\nstruct Person {\n    Name: String,\n    Age: i32,\n}\n\nfn main() {\n    let json_data = r#\"{\"Name\":\"Bob\",\"Age\":25}\"#;\n}\n",
            "expected_output": "Bob 25",
            "hints": ["`serde_json::from_str::<Person>(json_data).unwrap()`"],
            "solution": "use serde::Deserialize;\n\n#[derive(Deserialize)]\nstruct Person {\n    Name: String,\n    Age: i32,\n}\n\nfn main() {\n    let json_data = r#\"{\"Name\":\"Bob\",\"Age\":25}\"#;\n    let p: Person = serde_json::from_str(json_data).unwrap();\n    println!(\"{} {}\", p.Name, p.Age);\n}\n",
        },
        {
            "id": "json_03",
            "title": "serde rename",
            "description": "`User` with Rust fields `first_name`, `last_name`, `birth_year` but JSON keys `first_name`, `last_name`, `birth_year` in snake_case (use `#[serde(rename = ...)]`). Marshal John/Doe/1990 and print JSON.",
            "starter_code": "use serde::Serialize;\n\n#[derive(Serialize)]\nstruct User {\n    // #[serde(rename = \"first_name\")]\n}\n\nfn main() {}\n",
            "expected_output": "{\"first_name\":\"John\",\"last_name\":\"Doe\",\"birth_year\":1990}",
            "hints": ["Mirror Go tags: snake_case names in JSON."],
            "solution": "use serde::Serialize;\n\n#[derive(Serialize)]\nstruct User {\n    #[serde(rename = \"first_name\")]\n    first_name: String,\n    #[serde(rename = \"last_name\")]\n    last_name: String,\n    #[serde(rename = \"birth_year\")]\n    birth_year: i32,\n}\n\nfn main() {\n    let u = User {\n        first_name: \"John\".into(),\n        last_name: \"Doe\".into(),\n        birth_year: 1990,\n    };\n    println!(\"{}\", serde_json::to_string(&u).unwrap());\n}\n",
        },
        {
            "id": "json_04",
            "title": "skip_serializing_if / Option",
            "description": "Model Go’s `,omitempty` with `Option` fields: only set `server: Some(\"api.example.com\")`, leave others `None`. Serialize so output is `{\"Server\":\"api.example.com\"}` (capital `Server` to match the Go exercise).",
            "starter_code": "use serde::Serialize;\n\n#[derive(Serialize)]\nstruct Config {\n    #[serde(rename = \"Server\", skip_serializing_if = \"Option::is_none\")]\n    server: Option<String>,\n    #[serde(rename = \"Port\", skip_serializing_if = \"Option::is_none\")]\n    port: Option<i32>,\n    #[serde(rename = \"Debug\", skip_serializing_if = \"Option::is_none\")]\n    debug: Option<bool>,\n}\n\nfn main() {}\n",
            "expected_output": "{\"Server\":\"api.example.com\"}",
            "hints": ["`Config { server: Some(...), port: None, debug: None }`"],
            "solution": "use serde::Serialize;\n\n#[derive(Serialize)]\nstruct Config {\n    #[serde(rename = \"Server\", skip_serializing_if = \"Option::is_none\")]\n    server: Option<String>,\n    #[serde(rename = \"Port\", skip_serializing_if = \"Option::is_none\")]\n    port: Option<i32>,\n    #[serde(rename = \"Debug\", skip_serializing_if = \"Option::is_none\")]\n    debug: Option<bool>,\n}\n\nfn main() {\n    let c = Config {\n        server: Some(\"api.example.com\".into()),\n        port: None,\n        debug: None,\n    };\n    println!(\"{}\", serde_json::to_string(&c).unwrap());\n}\n",
        },
        {
            "id": "json_05",
            "title": "Round trip",
            "description": "`Product { id, name, price }` with Serialize+Deserialize. Marshal `{1, Laptop, 999.99}`, unmarshal into a new value, print two lines exactly: `Original: {1 Laptop 999.99}` and `Recovered: {1 Laptop 999.99}` (use the same formatting for both).",
            "starter_code": "use serde::{Deserialize, Serialize};\n\n#[derive(Clone, Serialize, Deserialize)]\nstruct Product {\n    id: i32,\n    name: String,\n    price: f64,\n}\n\nfn fmt_go_style(p: &Product) -> String {\n    format!(\"{{{} {} {:.2}}}\", p.id, p.name, p.price)\n}\n\nfn main() {}\n",
            "expected_output": "Original: {1 Laptop 999.99}\nRecovered: {1 Laptop 999.99}",
            "hints": ["`serde_json::to_string` then `from_str`"],
            "solution": "use serde::{Deserialize, Serialize};\n\n#[derive(Clone, Serialize, Deserialize)]\nstruct Product {\n    id: i32,\n    name: String,\n    price: f64,\n}\n\nfn fmt_go_style(p: &Product) -> String {\n    format!(\"{{{} {} {:.2}}}\", p.id, p.name, p.price)\n}\n\nfn main() {\n    let original = Product {\n        id: 1,\n        name: \"Laptop\".into(),\n        price: 999.99,\n    };\n    let data = serde_json::to_string(&original).unwrap();\n    let recovered: Product = serde_json::from_str(&data).unwrap();\n    println!(\"Original: {}\", fmt_go_style(&original));\n    println!(\"Recovered: {}\", fmt_go_style(&recovered));\n}\n",
        },
        {
            "id": "json_06",
            "title": "Nested structs",
            "description": "`Address { street, city }` and `User { name, address }` with `Serialize`. Marshal and print JSON matching Go’s field names (`Street`, `City`, `Name`, `Address`).",
            "starter_code": "use serde::Serialize;\n\n#[derive(Serialize)]\nstruct Address {\n    Street: String,\n    City: String,\n}\n\n#[derive(Serialize)]\nstruct User {\n    Name: String,\n    Address: Address,\n}\n\nfn main() {}\n",
            "expected_output": "{\"Name\":\"Alice\",\"Address\":{\"Street\":\"123 Main St\",\"City\":\"Springfield\"}}",
            "hints": ["PascalCase field names match the Go JSON keys."],
            "solution": "use serde::Serialize;\n\n#[derive(Serialize)]\nstruct Address {\n    Street: String,\n    City: String,\n}\n\n#[derive(Serialize)]\nstruct User {\n    Name: String,\n    Address: Address,\n}\n\nfn main() {\n    let user = User {\n        Name: \"Alice\".into(),\n        Address: Address {\n            Street: \"123 Main St\".into(),\n            City: \"Springfield\".into(),\n        },\n    };\n    println!(\"{}\", serde_json::to_string(&user).unwrap());\n}\n",
        },
        {
            "id": "json_07",
            "title": "Encode a slice",
            "description": "Serialize `Vec<Person>` with two entries to a JSON array string and print it (no extra spaces beyond what `serde_json` emits).",
            "starter_code": "use serde::Serialize;\n\n#[derive(Serialize)]\nstruct Person {\n    Name: String,\n    Age: i32,\n}\n\nfn main() {}\n",
            "expected_output": "[{\"Name\":\"Alice\",\"Age\":30},{\"Name\":\"Bob\",\"Age\":25}]",
            "hints": ["`serde_json::to_string(&vec![...]).unwrap()`"],
            "solution": "use serde::Serialize;\n\n#[derive(Serialize)]\nstruct Person {\n    Name: String,\n    Age: i32,\n}\n\nfn main() {\n    let people = vec![\n        Person {\n            Name: \"Alice\".into(),\n            Age: 30,\n        },\n        Person {\n            Name: \"Bob\".into(),\n            Age: 25,\n        },\n    ];\n    println!(\"{}\", serde_json::to_string(&people).unwrap());\n}\n",
        },
        {
            "id": "json_09",
            "title": "Deferred nested JSON",
            "description": "`LogEntry { level, data }` where `data` is `serde_json::Value`. Parse the sample, print `level` then `data` as compact JSON on the next line. (Object key order follows `serde_json`’s canonicalization, not the source text.)",
            "starter_code": "use serde::Deserialize;\n\n#[derive(Deserialize)]\nstruct LogEntry {\n    level: String,\n    data: serde_json::Value,\n}\n\nfn main() {}\n",
            "expected_output": "info\n{\"action\":\"login\",\"user\":\"alice\"}",
            "hints": ["`serde_json::to_string(&entry.data).unwrap()`"],
            "solution": "use serde::Deserialize;\n\n#[derive(Deserialize)]\nstruct LogEntry {\n    level: String,\n    data: serde_json::Value,\n}\n\nfn main() {\n    let json_data = r#\"{\"level\":\"info\",\"data\":{\"user\":\"alice\",\"action\":\"login\"}}\"#;\n    let entry: LogEntry = serde_json::from_str(json_data).unwrap();\n    println!(\"{}\", entry.level);\n    println!(\"{}\", serde_json::to_string(&entry.data).unwrap());\n}\n",
        },
        {
            "id": "json_08",
            "title": "Decode an array",
            "description": "Parse a JSON array of people with `serde_json::from_str::<Vec<Person>>`, then print each line as `Name Age` (same output as the Go decoder loop).",
            "starter_code": "use serde::Deserialize;\n\n#[derive(Deserialize)]\nstruct Person {\n    #[serde(rename = \"Name\")]\n    name: String,\n    #[serde(rename = \"Age\")]\n    age: i32,\n}\n\nfn main() {}\n",
            "expected_output": "Alice 30\nBob 25",
            "hints": ["`let people: Vec<Person> = serde_json::from_str(json_data).unwrap();`"],
            "solution": "use serde::Deserialize;\n\n#[derive(Deserialize)]\nstruct Person {\n    #[serde(rename = \"Name\")]\n    name: String,\n    #[serde(rename = \"Age\")]\n    age: i32,\n}\n\nfn main() {\n    let json_data = r#\"[{\"Name\":\"Alice\",\"Age\":30},{\"Name\":\"Bob\",\"Age\":25}]\"#;\n    let people: Vec<Person> = serde_json::from_str(json_data).unwrap();\n    for p in people {\n        println!(\"{} {}\", p.name, p.age);\n    }\n}\n",
        },
    ]

    out = copy.deepcopy(go)
    out["title"] = "JSON"
    out["description"] = "JSON with serde and serde_json"
    out["theory"] = theory
    out["exercises"] = exercises
    out["exercise_count"] = len(exercises)
    return out
