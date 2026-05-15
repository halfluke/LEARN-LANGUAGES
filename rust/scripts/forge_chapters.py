#!/usr/bin/env python3
"""Rebuild chapters/*.json from LEARN-GO sources + Rust chapter port modules.

Output filenames follow LEARN-LANGUAGES/CURRICULUM.md (numeric prefix + id).
Rust-only chapters (e.g. ownership, lifetimes) are not produced here—maintain those JSON files by hand.
"""
import json
import pathlib
import sys

MONO_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
ROOT = pathlib.Path(__file__).resolve().parent.parent
GO_CHAPTERS = MONO_ROOT / "go" / "chapters"
OUT_DIR = ROOT / "chapters"

# Canonical on-disk names (must match LEARN-LANGUAGES/CURRICULUM.md).
GO_ID_TO_FILENAME = {
    "variables": "01_variables.json",
    "controlflow": "03_controlflow.json",
    "functions": "04_functions.json",
    "arrays": "06_arrays.json",
    "slices": "07_slices.json",
    "maps": "08_maps.json",
    "strings": "09_strings.json",
    "structs": "10_structs.json",
    "interfaces": "11_interfaces.json",
    "methods": "12_methods.json",
    "packages": "13_packages.json",
    "pointers": "14_pointers.json",
    "errors": "15_errors.json",
    "concurrency": "16_concurrency.json",
    "testing": "17_testing.json",
    "json": "18_json.json",
    "time": "19_time.json",
}

SCRIPTS = pathlib.Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from chapter_ports import BUILDERS  # type: ignore


def main() -> None:
    if not GO_CHAPTERS.is_dir():
        print(
            "Expected LEARN-GO chapters at",
            GO_CHAPTERS,
            "— clone or point GO_CHAPTERS to your copy.",
            file=sys.stderr,
        )
        sys.exit(1)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for path in sorted(GO_CHAPTERS.glob("*.json")):
        go = json.loads(path.read_text(encoding="utf-8"))
        cid = go["id"]
        builder = BUILDERS.get(cid)
        if builder is None:
            print(f"missing port builder for chapter {cid}", file=sys.stderr)
            sys.exit(1)
        out_name = GO_ID_TO_FILENAME.get(cid)
        if not out_name:
            print(f"no GO_ID_TO_FILENAME mapping for chapter {cid}", file=sys.stderr)
            sys.exit(1)
        rust = builder(go)
        out_path = OUT_DIR / out_name
        out_path.write_text(
            json.dumps(rust, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print("wrote", out_path)


if __name__ == "__main__":
    main()
