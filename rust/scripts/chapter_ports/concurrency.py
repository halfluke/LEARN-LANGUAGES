"""Port: concurrency — threads and channels (std)."""

from __future__ import annotations

import copy


def build(go: dict) -> dict:
    theory = """## Concurrency in Rust

Use `std::thread::spawn` and `std::sync::mpsc` channels for message passing.

`std::thread::JoinHandle::join` waits for completion; `sync_channel` can bound buffers.
"""

    exercises = [
        {
            "id": "concurrency_01",
            "title": "Spawn thread",
            "description": "Spawn a thread that prints `Hello!`, sleep 100ms, then print `main done` (deterministic order).",
            "starter_code": "use std::thread;\nuse std::time::Duration;\n\nfn say_hello() {\n    println!(\"Hello!\");\n}\n\nfn main() {\n}\n",
            "expected_output": "Hello!\nmain done",
            "hints": ["`thread::spawn` then `sleep` then `join` so `Hello!` prints before `main done`."],
            "solution": "use std::thread;\nuse std::time::Duration;\n\nfn say_hello() {\n    println!(\"Hello!\");\n}\n\nfn main() {\n    let h = thread::spawn(|| say_hello());\n    thread::sleep(Duration::from_millis(100));\n    h.join().unwrap();\n    println!(\"main done\");\n}\n",
        },
        {
            "id": "concurrency_02",
            "title": "Channel",
            "description": "Send `ping` from a thread, receive in main.",
            "starter_code": "use std::thread;\nuse std::sync::mpsc;\n\nfn main() {\n}\n",
            "expected_output": "ping",
            "hints": ["`mpsc::channel()`"],
            "solution": "use std::sync::mpsc;\nuse std::thread;\n\nfn main() {\n    let (tx, rx) = mpsc::channel();\n    thread::spawn(move || {\n        tx.send(\"ping\".to_string()).unwrap();\n    });\n    println!(\"{}\", rx.recv().unwrap());\n}\n",
        },
        {
            "id": "concurrency_03",
            "title": "Bounded channel",
            "description": "`sync_channel(2)` send 10 and 20, receive both.",
            "starter_code": "use std::sync::mpsc;\n\nfn main() {\n}\n",
            "expected_output": "10 20",
            "hints": ["`mpsc::sync_channel(2)`"],
            "solution": "use std::sync::mpsc;\n\nfn main() {\n    let (tx, rx) = mpsc::sync_channel(2);\n    tx.send(10).unwrap();\n    tx.send(20).unwrap();\n    println!(\"{} {}\", rx.recv().unwrap(), rx.recv().unwrap());\n}\n",
        },
        {
            "id": "concurrency_04",
            "title": "First ready",
            "description": "Receive from `ch1` after a short sleep in another thread (no true `select!` in std alone).",
            "starter_code": "use std::sync::mpsc;\nuse std::thread;\nuse std::time::Duration;\n\nfn main() {\n    let (tx1, rx1) = mpsc::channel::<String>();\n}\n",
            "expected_output": "from ch1",
            "hints": ["Spawn thread that sleeps 10ms then sends"],
            "solution": "use std::sync::mpsc;\nuse std::thread;\nuse std::time::Duration;\n\nfn main() {\n    let (tx1, rx1) = mpsc::channel::<String>();\n    thread::spawn(move || {\n        thread::sleep(Duration::from_millis(10));\n        tx1.send(\"from ch1\".into()).unwrap();\n    });\n    println!(\"{}\", rx1.recv().unwrap());\n}\n",
        },
        {
            "id": "concurrency_05",
            "title": "Close / drain",
            "description": "Sender thread sends 1,2,3 then drops `tx`; main receives until error.",
            "starter_code": "use std::sync::mpsc;\nuse std::thread;\n\nfn main() {\n}\n",
            "expected_output": "1\n2\n3",
            "hints": ["`while let Ok(n) = rx.recv()`"],
            "solution": "use std::sync::mpsc;\nuse std::thread;\n\nfn main() {\n    let (tx, rx) = mpsc::channel::<i32>();\n    thread::spawn(move || {\n        for n in [1, 2, 3] {\n            tx.send(n).unwrap();\n        }\n    });\n    while let Ok(n) = rx.recv() {\n        println!(\"{}\", n);\n    }\n}\n",
        },
        {
            "id": "concurrency_07",
            "title": "Fan-in",
            "description": "Two threads send `hello` and `world`; collect both lines sorted for stable output.",
            "starter_code": "use std::sync::{mpsc, Arc, Mutex};\nuse std::thread;\n\nfn main() {\n}\n",
            "expected_output": "hello\nworld",
            "hints": ["`Arc<Mutex<Vec<_>>>` or receive into `Vec` then `sort`"],
            "solution": "use std::sync::mpsc;\nuse std::thread;\n\nfn main() {\n    let (tx, rx) = mpsc::channel::<String>();\n    let tx2 = tx.clone();\n    thread::spawn(move || {\n        tx.send(\"hello\".into()).unwrap();\n    });\n    thread::spawn(move || {\n        tx2.send(\"world\".into()).unwrap();\n    });\n    let mut v = Vec::new();\n    while let Ok(s) = rx.recv() {\n        v.push(s);\n    }\n    v.sort();\n    for s in v {\n        println!(\"{}\", s);\n    }\n}\n",
        },
        {
            "id": "concurrency_06",
            "title": "Join handles",
            "description": "Spawn three threads printing 1..=3 in order using sequential joins.",
            "starter_code": "use std::thread;\n\nfn main() {\n}\n",
            "expected_output": "1\n2\n3\ndone",
            "hints": ["Push handles then join in order"],
            "solution": "use std::thread;\n\nfn main() {\n    for i in 1..=3 {\n        thread::spawn(move || println!(\"{}\", i))\n            .join()\n            .unwrap();\n    }\n    println!(\"done\");\n}\n",
        },
    ]

    out = copy.deepcopy(go)
    out["description"] = "Threads and channels in Rust"
    out["theory"] = theory
    out["exercises"] = exercises
    out["exercise_count"] = len(exercises)
    return out
