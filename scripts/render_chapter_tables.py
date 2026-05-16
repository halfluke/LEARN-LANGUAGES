#!/usr/bin/env python3
"""Print markdown chapter tables from chapters/*.json (for README Course layout sections)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRACKS = ("rust", "go", "c", "csharp", "python", "java", "asmx64")


def table_for(track: str) -> str:
    chdir = ROOT / track / "chapters"
    rows: list[tuple[int, str, int]] = []
    for i, path in enumerate(sorted(chdir.glob("*.json")), 1):
        data = json.loads(path.read_text(encoding="utf-8"))
        rows.append((i, data.get("title", data["id"]), len(data.get("exercises", []))))
    total_ex = sum(r[2] for r in rows)
    lines = [
        f"**{len(rows)}** chapters, **{total_ex}** exercises — loaded from **`chapters/*.json`** (filename order).",
        "",
        "| # | Chapter | Exercises |",
        "|---|---------|-----------|",
    ]
    for num, title, n in rows:
        lines.append(f"| {num} | {title} | {n} |")
    return "\n".join(lines)


def main() -> int:
    tracks = sys.argv[1:] if len(sys.argv) > 1 else TRACKS
    for track in tracks:
        print(f"## {track}\n")
        print(table_for(track))
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
