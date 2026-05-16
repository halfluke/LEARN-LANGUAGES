#!/usr/bin/env python3
"""Apply idiomatic per-track hints from scripts/hints/<track>.json into chapter JSON."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRACKS = ("python", "java", "csharp", "c", "rust")


def load_hints(track: str) -> dict[str, dict]:
    path = ROOT / "scripts" / "hints" / f"{track}.json"
    if not path.is_file():
        raise FileNotFoundError(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected object at root")
    return data


def apply_track(track: str, *, dry_run: bool) -> tuple[int, int, list[str]]:
    hints_by_id = load_hints(track)
    chapters_dir = ROOT / track / "chapters"
    updated = 0
    missing: list[str] = []
    for path in sorted(chapters_dir.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        changed = False
        for ex in data.get("exercises", []):
            ex_id = ex.get("id", "")
            entry = hints_by_id.get(ex_id)
            if entry is None:
                missing.append(ex_id)
                continue
            new_hints = entry.get("hints")
            if not isinstance(new_hints, list) or not new_hints:
                missing.append(ex_id)
                continue
            if ex.get("hints") != new_hints:
                ex["hints"] = new_hints
                changed = True
        if changed:
            updated += 1
            if not dry_run:
                path.write_text(
                    json.dumps(data, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8",
                )
    return len(list(chapters_dir.glob("*.json"))), updated, missing


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    any_missing = False
    for track in TRACKS:
        total, updated, missing = apply_track(track, dry_run=args.dry_run)
        print(f"{track}: updated {updated}/{total} chapter files")
        if missing:
            any_missing = True
            print(f"  missing hints for {len(missing)} exercises: {missing[:5]}{'...' if len(missing) > 5 else ''}")
    if any_missing:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
