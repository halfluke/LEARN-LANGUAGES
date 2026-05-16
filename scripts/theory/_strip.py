"""Remove maintainer-only curriculum boilerplate from chapter theory text."""

from __future__ import annotations

import re

_CURRICULUM_BLOCKQUOTE = re.compile(
    r"^>\s*\*\*Curriculum:\*\*[^\n]*\n(?:>\s*[^\n]*\n)*\n*",
    re.MULTILINE | re.IGNORECASE,
)

_CURRICULUM_SECTION = re.compile(
    r"\n### Curriculum\n\n[^\n]*(?:\n[^\n#][^\n]*)*",
    re.IGNORECASE,
)


def strip_curriculum_boilerplate(theory: str) -> str:
    text = _CURRICULUM_BLOCKQUOTE.sub("", theory)
    text = _CURRICULUM_SECTION.sub("", text)
    # Collapse excessive blank lines left at the top.
    return text.lstrip("\n")
