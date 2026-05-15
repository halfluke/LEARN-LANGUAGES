#!/usr/bin/env python3
"""Regenerate LEARN-C# / LEARN-C chapter JSON from LEARN-GO + parity catalog."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GO_CHAPTERS = ROOT / "go" / "chapters"
OUT_CSHARP = ROOT / "csharp" / "chapters"
OUT_C = ROOT / "c" / "chapters"

SKIP_GO_STEMS = frozenset({"05_lifetimes"})
SKIP_C_STEMS = frozenset({"05_lifetimes", "13_packages"})

PRESERVE_CSHARP = frozenset(
    {
        "01_variables.json",
        "18_json.json",
        "19_time.json",
    }
)
PRESERVE_C = frozenset(
    {
        "01_variables.json",
        "16_concurrency.json",
        "17_testing.json",
    }
)

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.parity.catalog import CUR_BANNER, get_chapter_exercises  # noqa: E402
from scripts.refresh_theory_hints_cs_c import theories_c, theories_cs  # noqa: E402

SKIP_CSHARP_IDS = frozenset({"lifetimes"})
SKIP_C_IDS = frozenset({"lifetimes", "packages"})


def _chapter_meta(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _build_chapter(go_ch: dict, lang: str) -> dict:
    cid = go_ch["id"]
    exercises = get_chapter_exercises(cid, lang)
    if not exercises:
        raise SystemExit(f"chapter {cid} has no exercises for {lang}")
    th = (theories_cs() if lang == "csharp" else theories_c()).get(cid, "")
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


def _write(lang: str, out_dir: Path, skip_stems: frozenset[str], preserve: frozenset[str]) -> list[tuple[str, int]]:
    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[tuple[str, int]] = []
    skip_ids = SKIP_CSHARP_IDS if lang == "csharp" else SKIP_C_IDS

    for path in sorted(GO_CHAPTERS.glob("*.json")):
        if path.stem in skip_stems:
            continue
        go_ch = _chapter_meta(path)
        cid = go_ch["id"]
        if cid in skip_ids:
            continue
        dest = out_dir / f"{path.stem}.json"
        if dest.name in preserve:
            ch = json.loads(dest.read_text(encoding="utf-8"))
            written.append((dest.name, len(ch.get("exercises", []))))
            continue
        ported = _build_chapter(go_ch, lang)
        dest.write_text(
            json.dumps(ported, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        written.append((dest.name, ported["exercise_count"]))
    return written


def main() -> int:
    cs_written = _write("csharp", OUT_CSHARP, SKIP_GO_STEMS, PRESERVE_CSHARP)
    c_written = _write("c", OUT_C, SKIP_C_STEMS, PRESERVE_C)

    bad: list[str] = []
    for out_dir in (OUT_CSHARP, OUT_C):
        for p in out_dir.glob("*.json"):
            if not re.match(r"^\d{2}_", p.name):
                bad.append(p.name)
    if bad:
        print("non-prefixed json:", bad, file=sys.stderr)
        return 1

    print("csharp chapters written (or preserved):", len(cs_written))
    for name, n in cs_written:
        print(f"  {name}: {n} exercises")
    print("c chapters written (or preserved):", len(c_written))
    for name, n in c_written:
        print(f"  {name}: {n} exercises")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
