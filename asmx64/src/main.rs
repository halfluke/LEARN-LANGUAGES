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
    if let Err(e) = check_asm_prerequisites() {
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

fn check_asm_prerequisites() -> Result<(), String> {
    let nasm = Command::new("nasm")
        .arg("-v")
        .output()
        .map_err(|_| "nasm is not installed or not in PATH.\n\nInstall: sudo apt install nasm\n".to_string())?;
    if !nasm.status.success() {
        return Err("nasm did not run successfully.".into());
    }

    let ld = Command::new("ld")
        .arg("--version")
        .output()
        .map_err(|_| "ld is not installed or not in PATH.\n\nInstall: sudo apt install binutils\n".to_string())?;
    if !ld.status.success() {
        return Err("ld did not run successfully.".into());
    }

    let gcc = Command::new("gcc")
        .arg("--version")
        .output()
        .map_err(|_| "gcc is not installed or not in PATH.\n\nInstall: sudo apt install gcc\n".to_string())?;
    if !gcc.status.success() {
        return Err("gcc did not run successfully.".into());
    }

    eprintln!(
        "✓ {}",
        String::from_utf8_lossy(&nasm.stderr).lines().next().unwrap_or("nasm ok")
    );
    Ok(())
}
