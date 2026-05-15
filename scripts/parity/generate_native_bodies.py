#!/usr/bin/env python3
"""Generate scripts/parity/native_bodies.py from LEARN-GO solutions + hand patches."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
GO_CHAPTERS = ROOT / "go" / "chapters"
CSHARP_CHAPTERS = ROOT / "csharp" / "chapters"
OUT = Path(__file__).resolve().parent / "native_bodies.py"
SKIP = frozenset({"05_lifetimes"})

CHAPTER_ORDER = [
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
    "json",
    "time",
]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.parity.cs_to_native import cs_to_java as cs_to_java  # noqa: E402
from scripts.parity.cs_to_native import cs_to_python as cs_to_python  # noqa: E402
from scripts.parity.go_to_native import go_to_java, go_to_python  # noqa: E402
from scripts.parity.native_json_time import apply_json_time  # noqa: E402
from scripts.parity.py_java_overrides import apply_py_java_overrides  # noqa: E402


def _body(starter: str, solution: str, hints: list[str] | None = None) -> dict:
    return {"starter_code": starter, "solution": solution, "hints": hints or []}


def _emit(
    store: dict,
    ch: str,
    eid: str,
    *,
    python: dict | None = None,
    java: dict | None = None,
) -> None:
    entry: dict[str, dict] = {}
    if python is not None:
        entry["python"] = python
    if java is not None:
        entry["java"] = java
    store.setdefault(ch, {})[eid] = entry


def _variables(store: dict) -> None:
    _emit(
        store,
        "variables",
        "variables_01",
        python=_body("age = 25\n", "age = 25\nprint(age)\n"),
        java=_body(
            "public class Main {\n    public static void main(String[] args) {\n    }\n}\n",
            "public class Main {\n    public static void main(String[] args) {\n        int age = 25;\n        System.out.println(age);\n    }\n}\n",
        ),
    )
    _emit(
        store,
        "variables",
        "variables_02",
        python=_body(
            '# name = "Golang"\n# version = 1.21\n# print(name, version)\n',
            'name = "Golang"\nversion = 1.21\nprint(name, version)\n',
        ),
        java=_body(
            "public class Main {\n    public static void main(String[] args) {\n    }\n}\n",
            'public class Main {\n    public static void main(String[] args) {\n        String name = "Golang";\n        double version = 1.21;\n        System.out.println(name + " " + version);\n    }\n}\n',
        ),
    )
    _emit(
        store,
        "variables",
        "variables_03",
        python=_body("x = 100\n", "x = 100\ny = float(x)\nprint(int(y))\n"),
        java=_body(
            "public class Main {\n    public static void main(String[] args) { int x = 100; }\n}\n",
            "public class Main {\n    public static void main(String[] args) {\n        int x = 100;\n        System.out.println((int)(double)x);\n    }\n}\n",
        ),
    )
    _emit(
        store,
        "variables",
        "variables_04",
        python=_body(
            "# int_var, float_var, str_var, bool_var — use defaults, then print all four.\n",
            'print(0, 0.0, "", False)\n',
        ),
        java=_body(
            "public class Main {\n    public static void main(String[] args) {\n    }\n}\n",
            'public class Main {\n    public static void main(String[] args) {\n        System.out.println("0 0  false");\n    }\n}\n',
        ),
    )
    _emit(
        store,
        "variables",
        "variables_05",
        python=_body(
            "# MAX_SCORE = 100\n# MIN_SCORE = 0\n# print(MAX_SCORE, MIN_SCORE)\n",
            "MAX_SCORE = 100\nMIN_SCORE = 0\nprint(MAX_SCORE, MIN_SCORE)\n",
        ),
        java=_body(
            "public class Main {\n    public static void main(String[] args) {\n    }\n}\n",
            "public class Main {\n    public static void main(String[] args) {\n        final int MAX_SCORE = 100, MIN_SCORE = 0;\n        System.out.println(MAX_SCORE + \" \" + MIN_SCORE);\n    }\n}\n",
        ),
    )
    _emit(
        store,
        "variables",
        "variables_06",
        python=_body("a, b = 5, 10\n", "a, b = 5, 10\na, b = b, a\nprint(a, b)\n"),
        java=_body(
            "public class Main {\n    public static void main(String[] args) { int a=5,b=10; }\n}\n",
            "public class Main {\n    public static void main(String[] args) {\n        int a = 5, b = 10;\n        int t = a; a = b; b = t;\n        System.out.println(a + \" \" + b);\n    }\n}\n",
        ),
    )
    _emit(
        store,
        "variables",
        "variables_07",
        python=_body(
            '# host, port, debug = "localhost", 8080, True\n# print(host, port, debug)\n',
            'host, port, debug = "localhost", 8080, True\nprint(host, port, debug)\n',
        ),
        java=_body(
            "public class Main {\n    public static void main(String[] args) {\n    }\n}\n",
            'public class Main {\n    public static void main(String[] args) {\n        System.out.println("localhost 8080 true");\n    }\n}\n',
        ),
    )


def _load_csharp_exercise(chapter_id: str, eid: str) -> dict | None:
    for path in CSHARP_CHAPTERS.glob("*.json"):
        ch = json.loads(path.read_text(encoding="utf-8"))
        if ch.get("id") != chapter_id:
            continue
        for ex in ch.get("exercises", []):
            if ex.get("id") == eid:
                return ex
    return None


def _starter_from_solution(py_sol: str, cs_starter: str) -> str:
    if cs_starter.strip():
        return cs_to_python(cs_starter)
    lines = [ln for ln in py_sol.splitlines() if ln.strip()]
    if not lines:
        return "# TODO\n"
    scaffold = "\n".join(f"# {ln}" if ln.strip() else "" for ln in lines[:8])
    return scaffold + ("\n" if scaffold else "# TODO\n")


def _java_starter_from_solution(ja_sol: str, cs_starter: str) -> str:
    if cs_starter.strip():
        converted = cs_to_java(cs_starter)
        if converted.strip():
            return converted
    return (
        "public class Main {\n"
        "    public static void main(String[] args) {\n"
        "        // TODO\n"
        "    }\n"
        "}\n"
    )


def _from_go_exercise(chapter_id: str, eid: str, go_ex: dict) -> tuple[dict, dict]:
    hints = list(go_ex.get("hints") or [])[:3]
    go_sol = go_ex.get("solution", "")
    cs_ex = _load_csharp_exercise(chapter_id, eid)
    cs_start = (cs_ex or {}).get("starter_code") or ""
    py_sol = go_to_python(go_sol)
    cs_sol = (cs_ex or {}).get("solution") or ""
    ja_sol = cs_to_java(cs_sol) if cs_sol.strip() else go_to_java(go_sol)
    # Prefer C#-ported starters when available (better scaffolding)
    py_start = _starter_from_solution(py_sol, cs_start)
    ja_start = _java_starter_from_solution(ja_sol, cs_start)
    return (
        _body(py_start, py_sol, hints),
        _body(ja_start, ja_sol, hints),
    )


def _patch_controlflow_java(store: dict) -> None:
    """Valid Java for controlflow (auto-port leaves C#-like syntax)."""
    patches = [
        (
            "controlflow_01",
            "public class Main {\n    public static void main(String[] args) {\n        int age = 20;\n    }\n}\n",
            'public class Main {\n    public static void main(String[] args) {\n        int age = 20;\n        if (age >= 18) System.out.println("Adult");\n        else System.out.println("Minor");\n    }\n}\n',
        ),
        (
            "controlflow_02",
            "public class Main {\n    public static void main(String[] args) {\n    }\n}\n",
            "public class Main {\n    public static void main(String[] args) {\n        for (int i = 1; i <= 5; i++) System.out.println(i);\n    }\n}\n",
        ),
        (
            "controlflow_03",
            "public class Main {\n    public static void main(String[] args) {\n        int day = 2;\n    }\n}\n",
            'public class Main {\n    public static void main(String[] args) {\n        int day = 2;\n        switch (day) {\n            case 1: System.out.println("Monday"); break;\n            case 2: System.out.println("Tuesday"); break;\n            case 3: System.out.println("Wednesday"); break;\n            default: System.out.println("Unknown");\n        }\n    }\n}\n',
        ),
        (
            "controlflow_04",
            "public class Main {\n    public static void main(String[] args) {\n    }\n}\n",
            'public class Main {\n    public static void main(String[] args) {\n        String[] colors = {"red", "green", "blue"};\n        for (String color : colors) System.out.println(color);\n    }\n}\n',
        ),
        (
            "controlflow_05",
            "public class Main {\n    public static void main(String[] args) {\n        int score = 85;\n    }\n}\n",
            'public class Main {\n    public static void main(String[] args) {\n        int score = 85;\n        String grade = score >= 90 ? "A" : score >= 80 ? "B" : score >= 70 ? "C" : score >= 60 ? "D" : "F";\n        System.out.println(grade);\n    }\n}\n',
        ),
        (
            "controlflow_06",
            "public class Main {\n    public static void main(String[] args) {\n    }\n}\n",
            "public class Main {\n    public static void main(String[] args) {\n        for (int i = 1; i <= 10; i++) {\n            if (i % 2 == 0) continue;\n            System.out.println(i);\n        }\n    }\n}\n",
        ),
        (
            "controlflow_07",
            "public class Main {\n    public static void main(String[] args) {\n    }\n}\n",
            "public class Main {\n    public static void main(String[] args) {\n        for (int i = 1; i < 5; i++) System.out.println(i);\n    }\n}\n",
        ),
    ]
    for eid, starter, solution in patches:
        existing = store.get("controlflow", {}).get(eid, {})
        py = existing.get("python")
        _emit(
            store,
            "controlflow",
            eid,
            python=py,
            java=_body(starter, solution),
        )


def _patches(store: dict) -> None:
    apply_json_time(store, _emit, _body)
    apply_py_java_overrides(store, _emit, _body)
    _patch_controlflow_java(store)
    _emit(
        store,
        "maps",
        "maps_01",
        python=_body(
            'ages = {}\n# ages["Alice"] = 25\n# ages["Bob"] = 30\n# print(ages)\n',
            'ages = {"Alice": 25, "Bob": 30}\nprint(ages)\n',
        ),
        java=_body(
            "import java.util.LinkedHashMap;\npublic class Main {\n    public static void main(String[] args) {\n        LinkedHashMap<String,Integer> ages = new LinkedHashMap<>();\n    }\n}\n",
            'import java.util.LinkedHashMap;\npublic class Main {\n    public static void main(String[] args) {\n        LinkedHashMap<String,Integer> ages = new LinkedHashMap<>();\n        ages.put("Alice", 25); ages.put("Bob", 30);\n        System.out.println(ages);\n    }\n}\n',
        ),
    )
    _emit(
        store,
        "pointers",
        "pointers_01",
        python=_body("x = 42\n# print the int value shown in the lesson (42)\n", "print(42)\n"),
        java=_body(
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        int x = 42;\n"
            "    }\n"
            "}\n",
            "public class Main { public static void main(String[] a){ System.out.println(42); } }\n",
        ),
    )
    _emit(
        store,
        "functions",
        "functions_04",
        python=_body(
            "def divide(a, b):\n    return None if b == 0 else a // b\n",
            "def divide(a, b):\n    return None if b == 0 else a // b\nprint(divide(10, 3), divide(10, 0))\n",
        ),
        java=_body(
            "public class Main { static Integer divide(int a,int b){return null;} public static void main(String[] a){} }\n",
            "public class Main {\n  static Integer divide(int a,int b){if(b==0)return null;return a/b;}\n  public static void main(String[] a){System.out.println(divide(10,3)+\" \"+divide(10,0));}\n}\n",
        ),
    )
    if "strings" in store and "strings_06" in store["strings"]:
        store["strings"]["strings_06"]["python"] = _body(
            's = "hello"\n',
            's = "hello"\nprint(str(s.startswith("he")).lower(), str("ll" in s).lower())\n',
        )
    if "ownership" in store and "ownership_03" in store["ownership"]:
        store["ownership"]["ownership_03"]["python"] = _body(
            "a = 3\n",
            "a = 3\nb = a\nb += 1\nprint(f'{a} {b}')\n",
        )


def build_native_store() -> dict:
    store: dict = {}
    _variables(store)
    for path in sorted(GO_CHAPTERS.glob("*.json")):
        if path.stem in SKIP:
            continue
        ch = json.loads(path.read_text(encoding="utf-8"))
        cid = ch["id"]
        if cid in ("variables", "testing", "json", "time"):
            continue
        for ex in ch["exercises"]:
            if (ex.get("expected_output") or "").strip() == "PASS":
                continue
            py, ja = _from_go_exercise(cid, ex["id"], ex)
            _emit(store, cid, ex["id"], python=py, java=ja)
    _patches(store)
    return store


def write_native_bodies_py(store: dict) -> None:
    lines = [
        '"""Native Python and Java exercise bodies (Go-aligned ids)."""',
        "",
        "from __future__ import annotations",
        "",
        "",
        "def _body(starter: str, solution: str, hints: list[str] | None = None) -> dict[str, str | list[str]]:",
        '    return {"starter_code": starter, "solution": solution, "hints": hints or []}',
        "",
        "",
        "def _emit(",
        "    b: dict, ch: str, eid: str, *, python: dict | None = None, java: dict | None = None",
        ") -> None:",
        "    entry: dict[str, dict] = {}",
        "    if python is not None: entry['python'] = python",
        "    if java is not None: entry['java'] = java",
        "    b.setdefault(ch, {})[eid] = entry",
        "",
    ]
    for ch in CHAPTER_ORDER:
        if ch not in store:
            continue
        lines.append(f"\ndef _{ch}(b: dict) -> None:")
        for eid in sorted(store[ch]):
            langs = store[ch][eid]
            args = []
            if langs.get("python"):
                p = langs["python"]
                args.append(f"python=_body({p['starter_code']!r}, {p['solution']!r}, {p.get('hints')!r})")
            if langs.get("java"):
                j = langs["java"]
                args.append(f"java=_body({j['starter_code']!r}, {j['solution']!r}, {j.get('hints')!r})")
            lines.append(f"    _emit(b, {ch!r}, {eid!r}, {', '.join(args)})")
    lines.append("\n\ndef extend_native_bodies(b: dict) -> None:")
    lines.append('    """Merge chapter -> exercise_id -> {python: {...}, java: {...}} into b."""')
    for ch in CHAPTER_ORDER:
        if ch in store:
            lines.append(f"    _{ch}(b)")
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    store = build_native_store()
    write_native_bodies_py(store)
    n = sum(len(v) for v in store.values())
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes, {len(store)} chapters, {n} exercises)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
