mod chapter;
mod editor;
mod executor;
mod model;
mod progress;
mod validator;

#[cfg(test)]
mod solutions_alignment;

use crate::editor::Editor;
use crate::model::{App, UiEffect};
use crossterm::event::{self, Event};
use crossterm::execute;
use crossterm::terminal::{disable_raw_mode, enable_raw_mode, EnterAlternateScreen, LeaveAlternateScreen};
use ratatui::backend::CrosstermBackend;
use ratatui::Terminal;
use std::io::{self, stdout};
use std::process::Command;
use std::time::Duration;

fn main() -> io::Result<()> {
    if let Err(e) = check_rust_prerequisite() {
        eprintln!("{e}");
        std::process::exit(1);
    }

    enable_raw_mode()?;
    let mut stdout = stdout();
    execute!(stdout, EnterAlternateScreen)?;
    let mut terminal = Terminal::new(CrosstermBackend::new(stdout))?;

    let mut app = App::new();

    loop {
        terminal.draw(|f| app.draw(f))?;
        app.poll_run();

        if event::poll(Duration::from_millis(100))? {
            if let Event::Key(key) = event::read()? {
                match app.handle_key(key) {
                    UiEffect::Quit => break,
                    UiEffect::LaunchEditor => {
                        disable_raw_mode()?;
                        execute!(terminal.backend_mut(), LeaveAlternateScreen)?;
                        let res = Editor::new()
                            .and_then(|ed| ed.launch_editor(&app.current_code));
                        execute!(terminal.backend_mut(), EnterAlternateScreen)?;
                        enable_raw_mode()?;
                        terminal.clear()?;
                        app.apply_editor_result(res);
                    }
                    UiEffect::None => {}
                }
            }
        }
    }

    disable_raw_mode()?;
    execute!(terminal.backend_mut(), LeaveAlternateScreen)?;
    Ok(())
}

fn check_rust_prerequisite() -> Result<(), String> {
    let output = Command::new("rustc")
        .arg("--version")
        .output()
        .map_err(|_| {
            "Rust is not installed or rustc is not in PATH.\n\n\
             Install Rust from https://rustup.rs/\n\
             After installation, ensure `rustc` is on your PATH."
                .to_string()
        })?;

    if !output.status.success() {
        return Err("rustc did not run successfully. Check your Rust installation.".into());
    }

    let text = String::from_utf8_lossy(&output.stdout);
    eprintln!("✓ Rust found: {}", text.trim());
    Ok(())
}
