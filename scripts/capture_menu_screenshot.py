#!/usr/bin/env python3
"""Capture docs/assets/tui-screenshot.svg from the hub menu (Textual run_test)."""

from __future__ import annotations

import asyncio
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from learn_languages.app import LearnLanguagesMenu  # noqa: E402


async def main() -> None:
    app = LearnLanguagesMenu()
    async with app.run_test(size=(92, 28)) as pilot:
        await pilot.pause()
        out = ROOT / "docs" / "assets"
        out.mkdir(parents=True, exist_ok=True)
        dest = out / "tui-screenshot.svg"
        saved = Path(app.save_screenshot(path=str(out)))
        if saved != dest and saved.exists():
            shutil.copy2(saved, dest)
            saved.unlink(missing_ok=True)
        print("wrote", dest)


if __name__ == "__main__":
    asyncio.run(main())
