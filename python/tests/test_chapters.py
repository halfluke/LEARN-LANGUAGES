from pathlib import Path

from learn_python_tui.chapters import default_chapters_dir, load_chapters


def test_load_variables_chapter():
    root = Path(__file__).resolve().parent.parent
    chs = load_chapters(root / "chapters")
    assert len(chs) >= 1
    v = next(c for c in chs if c.id == "variables")
    assert len(v.exercises) == 7
    assert v.exercises[0].id == "variables_01"


def test_default_chapters_dir():
    d = default_chapters_dir()
    assert d.name == "chapters"
    assert any(d.glob("01_variables.json"))
