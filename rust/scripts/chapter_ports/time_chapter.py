"""Port: time — chrono / chrono-tz (from LEARN-GO time)."""

from __future__ import annotations

import copy


def build(go: dict) -> dict:
    theory = """## Time in Rust

The **`chrono`** crate is the common choice for calendar dates, time zones, and durations (similar to Go’s `time` package).

- `Utc.with_ymd_and_hms(...)` — build an instant in UTC  
- **`chrono_tz`** — named zones like `Asia::Tokyo`  
- `NaiveDateTime::parse_from_str` + `.and_utc()` — parse without offset then treat as UTC  
- `signed_duration_since`, `checked_add_signed`, `num_days`, `num_hours` — arithmetic  

Go’s `time.Now` + `Sleep` exercise is replaced here with a **fixed clock** so your output still matches the checker when you submit.
"""

    exercises = [
        {
            "id": "time_01",
            "title": "Build a UTC instant",
            "description": "Create January 1, 2024, 12:00:00 UTC with `chrono::Utc` and print it.",
            "starter_code": "use chrono::prelude::*;\n\nfn main() {\n}\n",
            "expected_output": "2024-01-01 12:00:00 UTC",
            "hints": ["`Utc.with_ymd_and_hms(2024, 1, 1, 12, 0, 0).unwrap()`"],
            "solution": "use chrono::prelude::*;\n\nfn main() {\n    let t = Utc.with_ymd_and_hms(2024, 1, 1, 12, 0, 0).unwrap();\n    println!(\"{}\", t);\n}\n",
        },
        {
            "id": "time_02",
            "title": "Components in Tokyo",
            "description": "Use `chrono_tz::Asia::Tokyo` and `with_ymd_and_hms` for 2023-03-15 14:30:00. Print year, month name, day, hour, minute, weekday (same labels as the Go exercise).",
            "starter_code": "use chrono::prelude::*;\nuse chrono_tz::Asia::Tokyo;\n\nfn main() {\n}\n",
            "expected_output": "Year: 2023\nMonth: March\nDay: 15\nHour: 14\nMinute: 30\nWeekday: Wednesday",
            "hints": ["`t.format(\"%B\")` for month name", "`t.format(\"%A\")` for weekday"],
            "solution": "use chrono::prelude::*;\nuse chrono_tz::Asia::Tokyo;\n\nfn main() {\n    let t = Tokyo.with_ymd_and_hms(2023, 3, 15, 14, 30, 0).unwrap();\n    println!(\"Year: {}\", t.year());\n    println!(\"Month: {}\", t.format(\"%B\"));\n    println!(\"Day: {}\", t.day());\n    println!(\"Hour: {}\", t.hour());\n    println!(\"Minute: {}\", t.minute());\n    println!(\"Weekday: {}\", t.format(\"%A\"));\n}\n",
        },
        {
            "id": "time_03",
            "title": "Durations",
            "description": "Build a duration of 2 hours + 30 minutes and print it in Go-style `HhMmMs` (`2h30m0s`). Then print `500ms` for a half-second (format these two lines exactly).",
            "starter_code": "use chrono::Duration;\n\nfn fmt_hms(d: Duration) -> String {\n    let secs = d.num_seconds();\n    let h = secs / 3600;\n    let m = (secs % 3600) / 60;\n    let s = secs % 60;\n    format!(\"{}h{}m{}s\", h, m, s)\n}\n\nfn main() {\n}\n",
            "expected_output": "2h30m0s\n500ms",
            "hints": ["`Duration::hours(2) + Duration::minutes(30)`", "For ms: `Duration::milliseconds(500).num_milliseconds()`"],
            "solution": "use chrono::Duration;\n\nfn fmt_hms(d: Duration) -> String {\n    let secs = d.num_seconds();\n    let h = secs / 3600;\n    let m = (secs % 3600) / 60;\n    let s = secs % 60;\n    format!(\"{}h{}m{}s\", h, m, s)\n}\n\nfn main() {\n    let d = Duration::hours(2) + Duration::minutes(30);\n    println!(\"{}\", fmt_hms(d));\n    let ms = Duration::milliseconds(500);\n    println!(\"{}ms\", ms.num_milliseconds());\n}\n",
        },
        {
            "id": "time_04",
            "title": "Parse naive datetime",
            "description": "Parse `\"2024-06-15 09:30:00\"` with format `'%Y-%m-%d %H:%M:%S'`, interpret as UTC with `.and_utc()`, print the `DateTime<Utc>`.",
            "starter_code": "use chrono::prelude::*;\n\nfn main() {\n}\n",
            "expected_output": "2024-06-15 09:30:00 UTC",
            "hints": ["`NaiveDateTime::parse_from_str(..., \"%Y-%m-%d %H:%M:%S\")`"],
            "solution": "use chrono::prelude::*;\n\nfn main() {\n    let layout = \"%Y-%m-%d %H:%M:%S\";\n    let value = \"2024-06-15 09:30:00\";\n    let naive = NaiveDateTime::parse_from_str(value, layout).unwrap();\n    let t = naive.and_utc();\n    println!(\"{}\", t);\n}\n",
        },
        {
            "id": "time_05",
            "title": "Format",
            "description": "July 4, 2024 16:00 UTC. Print `MM/DD/YYYY` on the first line, then a long line like `Thursday, July 4, 2024` (match the sample exactly).",
            "starter_code": "use chrono::prelude::*;\n\nfn main() {\n}\n",
            "expected_output": "07/04/2024\nThursday, July 4, 2024",
            "hints": ["`t.format(\"%m/%d/%Y\")`", "For the second line, `%A, %B %e, %Y` then collapse double spaces from `%e` padding"],
            "solution": "use chrono::prelude::*;\n\nfn main() {\n    let t = Utc.with_ymd_and_hms(2024, 7, 4, 16, 0, 0).unwrap();\n    println!(\"{}\", t.format(\"%m/%d/%Y\"));\n    let long = format!(\"{}\", t.format(\"%A, %B %e, %Y\"));\n    println!(\"{}\", long.replace(\"  \", \" \"));\n}\n",
        },
        {
            "id": "time_06",
            "title": "Add duration",
            "description": "Start at 2024-01-15 10:00 UTC. Add 3 days and 5 hours; print the result.",
            "starter_code": "use chrono::prelude::*;\n\nfn main() {\n}\n",
            "expected_output": "2024-01-18 15:00:00 UTC",
            "hints": ["`t + Duration::hours(3 * 24 + 5)`"],
            "solution": "use chrono::prelude::*;\n\nfn main() {\n    let t = Utc.with_ymd_and_hms(2024, 1, 15, 10, 0, 0).unwrap();\n    let out = t + chrono::Duration::hours(3 * 24 + 5);\n    println!(\"{}\", out);\n}\n",
        },
        {
            "id": "time_07",
            "title": "Subtract instants",
            "description": "Fixed `now` = 2024-12-25 UTC midnight, `then` = 2024-11-25 UTC midnight. Print the duration in Go-style hours (`720h0m0s`) then `Days: 30`.",
            "starter_code": "use chrono::prelude::*;\n\nfn main() {\n}\n",
            "expected_output": "720h0m0s\nDays: 30",
            "hints": ["`now.signed_duration_since(then)`", "`diff.num_hours()` and `diff.num_days()`"],
            "solution": "use chrono::prelude::*;\n\nfn main() {\n    let now = Utc.with_ymd_and_hms(2024, 12, 25, 0, 0, 0).unwrap();\n    let then = Utc.with_ymd_and_hms(2024, 11, 25, 0, 0, 0).unwrap();\n    let diff = now.signed_duration_since(then);\n    println!(\"{}h0m0s\", diff.num_hours());\n    println!(\"Days: {}\", diff.num_days());\n}\n",
        },
        {
            "id": "time_09",
            "title": "Before / after",
            "description": "Compare Jan 1 2024 and Dec 31 2024 UTC with `lt`/`gt` (or `<`/`>`) and print the two lines from the Go exercise.",
            "starter_code": "use chrono::prelude::*;\n\nfn main() {\n}\n",
            "expected_output": "January 1 is before December 31: true\nDecember 31 is after January 1: true",
            "hints": ["`t1 < t2` is the same idea as Go’s `Before`"],
            "solution": "use chrono::prelude::*;\n\nfn main() {\n    let t1 = Utc.with_ymd_and_hms(2024, 1, 1, 0, 0, 0).unwrap();\n    let t2 = Utc.with_ymd_and_hms(2024, 12, 31, 0, 0, 0).unwrap();\n    println!(\"January 1 is before December 31: {}\", t1 < t2);\n    println!(\"December 31 is after January 1: {}\", t2 > t1);\n}\n",
        },
        {
            "id": "time_08",
            "title": "Fixed clock (no wall time)",
            "description": "Go used `time.Now` + `Sleep`. Here: use `Utc.with_ymd_and_hms(2024, 6, 1, 10, 15, 30)`. Print the instant, then hour and minute, then the instant plus one second (`+ Duration::seconds(1)`) labeled `After +1s:` — deterministic output.",
            "starter_code": "use chrono::prelude::*;\n\nfn main() {\n}\n",
            "expected_output": "2024-06-01 10:15:30 UTC\nHour: 10\nMinute: 15\nAfter +1s: 2024-06-01 10:15:31 UTC",
            "hints": ["No `std::thread::sleep` — add a `chrono::Duration` instead"],
            "solution": "use chrono::prelude::*;\n\nfn main() {\n    let t = Utc.with_ymd_and_hms(2024, 6, 1, 10, 15, 30).unwrap();\n    println!(\"{}\", t);\n    println!(\"Hour: {}\", t.hour());\n    println!(\"Minute: {}\", t.minute());\n    let after = t + chrono::Duration::seconds(1);\n    println!(\"After +1s: {}\", after);\n}\n",
        },
    ]

    out = copy.deepcopy(go)
    out["title"] = "Time"
    out["description"] = "Dates, zones, and durations with chrono"
    out["theory"] = theory
    out["exercises"] = exercises
    out["exercise_count"] = len(exercises)
    return out
