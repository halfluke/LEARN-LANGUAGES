#!/usr/bin/env python3
"""Replace ## Course layout sections in track READMEs from chapters/*.json."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from render_chapter_tables import table_for  # noqa: E402

TRACKS = ("rust", "go", "c", "csharp", "python", "java", "asmx64")
SECTION_RE = re.compile(
    r"## Course layout\n.*?(?=\n## |\Z)",
    re.DOTALL,
)


def course_layout_block(track: str) -> str:
    return (
        "## Course layout\n\n"
        "Chapters live under **`chapters/*.json`** (filename order). "
        "Edit JSON in place. Schema: "
        f"**[../TUTORIAL_PLATFORM.md](../TUTORIAL_PLATFORM.md)**.\n\n"
        f"{table_for(track)}\n"
    )


def main() -> int:
    for track in TRACKS:
        readme = ROOT / track / "README.md"
        text = readme.read_text(encoding="utf-8")
        block = course_layout_block(track)
        if SECTION_RE.search(text):
            text = SECTION_RE.sub(block.rstrip() + "\n\n", text, count=1)
        else:
            print(f"skip {track}: no ## Course layout section", file=sys.stderr)
            continue
        readme.write_text(text, encoding="utf-8")
        print(f"updated {readme}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
