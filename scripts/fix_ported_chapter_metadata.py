#!/usr/bin/env python3
"""Fix chapter-level title/description text ported from the Go track."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PYTHON_OVERRIDES: dict[str, tuple[str | None, str | None]] = {
    "ownership": ("Values, copies, and references", "How assignment, mutability, and shared objects work in Python"),
    "concurrency": ("Concurrency", "Threads, locks, and coordinating work in Python"),
    "errors": ("Errors and exceptions", "Raising, catching, and modeling failure in Python"),
    "testing": ("Testing", "Writing and running tests with the standard library"),
    "packages": ("Modules and packages", "Imports, packages, and module-level code in Python"),
    "interfaces": ("Protocols and duck typing", "Structural typing with protocols and ABCs"),
    "structs": ("Classes and data objects", "Classes, dataclasses, and grouped state"),
    "maps": ("Dictionaries", "dict keys, values, and common mapping patterns"),
    "slices": ("Lists and slices", "list growth, slicing, and views of sequences"),
    "arrays": ("Sequences and lists", "Lists as the primary fixed/dynamic sequence"),
    "functions": ("Functions", "def, parameters, return values, and closures"),
    "controlflow": ("Control flow", "if, while, for, and match in Python"),
    "variables": ("Variables and types", "Names, dynamic typing, and basic conversions"),
    "pointers": ("References and identity", "Object identity, aliasing, and optional None"),
    "strings": ("Strings", "str, formatting, and text processing"),
    "json": ("JSON", "json module encoding and decoding"),
    "time": ("Date and time", "datetime, timedelta, and time zones"),
    "methods": ("Methods", "Instance methods, self, and special methods"),
}

JAVA_OVERRIDES: dict[str, tuple[str | None, str | None]] = {
    k: (v[0], v[1].replace("Python", "Java")) for k, v in PYTHON_OVERRIDES.items()
}
JAVA_OVERRIDES["ownership"] = (
    "Values, references, and mutation",
    "How Java passes references, copies fields, and shares mutable objects",
)
JAVA_OVERRIDES["interfaces"] = ("Interfaces", "Interfaces, implementations, and polymorphism in Java")
JAVA_OVERRIDES["structs"] = ("Classes and records", "Classes, records, and grouped state in Java")
JAVA_OVERRIDES["slices"] = ("Arrays and lists", "Arrays, ArrayList, and subranges")
JAVA_OVERRIDES["maps"] = ("Maps", "HashMap, keys, values, and iteration")
JAVA_OVERRIDES["packages"] = ("Packages", "package declarations, imports, and visibility")
JAVA_OVERRIDES["pointers"] = ("References", "References, null, and aliasing in Java")
JAVA_OVERRIDES["methods"] = ("Methods", "Instance and static methods on classes")

CSHARP_OVERRIDES: dict[str, tuple[str | None, str | None]] = {
    k: (v[0], v[1].replace("Python", "C#")) for k, v in PYTHON_OVERRIDES.items()
}
CSHARP_OVERRIDES["ownership"] = (
    "References vs values",
    "Value types, reference types, and garbage collection in C#",
)
CSHARP_OVERRIDES["interfaces"] = ("Interfaces", "Interfaces, classes, and polymorphism in C#")
CSHARP_OVERRIDES["structs"] = ("Structs and records", "Structs, records, and grouped data in C#")
CSHARP_OVERRIDES["slices"] = ("Spans and arrays", "Arrays, spans, and ranges in C#")
CSHARP_OVERRIDES["maps"] = ("Dictionaries", "Dictionary and sorted collections")
CSHARP_OVERRIDES["packages"] = ("Namespaces and projects", "Namespaces, assemblies, and project layout")
CSHARP_OVERRIDES["pointers"] = ("Unsafe code", "unsafe, pointers, and interop in C#")
CSHARP_OVERRIDES["concurrency"] = ("Async and tasks", "Tasks, async/await, and parallel work in C#")

C_OVERRIDES: dict[str, tuple[str | None, str | None]] = {
    "variables": ("Variables and types", "Declarations, types, literals, and printf output"),
    "ownership": ("Aliasing and memory", "Pointers, copies, and who owns heap data in C"),
    "controlflow": ("Control flow", "if, loops, switch, break, and continue"),
    "functions": ("Functions", "Prototypes, parameters, return values, and linkage"),
    "arrays": ("Arrays", "Fixed-size arrays and pointer decay"),
    "slices": ("Pointers and array views", "Pointers, lengths, and subranges in C"),
    "maps": ("Associative data", "Hash tables and key/value patterns (adapted)"),
    "strings": ("Strings", "char arrays, string literals, and stdio"),
    "structs": ("Structs", "struct layout, typedef, and grouped fields"),
    "interfaces": ("Polymorphism in C", "Function pointers and vtable-style patterns"),
    "methods": ("Methods as functions", "Functions with a struct pointer receiver"),
    "pointers": ("Pointers", "Addresses, dereference, and const correctness"),
    "errors": ("Error handling", "Return codes, errno, and reporting failures"),
    "concurrency": ("Concurrency", "Threads and synchronization with pthreads"),
    "testing": ("Testing", "Assertions and test harness patterns in C"),
    "json": ("JSON", "Parsing and emitting JSON-shaped text"),
    "time": ("Time", "Calendar time and monotonic clocks with time.h"),
}


def patch_track(track: str, overrides: dict[str, tuple[str | None, str | None]]) -> int:
    n = 0
    for path in sorted((ROOT / track / "chapters").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        chapter_id = data.get("id", "")
        if chapter_id not in overrides:
            continue
        title, description = overrides[chapter_id]
        changed = False
        if title and data.get("title") != title:
            data["title"] = title
            changed = True
        if description and data.get("description") != description:
            data["description"] = description
            changed = True
        if changed:
            path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            n += 1
    return n


def main() -> int:
    py_n = patch_track("python", PYTHON_OVERRIDES)
    java_n = patch_track("java", JAVA_OVERRIDES)
    cs_n = patch_track("csharp", CSHARP_OVERRIDES)
    c_n = patch_track("c", C_OVERRIDES)
    print(f"python: updated {py_n} chapter metadata files")
    print(f"java: updated {java_n} chapter metadata files")
    print(f"csharp: updated {cs_n} chapter metadata files")
    print(f"c: updated {c_n} chapter metadata files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
