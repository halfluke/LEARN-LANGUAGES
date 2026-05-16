"""Hub menu: choose a language track and launch its course TUI."""

from __future__ import annotations

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.events import Key
from textual.widgets import Footer, Header, Static

from learn_languages.tracks import TRACKS, Track, launch_track, repo_root


class LearnLanguagesMenu(App[None]):
    CSS = """
    #body { width: 100%; height: 1fr; padding: 0 1; }
    """

    BINDINGS = [
        Binding("ctrl+c", "quit", "", show=False),
        Binding("q", "quit", "Quit"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.cursor = 0
        self._status = ""

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Container(id="body")
        yield Footer()

    def on_mount(self) -> None:
        self.title = "LEARN-LANGUAGES"
        self.sub_title = "j/k move · enter open course · q quit"
        self.refresh_body()

    def refresh_body(self) -> None:
        body = self.query_one("#body", Container)
        body.remove_children()
        lines = [
            "[bold]Choose a language[/bold]",
            "",
            "Each course runs in this terminal. When you quit a course ([yellow]q[/yellow]), you return here.",
            "",
        ]
        for i, track in enumerate(TRACKS):
            cur = ">" if i == self.cursor else " "
            lines.append(f"{cur} [bold]{track.title}[/bold]  [dim]({track.subtitle})[/dim]")
        lines.extend(
            [
                "",
                "[yellow]j[/yellow]/[yellow]k[/yellow] move · [yellow]enter[/yellow] launch · [yellow]q[/yellow] quit",
            ]
        )
        if self._status:
            lines.extend(["", self._status])
        body.mount(Static("\n".join(lines)))

    def _selected(self) -> Track:
        return TRACKS[self.cursor]

    def on_key(self, event: Key) -> None:
        if event.key in ("j", "down") and self.cursor + 1 < len(TRACKS):
            self.cursor += 1
            self.refresh_body()
        elif event.key in ("k", "up") and self.cursor > 0:
            self.cursor -= 1
            self.refresh_body()
        elif event.key == "enter":
            self._open_track(self._selected())
        elif event.key in ("1", "2", "3", "4", "5", "6", "7"):
            idx = int(event.key) - 1
            if idx < len(TRACKS):
                self.cursor = idx
                self.refresh_body()
                self._open_track(TRACKS[idx])

    def _open_track(self, track: Track) -> None:
        self._status = f"[dim]Launching {track.title}…[/dim]"
        self.refresh_body()
        root = repo_root()
        with self.suspend():
            rc = launch_track(track, root=root)
        if rc == 0:
            self._status = f"[dim]Returned from {track.title}.[/dim]"
        else:
            self._status = (
                f"[red]{track.title} exited with code {rc}.[/red] "
                f"See [bold]{track.directory}/README.md[/bold] for setup."
            )
        self.refresh_body()
