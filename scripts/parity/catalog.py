"""Pedagogical parity catalog: C# and C exercises aligned with LEARN-GO ids."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.parity._builders import BODIES as _GENERATED  # noqa: E402
from scripts.parity._go import go_exercises  # noqa: E402
from scripts.parity.overrides import extend_bodies  # noqa: E402
from scripts.port_chapters_from_rust import testing_chapter  # noqa: E402

_BODIES: dict[str, dict[str, dict[str, dict]]] = {}
for ch, exs in _GENERATED.items():
    _BODIES[ch] = {eid: dict(lang) for eid, lang in exs.items()}
extend_bodies(_BODIES)

CUR_BANNER = (
    "> **Curriculum:** This chapter follows "
    "[LEARN-LANGUAGES/CURRICULUM.md](../../CURRICULUM.md). "
    "Exercise ids are shared across LEARN-* repos for cross-reference.\n\n"
)

_CHAPTER_IDS = frozenset(
    {
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


def _load_preserved_csharp(chapter_id: str) -> list[dict] | None:
    """Hand-authored C# json/time chapters (not regenerated on disk)."""
    stem = {
        "json": "18_json",
        "time": "19_time",
    }.get(chapter_id)
    if not stem:
        return None
    path = ROOT / "csharp" / "chapters" / f"{stem}.json"
    if not path.exists():
        return None
    ch = json.loads(path.read_text(encoding="utf-8"))
    return list(ch.get("exercises", []))


def _adapt_description(desc: str, lang: str) -> str:
    if lang == "csharp":
        return (
            desc.replace("Rust", "C#")
            .replace("rust", "C#")
            .replace("serde_json", "System.Text.Json")
            .replace("serde", "System.Text.Json")
            .replace("chrono", "DateTime / TimeSpan")
            .replace("cargo test", "dotnet test")
            .replace("goroutine", "Task")
            .replace("fmt.Println", "Console.WriteLine")
        )
    return (
        desc.replace("Rust", "C")
        .replace("rust", "C")
        .replace("serde_json", "snprintf / sscanf")
        .replace("serde", "snprintf / sscanf")
        .replace("chrono", "time.h")
        .replace("goroutine", "pthread")
        .replace("fmt.Println", "printf")
    )


def _is_csharp_decl_start(line: str) -> bool:
    s = line.strip()
    if not s or s.startswith("//"):
        return False
    if s.startswith("using ") and "=" not in s:
        return False
    if s.startswith(("unsafe", "try", "for", "foreach", "while", "if", "switch", "await ")):
        return False
    prefixes = (
        "class ",
        "interface ",
        "record ",
        "struct ",
        "enum ",
        "public class ",
        "public interface ",
        "public record ",
        "readonly struct ",
        "static class ",
    )
    if s.startswith(prefixes):
        return True
    if s.startswith("static ") and ("(" in s or "{" in s):
        return True
    return False


def _csharp_reorder_types(body: str) -> str:
    """Type and static member declarations follow top-level statements in Program.cs."""
    lines = body.split("\n")
    code: list[str] = []
    decls: list[str] = []
    in_decl = False
    brace = 0
    seen_brace = False

    def close_decl_if_done(line: str) -> None:
        nonlocal in_decl, brace, seen_brace
        s = line.strip()
        if brace <= 0 and (seen_brace or s.endswith(";")):
            in_decl = False
            seen_brace = False

    for line in lines:
        s = line.strip()
        if in_decl:
            decls.append(line)
            if "{" in line:
                seen_brace = True
            brace += line.count("{") - line.count("}")
            close_decl_if_done(line)
            continue
        if _is_csharp_decl_start(line):
            in_decl = True
            decls.append(line)
            seen_brace = "{" in line
            brace = line.count("{") - line.count("}")
            close_decl_if_done(line)
            continue
        code.append(line)
    if not decls:
        return body
    while code and not code[-1].strip():
        code.pop()
    while decls and not decls[0].strip():
        decls.pop(0)
    if not code:
        return body
    return "\n".join(code + [""] + decls)


def _csharp_solution(body: str) -> str:
    """Prepend usings so single-file Program.cs builds under check_solutions."""
    body = _csharp_reorder_types(body)
    usings: list[str] = []
    if "Channel." in body or "Channel<" in body:
        usings.append("using System.Threading.Channels;")
    if any(tok in body for tok in ("Task.", "Task.Run", "async ", "await ")):
        usings.append("using System.Threading.Tasks;")
    if any(tok in body for tok in (".Select(", ".Sum(", ".Append(", ".OrderBy(")):
        usings.append("using System.Linq;")
    if "List<" in body or "new List" in body:
        usings.append("using System.Collections.Generic;")
    if "CultureInfo" in body:
        usings.append("using System.Globalization;")
    if "Dictionary<" in body or "SortedDictionary<" in body:
        usings.append("using System.Collections.Generic;")
    if "JsonSerializer" in body or "JsonDocument" in body:
        usings.append("using System.Text.Json;")
    if "unsafe" in body and "using System;" not in body:
        usings.append("using System;")
    prefix = "\n".join(dict.fromkeys(usings))
    if not prefix:
        return body
    body_lines = body.split("\n")
    while body_lines and body_lines[0].strip().startswith("using "):
        body_lines.pop(0)
    while body_lines and not body_lines[0].strip():
        body_lines.pop(0)
    return f"{prefix}\n\n" + "\n".join(body_lines)


def _adapt_hints(hints: list[str], lang: str) -> list[str]:
    out: list[str] = []
    for h in hints:
        if lang == "csharp":
            out.append(
                h.replace("println!", "Console.WriteLine")
                .replace("print!", "Console.Write")
                .replace("let mut", "var")
                .replace("let ", "var ")
                .replace("&str", "string")
                .replace("Vec<", "List<")
                .replace("fmt.Println", "Console.WriteLine")
            )
        else:
            out.append(
                h.replace("println!", "printf(..., \"\\n\")")
                .replace("fmt.Println", "printf")
                .replace("Vec", "array")
            )
    return out


def get_chapter_exercises(chapter_id: str, lang: str) -> list[dict]:
    """Return exercise dicts for a chapter id and language (`csharp` or `c`)."""
    if lang not in ("csharp", "c"):
        raise ValueError(f"unsupported lang {lang!r}")
    if chapter_id not in _CHAPTER_IDS:
        raise KeyError(f"unknown chapter_id {chapter_id!r}")

    if chapter_id == "testing":
        return list(testing_chapter(lang)["exercises"])

    if lang == "csharp" and chapter_id in ("json", "time"):
        preserved = _load_preserved_csharp(chapter_id)
        if preserved:
            return preserved

    go_list = go_exercises(chapter_id)
    ch_bodies = _BODIES.get(chapter_id, {})
    out: list[dict] = []
    for go_ex in go_list:
        eid = go_ex["id"]
        expected = go_ex.get("expected_output", "")
        if (expected or "").strip() == "PASS":
            continue
        lang_body = ch_bodies.get(eid, {}).get(lang)
        if not lang_body:
            raise KeyError(f"missing body for {chapter_id}/{eid}/{lang}")
        title = go_ex.get("title", eid)
        desc = _adapt_description(go_ex.get("description", ""), lang)
        hints = _adapt_hints(list(lang_body.get("hints") or go_ex.get("hints") or []), lang)
        if chapter_id == "time" and eid == "time_08":
            expected = (
                "2024-06-01 10:15:30 UTC\n"
                "Hour: 10\n"
                "Minute: 15\n"
                "After +1s: 2024-06-01 10:15:31 UTC"
            )
        if chapter_id == "pointers" and eid == "pointers_01":
            expected = "42"
        if lang == "c" and (chapter_id, eid) == ("interfaces", "interfaces_03"):
            expected = "78.539816339745"
        if lang == "c" and (chapter_id, eid) == ("methods", "methods_07"):
            expected = "78.539816339745\n31.415926535898"
        if lang == "csharp" and (chapter_id, eid) == ("methods", "methods_07"):
            expected = "78.539816339744831\n31.415926535897931"
        if lang == "csharp" and chapter_id == "strings" and eid == "strings_03":
            expected = expected.replace("true", "True")
        solution = lang_body["solution"]
        starter = lang_body["starter_code"]
        if lang == "csharp":
            solution = _csharp_solution(solution)
            starter = _csharp_solution(starter)
        out.append(
            {
                "id": eid,
                "title": title,
                "description": desc,
                "starter_code": starter,
                "expected_output": expected,
                "hints": hints,
                "solution": solution,
            }
        )
    return out
