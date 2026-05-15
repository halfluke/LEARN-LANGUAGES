"""Entry point: prerequisite check + Textual app."""

from __future__ import annotations

import sys

from learn_c_tui.app import LearnCApp
from learn_c_tui.executor import check_cc_available


def main() -> None:
    try:
        check_cc_available()
    except RuntimeError as e:
        print(e, file=sys.stderr)
        raise SystemExit(1) from e
    LearnCApp().run()


if __name__ == "__main__":
    main()
