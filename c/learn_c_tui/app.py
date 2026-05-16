"""Textual TUI: chapter list, theory, exercises, C buffer, compile/run, hints."""

from __future__ import annotations

import shutil
import tempfile
import threading
from pathlib import Path
from typing import Literal

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, VerticalScroll
from textual.events import Key
from textual.widgets import Footer, Header, Static

from learn_c_tui.chapters import Chapter, Exercise, load_chapters
from learn_c_tui.editor import launch_editor
from learn_c_tui.executor import ExecutionResult, execute_code
from learn_c_tui.progress import ProgressStore
from learn_c_tui.validator import Validator, ValidationResult

Route = Literal[
    "list",
    "jump",
    "theory",
    "exercises",
    "code",
    "result",
    "stats",
    "help",
]


class LearnCApp(App[None]):
    CSS = """
    #body { width: 100%; height: 1fr; padding: 0 1; }
    #code_view { height: 1fr; border: solid $primary; padding: 1; }
    #title_line { text-style: bold; margin-bottom: 1; }
    """

    BINDINGS = [
        Binding("ctrl+c", "quit", "", show=False),
        Binding("q", "quit", "Quit"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.chapters: list[Chapter] = []
        self.route: Route = "list"
        self.chapter_cursor = 0
        self.selected_chapter: int | None = None
        self.selected_exercise: int | None = None
        self.exercise_cursor = 0
        self.theory_scroll = 0
        self.current_code = ""
        self.hints_used = 0
        self.validation: ValidationResult | None = None
        self.last_exec: ExecutionResult | None = None
        self.progress = ProgressStore()
        self.validator = Validator()
        self._build_dir: Path | None = None
        self._run_busy = False

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Container(id="body")
        yield Footer()

    def on_mount(self) -> None:
        self.title = "Learn C"
        self.sub_title = "list: j/k enter · ? help · s stats · / jump · q quit"
        try:
            self.chapters = load_chapters()
        except (OSError, ValueError) as e:
            self.notify(str(e), severity="error", timeout=20)
            self.exit(return_code=1)
            return
        self.progress.load()
        self._build_dir = Path(tempfile.mkdtemp(prefix="learn-c-tui-"))
        self.refresh_body()

    def on_unmount(self) -> None:
        if self._build_dir and self._build_dir.is_dir():
            shutil.rmtree(self._build_dir, ignore_errors=True)

    def refresh_body(self) -> None:
        body = self.query_one("#body", Container)
        body.remove_children()
        if self.route == "list":
            body.mount(self._chapter_list_widget())
        elif self.route == "jump":
            body.mount(
                Static(
                    "Jump to chapter by number (1–9). Esc/b back.\n\n"
                    + "\n".join(f"  {i + 1}. {c.title}" for i, c in enumerate(self.chapters[:9]))
                )
            )
        elif self.route == "theory" and self.selected_chapter is not None:
            ch = self.chapters[self.selected_chapter]
            lines = ch.theory.splitlines()
            h = 18
            chunk = "\n".join(lines[self.theory_scroll : self.theory_scroll + h])
            body.mount(
                Static(
                    f"[bold]{ch.title}[/bold] — theory (j/k scroll, enter exercises, b back)\n\n{chunk}"
                )
            )
        elif self.route == "exercises" and self.selected_chapter is not None:
            ch = self.chapters[self.selected_chapter]
            done = self.progress.completed_for_chapter(ch.id)
            lines = []
            for i, ex in enumerate(ch.exercises):
                mark = "✓ " if ex.id in done else "  "
                cur = ">" if i == self.exercise_cursor else " "
                lines.append(f"{cur}{mark}{ex.title}")
            body.mount(
                Static(
                    f"[bold]{ch.title}[/bold] — exercises\n\n"
                    + "\n".join(lines)
                    + "\n\nj/k move · enter open · b back to theory"
                )
            )
        elif self.route == "code" and self._exercise() is not None:
            ex = self._exercise()
            assert ex is not None
            body.mount(
                VerticalScroll(
                    Static(f"[bold]{ex.title}[/bold]\n{ex.description}\n", id="title_line"),
                    Static(self.current_code, id="code_view"),
                    Static("\n[yellow]r[/yellow] run · [yellow]e[/yellow] edit · [yellow]b[/yellow] back"),
                )
            )
        elif self.route == "result":
            msg = self.validation.message if self.validation else ""
            body.mount(
                VerticalScroll(
                    Static(msg),
                    Static(
                        "\n[yellow]h[/yellow] hint (if failed) · [yellow]b[/yellow] chapters · [yellow]r[/yellow] run again"
                    ),
                )
            )
        elif self.route == "stats":
            rows = self.progress.entries()
            lines = [f"Total progress rows: {len(rows)}", ""]
            for e in rows[-40:]:
                c = "done" if e.completed else "try"
                lines.append(f"  {e.chapter_id} :: {e.exercise_id}  ({c})")
            body.mount(Static("\n".join(lines) + "\n\nb back"))
        elif self.route == "help":
            body.mount(
                Static(
                    """
[bold]Learn C[/bold] — keys

[list]
- Chapter list: [yellow]j[/yellow]/[yellow]k[/yellow] or arrows, [yellow]enter[/yellow] open theory
- [yellow]/[/yellow] jump to chapter 1–9
- [yellow]?[/yellow] this help · [yellow]s[/yellow] stats · [yellow]q[/yellow] quit

Theory: [yellow]j[/yellow]/[yellow]k[/yellow] scroll · [yellow]enter[/yellow] exercise list · [yellow]b[/yellow] back

Exercises: [yellow]j[/yellow]/[yellow]k[/yellow] · [yellow]enter[/yellow] open code · [yellow]b[/yellow] back

Code: [yellow]r[/yellow] compile and run (cc/gcc) · [yellow]e[/yellow] external editor · [yellow]b[/yellow] back

Result: [yellow]h[/yellow] next hint on failure · [yellow]r[/yellow] re-run · [yellow]b[/yellow] back to chapter list
[/list]
                    """.strip()
                )
            )

    def _chapter_list_widget(self) -> Static:
        lines = []
        for i, ch in enumerate(self.chapters):
            cur = ">" if i == self.chapter_cursor else " "
            lines.append(f"{cur} {ch.title}")
        text = "\n".join(lines) + "\n\n[yellow]j/k[/yellow] move · [yellow]enter[/yellow] theory · [yellow]?[/yellow] help"
        return Static(text)

    def _exercise(self) -> Exercise | None:
        if self.selected_chapter is None or self.selected_exercise is None:
            return None
        return self.chapters[self.selected_chapter].exercises[self.selected_exercise]

    def on_key(self, event: Key) -> None:
        if self._run_busy and event.key not in ("escape",):
            return

        if event.key == "question_mark":
            self.route = "help"
            self.refresh_body()
            return

        if self.route == "list" and event.key == "s":
            self.route = "stats"
            self.refresh_body()
            return

        if self.route == "list":
            self._key_list(event)
        elif self.route == "jump":
            self._key_jump(event)
        elif self.route == "theory":
            self._key_theory(event)
        elif self.route == "exercises":
            self._key_exercises(event)
        elif self.route == "code":
            self._key_code(event)
        elif self.route == "result":
            self._key_result(event)
        elif self.route in ("stats", "help"):
            self._key_simple_back(event)

    def _key_simple_back(self, event: Key) -> None:
        if event.key in ("b", "escape"):
            self.route = "list"
            self.refresh_body()

    def _key_list(self, event: Key) -> None:
        if event.key == "slash":
            self.route = "jump"
            self.refresh_body()
            return
        if event.key in ("up", "k"):
            self.chapter_cursor = max(0, self.chapter_cursor - 1)
            self.refresh_body()
        elif event.key in ("down", "j"):
            self.chapter_cursor = min(len(self.chapters) - 1, self.chapter_cursor + 1)
            self.refresh_body()
        elif event.key == "enter":
            self.selected_chapter = self.chapter_cursor
            self.theory_scroll = 0
            self.route = "theory"
            self.refresh_body()

    def _key_jump(self, event: Key) -> None:
        if event.key in ("b", "escape"):
            self.route = "list"
            self.refresh_body()
            return
        ch = event.character
        if ch and ch.isdigit():
            n = int(ch)
            idx = n - 1
            if 0 <= idx < len(self.chapters):
                self.selected_chapter = idx
                self.chapter_cursor = idx
                self.theory_scroll = 0
                self.route = "theory"
                self.refresh_body()

    def _key_theory(self, event: Key) -> None:
        ch = self.chapters[self.selected_chapter or 0]
        lines = ch.theory.splitlines()
        h = 18
        max_scroll = max(0, len(lines) - h)
        if event.key in ("up", "k"):
            self.theory_scroll = max(0, self.theory_scroll - 1)
            self.refresh_body()
        elif event.key in ("down", "j"):
            self.theory_scroll = min(max_scroll, self.theory_scroll + 1)
            self.refresh_body()
        elif event.key == "enter":
            self.route = "exercises"
            self.exercise_cursor = 0
            self.refresh_body()
        elif event.key in ("b", "escape"):
            self.route = "list"
            self.selected_chapter = None
            self.refresh_body()

    def _key_exercises(self, event: Key) -> None:
        ch = self.chapters[self.selected_chapter or 0]
        n = len(ch.exercises)
        if event.key in ("up", "k"):
            self.exercise_cursor = max(0, self.exercise_cursor - 1)
            self.refresh_body()
        elif event.key in ("down", "j"):
            self.exercise_cursor = min(n - 1, self.exercise_cursor + 1)
            self.refresh_body()
        elif event.key == "enter":
            self.selected_exercise = self.exercise_cursor
            self.current_code = ch.exercises[self.exercise_cursor].starter_code
            self.hints_used = 0
            self.route = "code"
            self.refresh_body()
        elif event.key in ("b", "escape"):
            self.route = "theory"
            self.refresh_body()

    def _key_code(self, event: Key) -> None:
        if event.key == "r":
            self.action_run_snippet()
        elif event.key == "e":
            self.action_edit_snippet()
        elif event.key in ("b", "escape"):
            self.route = "exercises"
            self.selected_exercise = None
            self.refresh_body()

    def _key_result(self, event: Key) -> None:
        if event.key == "h" and self.validation and not self.validation.passed:
            self.hints_used += 1
            if self.last_exec is not None and self._exercise() is not None:
                self.validation = self.validator.validate(
                    self.last_exec,
                    self._exercise(),  # type: ignore[arg-type]
                    self.hints_used,
                )
            self.refresh_body()
        elif event.key == "r":
            self.action_run_snippet()
        elif event.key in ("b", "escape"):
            self.route = "list"
            self.selected_chapter = None
            self.selected_exercise = None
            self.refresh_body()

    def action_edit_snippet(self) -> None:
        if self.route != "code" or self._exercise() is None:
            return
        try:
            with self.suspend():
                self.current_code = launch_editor(self.current_code)
        except RuntimeError as e:
            self.notify(str(e), severity="error")
        self.refresh_body()

    def action_run_snippet(self) -> None:
        if self.route not in ("code", "result") or self._exercise() is None:
            return
        if self._run_busy or self._build_dir is None:
            return
        self._run_busy = True
        code = self.current_code
        bdir = self._build_dir

        def run() -> None:
            res = execute_code(code, work_dir=bdir)
            self.call_from_thread(self._on_run_done, res)

        threading.Thread(target=run, daemon=True).start()

    def _on_run_done(self, res: ExecutionResult) -> None:
        self._run_busy = False
        self.last_exec = res
        ex = self._exercise()
        if ex is None or self.selected_chapter is None:
            return
        self.validation = self.validator.validate(res, ex, self.hints_used)
        if self.validation.passed:
            ch = self.chapters[self.selected_chapter]
            self.progress.save_progress(
                ch.id,
                ex.id,
                completed=True,
                attempts=1,
                hints_used=self.hints_used,
            )
            try:
                self.progress.save()
            except OSError as e:
                self.notify(f"Could not save progress: {e}", severity="warning")
        self.route = "result"
        self.refresh_body()
