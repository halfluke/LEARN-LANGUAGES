#!/usr/bin/env python3
"""Rewrite exercise description/title text ported from Go into track-idiomatic copy."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRACKS = ("python", "java", "csharp", "c")


def _sub(pattern: str, repl: str, text: str) -> str:
    return re.sub(pattern, repl, text)


def port_text(text: str, track: str) -> str:
    if not text:
        return text
    s = text

    # Shared cleanups
    s = _sub(r"\bGo's\b", "This language's", s)
    lang_name = {"python": "Python", "java": "Java", "csharp": "C#", "c": "C"}[track]
    s = _sub(r"\bGo\b", lang_name, s)
    s = _sub(r"\bGolang\b", lang_name, s)
    s = re.sub(r"\bgoroutines?\b", "thread", s, flags=re.IGNORECASE)
    s = s.replace("Pythonroutine", "thread")
    s = s.replace("Javaroutine", "thread")
    s = _sub(r"\bfloat64\b", "float" if track == "python" else "double", s)
    s = _sub(r"\bfmt\.(Println|Print|Printf|Sprintf|Errorf|Fprintln)\b", "print", s)
    s = _sub(r"\bmake\(map\[string\](\w+)\)", r"empty dict", s)
    s = _sub(r"map\[string\](\w+)", r"dict", s)
    s = _sub(r"\[\](\w+)\{", r"list[", s)
    s = _sub(r"\[(\d+)\](\w+)\{", r"[", s)
    s = _sub(r" := ", " = ", s)
    s = _sub(r"for-range", "for ... in", s)
    s = _sub(r"make\(chan string\)", "a queue", s)
    s = _sub(r"interface\{\}", "object" if track == "python" else "Object", s)
    s = _sub(r"Write\(\[\]byte\) int", "write bytes", s)
    s = _sub(r"Area\(\) float64", "area() method", s)

    if track == "python":
        s = s.replace("switch statement", "match statement (Python 3.10+)")
        s = s.replace("[]rune", "list or string reversal")
        s = s.replace("b++", "b += 1")
        s = _sub(r"Create (\w+) = make\(\[\]int, (\d+), (\d+)\)", r"Create list \1 with length/capacity", s)
    elif track == "java":
        s = s.replace("match statement (Python 3.10+)", "switch expression")
        s = s.replace("print", "System.out.println")
        s = s.replace("dict", "HashMap")
        s = s.replace("list[", "int[] {")
    elif track == "csharp":
        s = s.replace("dict", "Dictionary")
        s = s.replace("print", "Console.WriteLine")
    elif track == "c":
        s = s.replace("dict", "parallel key/value arrays")
        s = s.replace("HashMap", "parallel key/value arrays")
        s = s.replace("Create list", "Use a C array or loop")
        s = s.replace("match statement", "switch statement")

    return s


def port_track(track: str, *, dry_run: bool) -> int:
    n = 0
    for path in sorted((ROOT / track / "chapters").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        changed = False
        for ex in data.get("exercises", []):
            for field in ("title", "description"):
                old = ex.get(field, "")
                if not isinstance(old, str):
                    continue
                new = port_text(old, track)
                if new != old:
                    ex[field] = new
                    changed = True
        if changed:
            n += 1
            if not dry_run:
                path.write_text(
                    json.dumps(data, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8",
                )
    return n


def main() -> int:
    for track in TRACKS:
        updated = port_track(track, dry_run=False)
        print(f"{track}: updated exercise text in {updated} chapter files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
