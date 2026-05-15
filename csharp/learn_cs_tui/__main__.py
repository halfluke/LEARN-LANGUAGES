"""Entry point: prerequisite check + Textual app."""

from __future__ import annotations

import sys

from learn_cs_tui.app import LearnCSharpApp
from learn_cs_tui.executor import check_dotnet_available


def main() -> None:
    try:
        check_dotnet_available()
    except RuntimeError as e:
        print(e, file=sys.stderr)
        raise SystemExit(1) from e
    LearnCSharpApp().run()


if __name__ == "__main__":
    main()
