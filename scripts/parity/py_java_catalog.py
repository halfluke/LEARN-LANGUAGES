"""Pedagogical parity catalog: Python and Java exercises aligned with LEARN-GO ids."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.parity._go import go_exercises  # noqa: E402
from scripts.parity.native_bodies import extend_native_bodies  # noqa: E402

_BODIES: dict[str, dict[str, dict[str, dict]]] = {}
extend_native_bodies(_BODIES)

CUR_BANNER = (
    "> **Curriculum:** This chapter follows "
    "[LEARN-LANGUAGES/CURRICULUM.md](../../CURRICULUM.md). "
    "Exercise ids are shared across LEARN-* repos for cross-reference.\n\n"
)

_CHAPTER_IDS = frozenset(
    {
        "variables",
        "ownership",
        "controlflow",
        "functions",
        "arrays",
        "slices",
        "maps",
        "strings",
        "structs",
        "interfaces",
        "methods",
        "packages",
        "pointers",
        "errors",
        "concurrency",
        "testing",
        "json",
        "time",
    }
)

# (chapter_id, exercise_id) -> expected_output override per language
_EXPECTED_OVERRIDES: dict[tuple[str, str, str], str] = {
    ("python", "maps", "maps_01"): "{'Alice': 25, 'Bob': 30}",
    ("python", "maps", "maps_03"): "{'1': 'One', '2': 'Two'}",
    ("python", "maps", "maps_04"): "{'a': 1, 'c': 3}",
    ("java", "maps", "maps_01"): "{Alice=25, Bob=30}",
    ("java", "maps", "maps_03"): "{1=One, 2=Two}",
    ("java", "maps", "maps_04"): "{a=1, c=3}",
    ("python", "strings", "strings_06"): "true true",
    ("java", "strings", "strings_06"): "true true",
    ("python", "pointers", "pointers_01"): "42",
    ("java", "pointers", "pointers_01"): "42",
    ("python", "functions", "functions_04"): "3 None",
    ("java", "functions", "functions_04"): "3 null",
    ("python", "methods", "methods_07"): "78.53981633974483\n31.41592653589793",
    ("java", "methods", "methods_07"): "78.53981633974483\n31.41592653589793",
    ("python", "variables", "variables_04"): "0 0.0  False",
    ("python", "variables", "variables_07"): "localhost 8080 True",
    ("python", "json", "json_09"): "info\n{\"user\":\"alice\",\"action\":\"login\"}",
    ("python", "time", "time_08"): (
        "2024-06-01 10:15:30 UTC\nHour: 10\nMinute: 15\nAfter +1s: 2024-06-01 10:15:31 UTC"
    ),
    ("java", "time", "time_08"): (
        "2024-06-01 10:15:30 UTC\nHour: 10\nMinute: 15\nAfter +1s: 2024-06-01 10:15:31 UTC"
    ),
}


def theories_python() -> dict[str, str]:
    return {
        "variables": "## Variables in Python 3\n\nBindings use `=`; types are dynamic. Use `print()` for stdout. Constants are convention (`MAX = 100`), not enforced.\n",
        "ownership": CUR_BANNER
        + "## References vs values\n\nLists and dicts are mutable references; integers and strings behave like copied values for assignment. This chapter maps Go ownership ideas to Python’s object model.\n",
        "controlflow": CUR_BANNER + "## Control flow\n\n`if`/`elif`/`else`, `for` and `while`, `break`, `continue`, and `match` (3.10+) where useful.\n",
        "functions": CUR_BANNER + "## Functions\n\n`def`, parameters, `return`, and closures that capture outer names.\n",
        "arrays": CUR_BANNER + "## Lists as arrays\n\nUse fixed-length patterns with lists; format with f-strings or `join` for checker-stable output.\n",
        "slices": CUR_BANNER + "## Slicing\n\n`seq[start:stop]`, negative indices, and `len()` mirror Go slice ergonomics on lists.\n",
        "maps": CUR_BANNER + "## Dicts\n\n`dict` literals, `in`, `del`, and iteration with `.items()`.\n",
        "strings": CUR_BANNER + "## Strings\n\nImmutable `str`, slicing, methods like `.startswith`, and f-strings for formatting.\n",
        "structs": CUR_BANNER + "## Data carriers\n\n`dataclass`, simple classes, or tuples for grouped fields.\n",
        "interfaces": CUR_BANNER + "## Duck typing\n\nProtocols are implicit; use functions and `isinstance` where the exercise needs dispatch.\n",
        "methods": CUR_BANNER + "## Methods\n\nInstance methods take `self`; `@staticmethod` / `@classmethod` when appropriate.\n",
        "packages": CUR_BANNER
        + "## Modules (concept)\n\nReal code splits across files with `import`. These exercises keep helpers in one script and note where a module boundary would go.\n",
        "pointers": CUR_BANNER + "## References\n\nLists and mutable objects model indirection; avoid printing `id()` unless the exercise asks for identity.\n",
        "errors": CUR_BANNER + "## Exceptions\n\n`try`/`except`, raising `ValueError`/`RuntimeError`, and exception chaining with `raise ... from`.\n",
        "concurrency": CUR_BANNER + "## Threading\n\n`threading.Thread` for background work; join before printing final lines for stable stdout.\n",
        "testing": CUR_BANNER
        + "## Testing\n\nProduction code uses `pytest` or `unittest`. Here, small scripts print the same outcomes you would assert in tests.\n",
        "json": CUR_BANNER + "## JSON\n\nstdlib `json.dumps` / `json.loads` with `separators` when compact output must match Go.\n",
        "time": CUR_BANNER + "## Time\n\n`datetime`, `timedelta`, and `zoneinfo` for aware instants and formatting.\n",
    }


def theories_java() -> dict[str, str]:
    return {
        "variables": "## Variables in Java 17\n\nDeclare types explicitly (`int`, `String`, `boolean`). Use `System.out.println` for stdout.\n",
        "ownership": CUR_BANNER
        + "## References vs primitives\n\nPrimitives copy by value; objects share references. `String` is immutable like Go strings.\n",
        "controlflow": CUR_BANNER + "## Control flow\n\n`if`/`else`, `switch`, `for`, `while`, `break`, and `continue`.\n",
        "functions": CUR_BANNER + "## Methods\n\n`static` helpers in `Main` model file-scope functions; overloads and `varargs` where needed.\n",
        "arrays": CUR_BANNER + "## Arrays\n\n`int[]`, enhanced `for`, and `Arrays.toString` or manual formatting for stable output.\n",
        "slices": CUR_BANNER + "## Array views\n\nUse indices and `Arrays.copyOfRange` instead of Go slices.\n",
        "maps": CUR_BANNER + "## Hash maps\n\n`HashMap` for key/value storage; `toString()` format differs from Go—see checker overrides.\n",
        "strings": CUR_BANNER + "## Strings\n\n`String` methods, `StringBuilder` for building text, and `formatted`/`+` for output.\n",
        "structs": CUR_BANNER + "## Records and classes\n\nSimple classes or records hold grouped fields.\n",
        "interfaces": CUR_BANNER + "## Interfaces\n\n`interface` + implementing classes for polymorphism.\n",
        "methods": CUR_BANNER + "## Instance methods\n\nReceivers are explicit instance methods; use `static` helpers in `Main` for small exercises.\n",
        "packages": CUR_BANNER
        + "## Packages (concept)\n\nReal projects use packages and imports; exercises use `static` methods in `Main` as stand-ins.\n",
        "pointers": CUR_BANNER + "## References\n\nObject variables are references; primitives are values. Print data, not default `toString()` of wrappers unless asked.\n",
        "errors": CUR_BANNER + "## Exceptions\n\n`try`/`catch`, custom exceptions, and `getCause()` for wrapped errors.\n",
        "concurrency": CUR_BANNER + "## Threads\n\n`Thread`, `ExecutorService`, and joining tasks for deterministic stdout.\n",
        "testing": CUR_BANNER
        + "## Testing\n\nJUnit is the norm; these exercises use stdout to mirror test assertions.\n",
        "json": CUR_BANNER + "## JSON without libraries\n\nBuild and parse JSON with `StringBuilder`, `String.split`, and careful escaping—no `org.json`.\n",
        "time": CUR_BANNER + "## java.time\n\n`ZonedDateTime`, `Duration`, and `DateTimeFormatter` for instants and durations.\n",
    }


def _adapt_description(desc: str, lang: str) -> str:
    if lang == "python":
        return (
            desc.replace("Go", "Python")
            .replace("go", "Python")
            .replace("fmt.Println", "print")
            .replace("fmt.Print", "print")
            .replace("goroutine", "thread")
            .replace("package main", "# script")
            .replace("serde_json", "json")
            .replace("chrono", "datetime")
        )
    return (
        desc.replace("Go", "Java")
        .replace("go", "Java")
        .replace("fmt.Println", "System.out.println")
        .replace("fmt.Print", "System.out.print")
        .replace("goroutine", "Thread")
        .replace("package main", "public class Main")
        .replace("serde_json", "hand-built JSON")
        .replace("chrono", "java.time")
    )


def _adapt_hints(hints: list[str], lang: str) -> list[str]:
    out: list[str] = []
    for h in hints:
        if lang == "python":
            out.append(
                h.replace("Console.WriteLine", "print")
                .replace("Console.Write", "print")
                .replace("var ", "")
                .replace("fmt.Println", "print")
                .replace("Dictionary<", "dict")
                .replace("List<", "list")
            )
        else:
            out.append(
                h.replace("Console.WriteLine", "System.out.println")
                .replace("Console.Write", "System.out.print")
                .replace("var ", "")
                .replace("fmt.Println", "System.out.println")
                .replace("Dictionary<", "HashMap<")
                .replace("List<", "ArrayList<")
            )
    return out


def testing_exercises_python() -> list[dict]:
    return [
        {
            "id": "testing_01",
            "title": "Basic test (stdout)",
            "description": "Implement `sum` and print `sum(2, 3)` (same intent as the Go `testing` exercise).",
            "starter_code": "def sum(a, b):\n    return 0\n\n# print(sum(2, 3))\n",
            "expected_output": "5",
            "hints": ["Return `a + b`."],
            "solution": "def sum(a, b):\n    return a + b\n\nprint(sum(2, 3))\n",
        },
        {
            "id": "testing_02",
            "title": "Table cases (stdout)",
            "description": "Print `6 0 -4` from `multiply` for (2,3), (0,5), (-1,4).",
            "starter_code": "def multiply(a, b):\n    return 0\n\n",
            "expected_output": "6 0 -4",
            "hints": ["Use one `print` with three values."],
            "solution": "def multiply(a, b):\n    return a * b\n\n"
            "print(multiply(2, 3), multiply(0, 5), multiply(-1, 4))\n",
        },
        {
            "id": "testing_03",
            "title": "Divide and error (stdout)",
            "description": "Print `ok` if `divide(10,2)` is 5 and `divide(10,0)` is `None`.",
            "starter_code": "def divide(a, b):\n    return None\n\n",
            "expected_output": "ok",
            "hints": ["Return `None` when `b == 0`."],
            "solution": "def divide(a, b):\n    if b == 0:\n        return None\n    return a // b\n\n"
            "if divide(10, 2) == 5 and divide(10, 0) is None:\n    print('ok')\n",
        },
        {
            "id": "testing_04",
            "title": "Error message check (stdout)",
            "description": "If `validate(-5)` raises `ValueError` with `negative` in the message, print `yes`.",
            "starter_code": "def validate(age):\n    pass\n\n",
            "expected_output": "yes",
            "hints": ["`raise ValueError('age cannot be negative')` when `age < 0`."],
            "solution": "def validate(age):\n    if age < 0:\n        raise ValueError('age cannot be negative')\n\n"
            "try:\n    validate(-5)\nexcept ValueError as e:\n    print('yes' if 'negative' in str(e) else 'no')\n",
        },
        {
            "id": "testing_05",
            "title": "Hot path loop (stdout)",
            "description": "Call `sum(2,3)` ten thousand times, then print `done`.",
            "starter_code": "def sum(a, b):\n    return a + b\n\n",
            "expected_output": "done",
            "hints": ["`for _ in range(10000): sum(2, 3)`"],
            "solution": "def sum(a, b):\n    return a + b\n\n"
            "for _ in range(10000):\n    sum(2, 3)\nprint('done', end='')\n",
        },
    ]


def testing_exercises_java() -> list[dict]:
    return [
        {
            "id": "testing_01",
            "title": "Basic test (stdout)",
            "description": "Implement `sum` and print `sum(2, 3)`.",
            "starter_code": "public class Main {\n    static int sum(int a, int b) { return 0; }\n    public static void main(String[] args) {\n    }\n}\n",
            "expected_output": "5",
            "hints": ["Return `a + b` from `sum`."],
            "solution": "public class Main {\n    static int sum(int a, int b) { return a + b; }\n    public static void main(String[] args) {\n        System.out.println(sum(2, 3));\n    }\n}\n",
        },
        {
            "id": "testing_02",
            "title": "Table cases (stdout)",
            "description": "Print `6 0 -4` from `multiply` for three pairs.",
            "starter_code": "public class Main {\n    static int multiply(int a, int b) { return 0; }\n    public static void main(String[] args) {\n    }\n}\n",
            "expected_output": "6 0 -4",
            "hints": ["`System.out.println(a + \" \" + b + \" \" + c);`"],
            "solution": "public class Main {\n    static int multiply(int a, int b) { return a * b; }\n    public static void main(String[] args) {\n"
            '        System.out.println(multiply(2, 3) + " " + multiply(0, 5) + " " + multiply(-1, 4));\n'
            "    }\n}\n",
        },
        {
            "id": "testing_03",
            "title": "Divide and error (stdout)",
            "description": "Print `ok` if `divide(10,2)` is 5 and `divide(10,0)` is null.",
            "starter_code": "public class Main {\n    static Integer divide(int a, int b) { return null; }\n    public static void main(String[] args) {\n    }\n}\n",
            "expected_output": "ok",
            "hints": ["Return `null` when `b == 0`."],
            "solution": "public class Main {\n    static Integer divide(int a, int b) {\n        if (b == 0) return null;\n        return a / b;\n    }\n    public static void main(String[] args) {\n"
            "        if (divide(10, 2) == 5 && divide(10, 0) == null) System.out.print(\"ok\");\n"
            "    }\n}\n",
        },
        {
            "id": "testing_04",
            "title": "Error message check (stdout)",
            "description": "If `validate(-5)` throws with `negative` in the message, print `yes`.",
            "starter_code": "public class Main {\n    static void validate(int age) {}\n    public static void main(String[] args) {\n    }\n}\n",
            "expected_output": "yes",
            "hints": ["`throw new IllegalArgumentException(\"age cannot be negative\");`"],
            "solution": "public class Main {\n    static void validate(int age) {\n"
            '        if (age < 0) throw new IllegalArgumentException("age cannot be negative");\n'
            "    }\n    public static void main(String[] args) {\n"
            "        try {\n            validate(-5);\n        } catch (IllegalArgumentException e) {\n"
            '            System.out.print(e.getMessage().contains("negative") ? "yes" : "no");\n'
            "        }\n    }\n}\n",
        },
        {
            "id": "testing_05",
            "title": "Hot path loop (stdout)",
            "description": "Call `sum(2,3)` ten thousand times, then print `done`.",
            "starter_code": "public class Main {\n    static int sum(int a, int b) { return a + b; }\n    public static void main(String[] args) {\n    }\n}\n",
            "expected_output": "done",
            "hints": ["Use a `for` loop with 10_000 iterations."],
            "solution": "public class Main {\n    static int sum(int a, int b) { return a + b; }\n    public static void main(String[] args) {\n"
            "        for (int i = 0; i < 10000; i++) sum(2, 3);\n"
            '        System.out.print("done");\n'
            "    }\n}\n",
        },
    ]


def _expected_for(chapter_id: str, eid: str, lang: str, go_default: str) -> str:
    key = (lang, chapter_id, eid)
    if key in _EXPECTED_OVERRIDES:
        return _EXPECTED_OVERRIDES[key]
    if lang == "java" and chapter_id == "strings" and eid == "strings_03":
        return go_default.replace("true", "true")
    return go_default


def get_chapter_exercises(chapter_id: str, lang: str) -> list[dict]:
    """Return exercise dicts for a chapter id and language (`python` or `java`)."""
    if lang not in ("python", "java"):
        raise ValueError(f"unsupported lang {lang!r}")
    if chapter_id not in _CHAPTER_IDS:
        raise KeyError(f"unknown chapter_id {chapter_id!r}")

    if chapter_id == "testing":
        return list(
            testing_exercises_python() if lang == "python" else testing_exercises_java()
        )

    go_list = go_exercises(chapter_id)
    ch_bodies = _BODIES.get(chapter_id, {})
    out: list[dict] = []
    for go_ex in go_list:
        eid = go_ex["id"]
        expected_go = go_ex.get("expected_output", "")
        if (expected_go or "").strip() == "PASS":
            continue
        lang_body = ch_bodies.get(eid, {}).get(lang)
        if not lang_body:
            raise KeyError(f"missing body for {chapter_id}/{eid}/{lang}")
        expected = _expected_for(chapter_id, eid, lang, expected_go)
        title = go_ex.get("title", eid)
        desc = _adapt_description(go_ex.get("description", ""), lang)
        hints = _adapt_hints(list(lang_body.get("hints") or go_ex.get("hints") or []), lang)
        starter = lang_body["starter_code"]
        if starter is None or not str(starter).strip():
            if lang == "python":
                starter = "# TODO: see description and hints below.\n"
            else:
                starter = (
                    "public class Main {\n"
                    "    public static void main(String[] args) {\n"
                    "        // TODO\n"
                    "    }\n"
                    "}\n"
                )
        out.append(
            {
                "id": eid,
                "title": title,
                "description": desc,
                "starter_code": starter,
                "expected_output": expected,
                "hints": hints,
                "solution": lang_body["solution"],
            }
        )
    return out
