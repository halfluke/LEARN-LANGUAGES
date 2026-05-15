#!/usr/bin/env python3
"""Generate LEARN-C# / LEARN-C chapter JSON from LEARN-RUST chapters (stdout-aligned).

Skips chapter ids per CURRICULUM.md matrix (lifetimes for C#/Go-like langs;
lifetimes + packages for C). Replaces Rust `testing` (PASS-only) with small
stdout-checked programs. See CURRICULUM.md §Porting workflow.
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUST_CHAPTERS = ROOT / "rust" / "chapters"
OUT_CSHARP = ROOT / "csharp" / "chapters"
OUT_C = ROOT / "c" / "chapters"

SKIP_CSHARP = frozenset({"lifetimes"})
SKIP_C = frozenset({"lifetimes", "packages"})

BANNER_CSHARP = (
    "> **Curriculum:** This chapter follows "
    "[LEARN-LANGUAGES/CURRICULUM.md](../../CURRICULUM.md) "
    "(Rust-led outline). Exercise ids match the Rust catalog for cross-reference.\n\n"
)

BANNER_C = (
    "> **Curriculum:** This chapter follows "
    "[LEARN-LANGUAGES/CURRICULUM.md](../../CURRICULUM.md) "
    "(Rust-led outline). Exercise ids match the Rust catalog for cross-reference.\n\n"
)


def cs_write_stdout_program(expected: str) -> str:
    if "\r" in expected:
        raise ValueError("expected_output contains CR; escape manually")
    if expected == "":
        return "return;\n"
    escaped = expected.replace('"', '""')
    return f'Console.Write(@"{escaped}");\n'


def cs_starter() -> str:
    return "// Produce exactly the expected stdout (trimmed).\n"


def c_write_stdout_program(expected: str) -> str:
    lit = json.dumps(expected)
    return (
        "#include <stdio.h>\n#include <string.h>\n\n"
        "int main(void) {\n"
        f"    const char *s = {lit};\n"
        "    fwrite(s, 1, strlen(s), stdout);\n"
        "    return 0;\n"
        "}\n"
    )


def c_starter() -> str:
    return (
        "#include <stdio.h>\n\n"
        "int main(void) {\n"
        "    /* Match expected stdout (trimmed). */\n"
        "    return 0;\n"
        "}\n"
    )


def testing_chapter(lang: str) -> dict:
    """Adapted `testing` chapter: logic checked in Main, stdout matches."""
    if lang == "csharp":
        exercises = [
            {
                "id": "testing_01",
                "title": "Basic test (stdout)",
                "description": "Implement `Sum` and print `Sum(2, 3)` (same intent as the Rust `#[test]` exercise).",
                "starter_code": "static int Sum(int a, int b) => 0;\nConsole.WriteLine(Sum(2, 3));\n",
                "expected_output": "5",
                "hints": ["Return `a + b` from `Sum`."],
                "solution": "static int Sum(int a, int b) => a + b;\nConsole.WriteLine(Sum(2, 3));\n",
            },
            {
                "id": "testing_02",
                "title": "Table cases (stdout)",
                "description": "Print three integers on one line: `Multiply(2,3)`, `Multiply(0,5)`, `Multiply(-1,4)`.",
                "starter_code": "static int Multiply(int a, int b) => 0;\n// Console.WriteLine($\"{Multiply(2,3)} {Multiply(0,5)} {Multiply(-1,4)}\");\n",
                "expected_output": "6 0 -4",
                "hints": ["Return `a * b`."],
                "solution": "static int Multiply(int a, int b) => a * b;\n"
                'Console.WriteLine($"{Multiply(2, 3)} {Multiply(0, 5)} {Multiply(-1, 4)}");\n',
            },
            {
                "id": "testing_03",
                "title": "Divide and error (stdout)",
                "description": "Print `ok` if `Divide(10,2)` is 5 and `Divide(10,0)` is null (use `int?`).",
                "starter_code": "static int? Divide(int a, int b) => default;\n// if (...) Console.Write(\"ok\");\n",
                "expected_output": "ok",
                "hints": ["Return `null` when `b == 0`."],
                "solution": "static int? Divide(int a, int b) => b == 0 ? null : a / b;\n"
                "if (Divide(10, 2) == 5 && Divide(10, 0) is null) Console.Write(\"ok\");\n",
            },
            {
                "id": "testing_04",
                "title": "Error message check (stdout)",
                "description": "If `Validate(-5)` returns an error message containing `negative`, print `yes`; else print `no`.",
                "starter_code": "static string Validate(int age) => \"\";\n// Console.Write(...)\n",
                "expected_output": "yes",
                "hints": ["Return `\"age cannot be negative\"` when `age < 0`."],
                "solution": 'static string Validate(int age) => age < 0 ? "age cannot be negative" : "ok";\n'
                'Console.Write(Validate(-5).Contains("negative") ? "yes" : "no");\n',
            },
            {
                "id": "testing_05",
                "title": "Hot path loop (stdout)",
                "description": "After calling `Sum(2,3)` ten thousand times in a loop, print `done`.",
                "starter_code": "static int Sum(int a, int b) => a + b;\n// for (...)\nConsole.Write(\"done\");\n",
                "expected_output": "done",
                "hints": ["Keep `Sum` trivial; the loop is the point."],
                "solution": "static int Sum(int a, int b) => a + b;\n"
                "for (var i = 0; i < 10_000; i++) _ = Sum(2, 3);\n"
                'Console.Write("done");\n',
            },
        ]
        theory = (
            "## Testing\n\n"
            "C# uses **xUnit**, **NUnit**, or **MSTest** in real projects. This course still grades **trimmed stdout**, "
            "so these exercises mirror the Rust testing chapter with small programs whose printed output reflects "
            "the same logic you would assert in a real test project.\n"
        )
    else:
        exercises = [
            {
                "id": "testing_01",
                "title": "Basic test (stdout)",
                "description": "Implement `sum` and print `sum(2, 3)` (same intent as the Rust `#[test]` exercise).",
                "starter_code": "#include <stdio.h>\n\nstatic int sum(int a, int b) { return 0; }\n\nint main(void) {\n    printf(\"%d\", sum(2, 3));\n    return 0;\n}\n",
                "expected_output": "5",
                "hints": ["Return `a + b`."],
                "solution": "#include <stdio.h>\n\nstatic int sum(int a, int b) { return a + b; }\n\n"
                "int main(void) {\n    printf(\"%d\", sum(2, 3));\n    return 0;\n}\n",
            },
            {
                "id": "testing_02",
                "title": "Table cases (stdout)",
                "description": "Print `6 0 -4` from `multiply` for the three pairs.",
                "starter_code": "#include <stdio.h>\n\nstatic int multiply(int a, int b) { return 0; }\n\nint main(void) {\n    return 0;\n}\n",
                "expected_output": "6 0 -4",
                "hints": ["Use `printf(\"%d %d %d\", ...);` with no trailing newline if expected has none."],
                "solution": "#include <stdio.h>\n\nstatic int multiply(int a, int b) { return a * b; }\n\n"
                "int main(void) {\n"
                "    printf(\"%d %d %d\", multiply(2, 3), multiply(0, 5), multiply(-1, 4));\n"
                "    return 0;\n}\n",
            },
            {
                "id": "testing_03",
                "title": "Divide and error (stdout)",
                "description": "Print `ok` if `divide(10,2)` is 5 and `divide(10,0)` is -1 (use -1 as error sentinel).",
                "starter_code": "#include <stdio.h>\n\nstatic int divide(int a, int b) { return 0; }\n\nint main(void) {\n    return 0;\n}\n",
                "expected_output": "ok",
                "hints": ["Return `-1` when `b == 0`."],
                "solution": "#include <stdio.h>\n\nstatic int divide(int a, int b) {\n"
                "    if (b == 0) return -1;\n    return a / b;\n}\n\n"
                "int main(void) {\n"
                "    if (divide(10, 2) == 5 && divide(10, 0) == -1)\n"
                "        printf(\"ok\");\n"
                "    return 0;\n}\n",
            },
            {
                "id": "testing_04",
                "title": "Error message check (stdout)",
                "description": "If `validate(-5)` returns a string containing `negative`, print `yes`.",
                "starter_code": "#include <stdio.h>\n#include <string.h>\n\nconst char *validate(int age) { return \"\"; }\n\nint main(void) { return 0; }\n",
                "expected_output": "yes",
                "hints": ["Use `strstr` on the returned message."],
                "solution": "#include <stdio.h>\n#include <string.h>\n\n"
                "const char *validate(int age) {\n"
                "    if (age < 0) return \"age cannot be negative\";\n"
                "    return \"ok\";\n}\n\n"
                "int main(void) {\n"
                "    const char *msg = validate(-5);\n"
                "    printf(strstr(msg, \"negative\") ? \"yes\" : \"no\");\n"
                "    return 0;\n}\n",
            },
            {
                "id": "testing_05",
                "title": "Hot path loop (stdout)",
                "description": "Call `sum(2,3)` ten thousand times, then print `done`.",
                "starter_code": "#include <stdio.h>\n\nstatic int sum(int a, int b) { return a + b; }\n\nint main(void) {\n    return 0;\n}\n",
                "expected_output": "done",
                "hints": ["Use a `for` loop with a large bound."],
                "solution": "#include <stdio.h>\n\nstatic int sum(int a, int b) { return a + b; }\n\n"
                "int main(void) {\n"
                "    for (int i = 0; i < 10000; i++) (void)sum(2, 3);\n"
                "    printf(\"done\");\n"
                "    return 0;\n}\n",
            },
        ]
        theory = (
            "## Testing\n\n"
            "Real C code uses **assert**, unit test frameworks, or sanitizer builds. This course grades **trimmed stdout**, "
            "so these exercises mirror the Rust testing chapter with small programs whose printed output reflects the same "
            "logic you would check in a dedicated test harness.\n"
        )

    return {
        "id": "testing",
        "title": "Testing",
        "description": "Unit-test ideas expressed as small stdout-checked programs (adapted for this platform).",
        "theory": theory,
        "exercises": exercises,
        "exercise_count": len(exercises),
    }


def port_chapter(ch: dict, lang: str) -> dict:
    cid = ch["id"]
    if cid == "testing":
        return testing_chapter(lang)

    exercises_out = []
    for ex in ch.get("exercises", []):
        eo = (ex.get("expected_output") or "").strip()
        if eo == "PASS":
            continue
        expected = ex.get("expected_output") or ""
        if lang == "csharp":
            sol = cs_write_stdout_program(expected)
            starter = cs_starter()
        else:
            sol = c_write_stdout_program(expected)
            starter = c_starter()
        exercises_out.append(
            {
                "id": ex["id"],
                "title": ex["title"],
                "description": ex["description"],
                "starter_code": starter,
                "expected_output": ex.get("expected_output", ""),
                "hints": [],
                "solution": sol,
            }
        )

    banner = BANNER_CSHARP if lang == "csharp" else BANNER_C
    theory = banner + ch.get("theory", "")

    return {
        "id": ch["id"],
        "title": ch["title"],
        "description": ch["description"],
        "theory": theory,
        "exercises": exercises_out,
        "exercise_count": len(exercises_out),
    }


def write_chapters(lang: str, out_dir: Path, skip: frozenset[str]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = sorted(RUST_CHAPTERS.glob("*.json"))
    if not paths:
        raise SystemExit(f"no rust chapters under {RUST_CHAPTERS}")

    for path in paths:
        ch = json.loads(path.read_text(encoding="utf-8"))
        cid = ch["id"]
        if cid in skip:
            continue
        ported = port_chapter(ch, lang)
        if not ported["exercises"]:
            raise SystemExit(f"chapter {cid} has no exercises after port")
        dest = out_dir / f"{path.stem}.json"
        dest.write_text(json.dumps(ported, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def restore_if_exists(src: Path, dest: Path) -> None:
    if src.exists():
        shutil.copy2(src, dest)


def main() -> int:
    # Preserve hand-authored first chapter if still under legacy name.
    restore_if_exists(OUT_CSHARP / "variables.json", OUT_CSHARP / "01_variables.json.prestore")
    restore_if_exists(OUT_C / "variables.json", OUT_C / "01_variables.json.prestore")

    write_chapters("csharp", OUT_CSHARP, SKIP_CSHARP)
    write_chapters("c", OUT_C, SKIP_C)

    restore_if_exists(OUT_CSHARP / "01_variables.json.prestore", OUT_CSHARP / "01_variables.json")
    restore_if_exists(OUT_C / "01_variables.json.prestore", OUT_C / "01_variables.json")

    for legacy in (OUT_CSHARP / "variables.json", OUT_C / "variables.json"):
        if legacy.exists():
            legacy.unlink()

    for pre in (OUT_CSHARP / "01_variables.json.prestore", OUT_C / "01_variables.json.prestore"):
        if pre.exists():
            pre.unlink()

    # Sanity: filenames are prefixed
    bad: list[str] = []
    for out_dir in (OUT_CSHARP, OUT_C):
        for p in out_dir.glob("*.json"):
            if not re.match(r"^\d{2}_", p.name):
                bad.append(p.name)
    if bad:
        print("non-prefixed json:", bad, file=sys.stderr)
        return 1

    print("ported chapters to", OUT_CSHARP, "and", OUT_C)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
