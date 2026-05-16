#!/usr/bin/env python3
"""Apply expanded chapter theory and strip curriculum boilerplate.

Usage (repository root):
  python3 scripts/apply_chapter_theory.py
  python3 scripts/apply_chapter_theory.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from theory._strip import strip_curriculum_boilerplate  # noqa: E402
from theory.content import THEORY_BY_TRACK  # noqa: E402

TRACKS = ("c", "csharp", "python", "java", "asmx64", "rust", "go")


def patch_track(track: str, *, dry_run: bool) -> tuple[int, int]:
    chapters_dir = ROOT / track / "chapters"
    if not chapters_dir.is_dir():
        return 0, 0
    theories = THEORY_BY_TRACK.get(track, {})
    updated = 0
    for path in sorted(chapters_dir.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        chapter_id = data.get("id", "")
        old = data.get("theory", "")
        new = strip_curriculum_boilerplate(old)
        if chapter_id in theories:
            new = theories[chapter_id]
        if new == old:
            continue
        data["theory"] = new
        updated += 1
        if not dry_run:
            path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return len(list(chapters_dir.glob("*.json"))), updated


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    total = changed = 0
    for track in TRACKS:
        n, u = patch_track(track, dry_run=args.dry_run)
        if u:
            print(f"{track}: updated {u}/{n} chapters")
        total += n
        changed += u
    print(f"done: {changed} files changed ({total} chapters scanned)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
