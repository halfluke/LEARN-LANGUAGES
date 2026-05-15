#!/usr/bin/env python3
"""Regenerate LEARN-Python / LEARN-Java chapter JSON from LEARN-GO + parity catalog."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GO_CHAPTERS = ROOT / "go" / "chapters"
OUT_PYTHON = ROOT / "python" / "chapters"
OUT_JAVA = ROOT / "java" / "chapters"

SKIP_GO_STEMS = frozenset({"05_lifetimes"})

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.parity.py_java_catalog import (  # noqa: E402
    CUR_BANNER,
    get_chapter_exercises,
    theories_java,
    theories_python,
)


def _chapter_meta(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _build_chapter(go_ch: dict, lang: str) -> dict:
    cid = go_ch["id"]
    exercises = get_chapter_exercises(cid, lang)
    if not exercises:
        raise SystemExit(f"chapter {cid} has no exercises for {lang}")
    th_map = theories_python() if lang == "python" else theories_java()
    th = th_map.get(cid, "")
    if cid != "variables" and not th.startswith(">"):
        th = CUR_BANNER + th
    return {
        "id": cid,
        "title": go_ch.get("title", cid.title()),
        "description": go_ch.get("description", ""),
        "theory": th,
        "exercises": exercises,
        "exercise_count": len(exercises),
    }


def _write(lang: str, out_dir: Path) -> list[tuple[str, int]]:
    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[tuple[str, int]] = []

    for path in sorted(GO_CHAPTERS.glob("*.json")):
        if path.stem in SKIP_GO_STEMS:
            continue
        go_ch = _chapter_meta(path)
        cid = go_ch["id"]
        if cid == "lifetimes":
            continue
        dest = out_dir / f"{path.stem}.json"
        ported = _build_chapter(go_ch, lang)
        dest.write_text(
            json.dumps(ported, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        written.append((dest.name, ported["exercise_count"]))
    return written


def main() -> int:
    py_written = _write("python", OUT_PYTHON)
    java_written = _write("java", OUT_JAVA)

    bad: list[str] = []
    for out_dir in (OUT_PYTHON, OUT_JAVA):
        for p in out_dir.glob("*.json"):
            if not re.match(r"^\d{2}_", p.name):
                bad.append(p.name)
    if bad:
        print("non-prefixed json:", bad, file=sys.stderr)
        return 1

    print("python chapters written:", len(py_written))
    for name, n in py_written:
        print(f"  {name}: {n} exercises")
    print("java chapters written:", len(java_written))
    for name, n in java_written:
        print(f"  {name}: {n} exercises")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
