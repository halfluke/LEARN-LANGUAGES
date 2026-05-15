#!/usr/bin/env python3
"""Refresh chapter theory, descriptions, and hints for LEARN-C# / LEARN-C (keep solutions)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CS_DIR = ROOT / "csharp" / "chapters"
C_DIR = ROOT / "c" / "chapters"

CUR = (
    "> **Curriculum:** This chapter follows "
    "[LEARN-LANGUAGES/CURRICULUM.md](../../CURRICULUM.md). "
    "Exercise ids are shared across LEARN-* repos for cross-reference.\n\n"
)


def theories_cs() -> dict[str, str]:
    return {
        "variables": "## Variables & types in C#\n\nLocals use `var` or explicit types. Value types copy by assignment; **`string`** is an immutable reference type with convenient literals. Use **`CultureInfo.InvariantCulture`** when exercises require stable decimal text.\n",
        "ownership": CUR
        + "## References vs values in C#\n\nC# is GC-backed like Go. **`string`** is a reference type but behaves like a value for equality on content; small **`struct`** types copy by value. Use this chapter to connect Rust’s move/clone vocabulary to C#’s rules.\n",
        "controlflow": CUR
        + "## Control flow in C#\n\n`if`/`else`, `switch` expressions, `for`, `foreach`, `while`, `break`, and `continue`. Prefer `foreach` for collections.\n",
        "functions": CUR
        + "## Functions in C#\n\nTop-level programs can call **`static` local functions** declared later in the file. Use tuples or `out` parameters when modeling multi-return patterns.\n",
        "arrays": CUR
        + "## Arrays in C#\n\nUse **`int[]`**, **`Span<T>`**, and LINQ (`string.Join`) when you need stable, human-readable formatting for automated stdout checks.\n",
        "slices": CUR
        + "## Spans and ranges\n\nRust slices map well to **`ReadOnlySpan<T>`** and **range syntax** (`arr[1..^1]`).\n",
        "maps": CUR
        + "## Associative containers\n\nUse **`Dictionary<,>`** for hash maps and **`SortedDictionary<,>`** when sorted iteration matters for deterministic output.\n",
        "strings": CUR
        + "## Strings and formatting\n\n`string` is UTF-16. Use **`StringBuilder`** for repeated concatenation and **`CultureInfo`** for invariant formatting.\n",
        "structs": CUR
        + "## Structs and records\n\n**`record`** gives concise data carriers; **`struct`** avoids heap allocation for small immutable values.\n",
        "interfaces": CUR
        + "## Interfaces\n\nC# interfaces describe instance contracts; combine with **`switch` expressions** on types for polymorphic dispatch.\n",
        "methods": CUR
        + "## Methods\n\nInstance methods take an implicit `this`; extension methods add sugar for static calls.\n",
        "packages": CUR
        + "## Namespaces & assemblies\n\nNamespaces organize types; assemblies ship as `.dll`. `using` imports types into scope.\n",
        "pointers": CUR
        + "## Unsafe and pointers\n\nMost code stays managed; **`unsafe`**, **`fixed`**, and **`nint`** exist for interop and performance.\n",
        "errors": CUR
        + "## Errors\n\nUse exceptions for exceptional paths; **`try`/`catch`**, custom exception types, and `when` filters.\n",
        "concurrency": CUR
        + "## Concurrency\n\n**`Task`**, **`async`/`await`**, and **`System.Threading.Channels.Channel`** mirror goroutines/channels at a high level.\n",
        "testing": CUR
        + "## Testing\n\nReal code uses xUnit/NUnit; stdout exercises here mirror assertions as printable outcomes.\n",
        "json": CUR
        + "## JSON\n\n**`System.Text.Json`** handles serialization attributes and polymorphic options.\n",
        "time": CUR
        + "## Time\n\n**`DateTimeOffset`**, **`TimeSpan`**, and **`TimeZoneInfo`** cover instants, durations, and zones.\n",
    }


def theories_c() -> dict[str, str]:
    return {
        "variables": "## Variables in C\n\nLocals are stack objects or pointers; strings are **`const char *`** literals. `printf` formatting must match the exercise’s expected stdout exactly.\n",
        "ownership": CUR
        + "## Aliasing in C\n\nPointers can alias the same storage; integers copy by value. Be explicit about who owns `malloc`’d memory.\n",
        "controlflow": CUR + "## Control flow in C\n\n`if`, `for`, `while`, `switch`, `break`, `continue`.\n",
        "functions": CUR + "## Functions\n\nFile-scope `static` helpers, prototypes, and `struct` parameters.\n",
        "arrays": CUR + "## Arrays\n\nFixed-size arrays and pointer decay; watch sizes and NUL terminators.\n",
        "slices": CUR + "## Pointer + length\n\nPass `(ptr, len)` pairs; never walk past `len`.\n",
        "maps": CUR + "## Small tables\n\nParallel arrays / linear search keep exercises portable without a hash library.\n",
        "strings": CUR + "## C strings\n\n`const char *`, `printf`, and `strncmp` for comparisons.\n",
        "structs": CUR + "## Structs\n\n`struct` layout, padding, and `typedef` aliases.\n",
        "interfaces": CUR + "## Function pointers\n\nModel interfaces as structs of callbacks (`vtable` style).\n",
        "methods": CUR + "## Methods as conventions\n\n`typedef struct` + functions taking `T *self`.\n",
        "pointers": CUR + "## Pointers\n\n`&`, `*`, `const`, and pointer arithmetic on arrays.\n",
        "errors": CUR + "## Errors\n\nReturn codes, `errno`, and `const char *` messages.\n",
        "concurrency": CUR + "## pthreads\n\n`pthread_create` / `pthread_join` and mutexes for shared state.\n",
        "testing": CUR + "## Testing\n\nStdout exercises stand in for a real unit harness.\n",
        "json": CUR + "## JSON-shaped text\n\nExercises use string composition; production code would link a parser library.\n",
        "time": CUR + "## time.h\n\n`gmtime_r`, `strftime`, and `difftime` for deterministic UTC output.\n",
    }


def hint_cs(h: str) -> str:
    return (
        h.replace("println!", "Console.WriteLine")
        .replace("print!", "Console.Write")
        .replace("let mut", "var")
        .replace("let ", "var ")
        .replace("&str", "string")
        .replace("Vec<", "List<")
    )


def hint_c(h: str) -> str:
    return h.replace("println!", "printf(..., \"\\n\")").replace("Vec", "array")


def desc_cs(d: str) -> str:
    return (
        d.replace("Rust", "C#")
        .replace("rust", "C#")
        .replace("serde_json", "System.Text.Json")
        .replace("serde", "System.Text.Json")
        .replace("chrono", "DateTime / TimeSpan")
        .replace("cargo test", "dotnet test")
    )


def desc_c(d: str) -> str:
    return (
        d.replace("Rust", "C")
        .replace("rust", "C")
        .replace("serde_json", "hand-built JSON or a tiny parser")
        .replace("chrono", "time.h")
    )


def refresh(dest: Path, lang: str) -> None:
    th = theories_cs() if lang == "csharp" else theories_c()
    for path in sorted(dest.glob("*.json")):
        ch = json.loads(path.read_text(encoding="utf-8"))
        cid = ch["id"]
        head = th.get(cid)
        if head:
            ch["theory"] = head
        if cid != "variables":
            ch["description"] = (desc_cs if lang == "csharp" else desc_c)(ch.get("description", ""))
        for ex in ch.get("exercises", []):
            if cid != "variables":
                ex["description"] = (desc_cs if lang == "csharp" else desc_c)(ex.get("description", ""))
                rh = ex.get("hints") or []
                ex["hints"] = [(hint_cs if lang == "csharp" else hint_c)(h) for h in rh]
        path.write_text(json.dumps(ch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    refresh(CS_DIR, "csharp")
    refresh(C_DIR, "c")
    print("refreshed theory/descriptions/hints for C# and C (solutions unchanged)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
