use crate::chapter::Chapter;
use crate::executor::{ExecutionResult, Executor};
use crate::progress::ProgressStore;
use crate::validator::{ValidationResult, Validator};
use crossterm::event::{KeyCode, KeyEvent, KeyModifiers};
use ratatui::layout::Rect;
use ratatui::style::{Color, Modifier, Style};
use ratatui::text::{Line, Span};
use ratatui::widgets::{Paragraph, Wrap};
use ratatui::Frame;
use std::sync::mpsc;
use std::thread;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum UiEffect {
    None,
    Quit,
    LaunchEditor,
}

pub struct RunComplete {
    pub exec: Result<ExecutionResult, String>,
    pub hints_used: usize,
}

pub struct App {
    pub view: String,
    pub chapters: Vec<Chapter>,
    pub cursor: usize,
    pub theory_scroll: usize,
    pub selected_chapter_idx: Option<usize>,
    pub selected_exercise_idx: Option<usize>,
    pub exercise_cursor: usize,
    pub hints_used: usize,
    pub execution_result: Option<ExecutionResult>,
    pub validation_result: Option<ValidationResult>,
    pub current_code: String,
    pub validator: Validator,
    pub progress: ProgressStore,
    pub run_rx: Option<mpsc::Receiver<RunComplete>>,
}

impl App {
    pub fn new() -> Self {
        let loader = crate::chapter::ChapterLoader::new(crate::chapter::default_chapters_dir());
        let chapters = loader.load_chapters().unwrap_or_else(|e| {
            eprintln!("Warning: could not load chapters: {e}");
            Vec::new()
        });

        let mut progress = ProgressStore::new();
        if let Err(e) = progress.load() {
            eprintln!("Warning: could not load progress: {e}");
        }

        Self {
            view: "list".into(),
            chapters,
            cursor: 0,
            theory_scroll: 0,
            selected_chapter_idx: None,
            selected_exercise_idx: None,
            exercise_cursor: 0,
            hints_used: 0,
            execution_result: None,
            validation_result: None,
            current_code: String::new(),
            validator: Validator::new(),
            progress,
            run_rx: None,
        }
    }

    pub fn poll_run(&mut self) {
        if let Some(rx) = self.run_rx.take() {
            match rx.try_recv() {
                Ok(msg) => {
                    self.handle_run_complete(msg);
                }
                Err(std::sync::mpsc::TryRecvError::Empty) => {
                    self.run_rx = Some(rx);
                }
                Err(std::sync::mpsc::TryRecvError::Disconnected) => {}
            }
        }
    }

    fn handle_run_complete(&mut self, msg: RunComplete) {
        let hints_used = msg.hints_used;
        match msg.exec {
            Err(e) => {
                self.validation_result = Some(ValidationResult {
                    passed: false,
                    message: format!("Execution error: {e}"),
                    show_solution: false,
                });
                self.view = "result".into();
            }
            Ok(exec_res) => {
                self.execution_result = Some(exec_res.clone());
                if let (Some(ch_idx), Some(ex_idx)) =
                    (self.selected_chapter_idx, self.selected_exercise_idx)
                {
                    let exercise = self.chapters[ch_idx].exercises[ex_idx].clone();
                    let chapter_id = self.chapters[ch_idx].id.clone();
                    let exercise_id = exercise.id.clone();
                    let validation = self.validator.validate(&exec_res, &exercise, hints_used);
                    let passed = validation.passed;
                    self.validation_result = Some(validation);
                    self.view = "result".into();

                    if passed {
                        self.progress.save_progress(
                            &chapter_id,
                            &exercise_id,
                            true,
                            1,
                            hints_used,
                        );
                        if let Err(e) = self.progress.save() {
                            eprintln!("Warning: could not save progress: {e}");
                        }
                    }
                }
            }
        }
    }

    pub fn handle_key(&mut self, key: KeyEvent) -> UiEffect {
        if key.modifiers.contains(KeyModifiers::CONTROL) && matches!(key.code, KeyCode::Char('c')) {
            return UiEffect::Quit;
        }
        if matches!(key.code, KeyCode::Char('q')) {
            return UiEffect::Quit;
        }

        match key.code {
            KeyCode::Char('s') if matches!(self.view.as_str(), "list" | "stats") => {
                self.view = "stats".into();
                return UiEffect::None;
            }
            KeyCode::Char('?') if matches!(self.view.as_str(), "list" | "help") => {
                self.view = "help".into();
                return UiEffect::None;
            }
            _ => {}
        }

        match self.view.as_str() {
            "list" => self.handle_list(key),
            "theory" => self.handle_theory(key),
            "jump" => self.handle_jump(key),
            "exercise_list" => self.handle_exercise_list(key),
            "editor" | "result" => return self.handle_editor(key),
            "stats" => self.handle_stats(key),
            "help" => self.handle_help(key),
            _ => {}
        }

        UiEffect::None
    }

    fn handle_list(&mut self, key: KeyEvent) {
        match key.code {
            KeyCode::Char('/') => self.view = "jump".into(),
            KeyCode::Up | KeyCode::Char('k') => {
                if self.cursor > 0 {
                    self.cursor -= 1;
                }
            }
            KeyCode::Down | KeyCode::Char('j') => {
                if self.cursor + 1 < self.chapters.len() {
                    self.cursor += 1;
                }
            }
            KeyCode::Enter => {
                self.selected_chapter_idx = Some(self.cursor);
                self.theory_scroll = 0;
                self.view = "theory".into();
            }
            _ => {}
        }
    }

    fn handle_jump(&mut self, key: KeyEvent) {
        match key.code {
            KeyCode::Up | KeyCode::Char('k') | KeyCode::Esc | KeyCode::Backspace | KeyCode::Char('b') => {
                self.view = "list".into();
            }
            KeyCode::Char(c @ '1'..='9') => {
                let idx = (c as u8 - b'1') as usize;
                if idx < self.chapters.len() {
                    self.selected_chapter_idx = Some(idx);
                    self.theory_scroll = 0;
                    self.view = "theory".into();
                }
            }
            KeyCode::Char('0') => {
                if self.chapters.len() >= 10 {
                    self.selected_chapter_idx = Some(9);
                    self.theory_scroll = 0;
                    self.exercise_cursor = 0;
                    self.view = "theory".into();
                }
            }
            _ => self.view = "list".into(),
        }
    }

    fn handle_exercise_list(&mut self, key: KeyEvent) {
        let Some(ch_idx) = self.selected_chapter_idx else {
            return;
        };
        let n = self.chapters[ch_idx].exercises.len();
        match key.code {
            KeyCode::Up | KeyCode::Char('k') => {
                if self.exercise_cursor > 0 {
                    self.exercise_cursor -= 1;
                }
            }
            KeyCode::Down | KeyCode::Char('j') => {
                if self.exercise_cursor + 1 < n {
                    self.exercise_cursor += 1;
                }
            }
            KeyCode::Enter => {
                self.selected_exercise_idx = Some(self.exercise_cursor);
                self.current_code = self.chapters[ch_idx].exercises[self.exercise_cursor]
                    .starter_code
                    .clone();
                self.hints_used = 0;
                self.view = "editor".into();
            }
            KeyCode::Esc | KeyCode::Backspace | KeyCode::Char('b') => {
                self.view = "list".into();
                self.selected_chapter_idx = None;
                self.selected_exercise_idx = None;
                self.exercise_cursor = 0;
            }
            _ => {}
        }
    }

    fn handle_editor(&mut self, key: KeyEvent) -> UiEffect {
        if self.run_rx.is_some() {
            return UiEffect::None;
        }

        match key.code {
            KeyCode::Char('r') => {
                self.spawn_run();
                UiEffect::None
            }
            KeyCode::Char('e') if self.selected_exercise_idx.is_some() => UiEffect::LaunchEditor,
            KeyCode::Char('h') if self.view == "result" => {
                if let Some(v) = &self.validation_result {
                    if !v.passed {
                        self.hints_used += 1;
                        self.spawn_run();
                    }
                }
                UiEffect::None
            }
            KeyCode::Esc | KeyCode::Backspace | KeyCode::Char('b') => {
                self.view = "list".into();
                self.selected_chapter_idx = None;
                self.selected_exercise_idx = None;
                self.exercise_cursor = 0;
                UiEffect::None
            }
            _ => UiEffect::None,
        }
    }

    fn spawn_run(&mut self) {
        let code = self.current_code.clone();
        let hints_used = self.hints_used;
        let (tx, rx) = mpsc::channel();
        thread::spawn(move || {
            let exec = Executor::new().execute_code(&code);
            let _ = tx.send(RunComplete { exec, hints_used });
        });
        self.run_rx = Some(rx);
    }

    fn handle_stats(&mut self, key: KeyEvent) {
        match key.code {
            KeyCode::Esc | KeyCode::Backspace | KeyCode::Char('b') => {
                self.view = "list".into();
            }
            _ => {}
        }
    }

    fn handle_help(&mut self, key: KeyEvent) {
        match key.code {
            KeyCode::Esc | KeyCode::Backspace | KeyCode::Char('b') => {
                self.view = "list".into();
            }
            _ => {}
        }
    }

    fn theory_scroll_max(&self) -> usize {
        let Some(ch_idx) = self.selected_chapter_idx else {
            return 0;
        };
        let lines: Vec<&str> = self.chapters[ch_idx].theory.lines().collect();
        let term_height = 24usize;
        if lines.len() <= term_height {
            0
        } else {
            lines.len().saturating_sub(term_height) + 4
        }
    }

    fn handle_theory(&mut self, key: KeyEvent) {
        match key.code {
            KeyCode::Up | KeyCode::Char('k') => {
                self.theory_scroll = self.theory_scroll.saturating_sub(1);
            }
            KeyCode::Down | KeyCode::Char('j') => {
                let max = self.theory_scroll_max();
                if self.theory_scroll < max {
                    self.theory_scroll += 1;
                }
            }
            KeyCode::Enter => {
                self.view = "exercise_list".into();
                self.exercise_cursor = 0;
            }
            KeyCode::Esc | KeyCode::Backspace | KeyCode::Char('b') => {
                self.view = "list".into();
            }
            _ => {}
        }
    }

    pub fn apply_editor_result(&mut self, res: Result<String, String>) {
        match res {
            Err(e) => {
                self.validation_result = Some(ValidationResult {
                    passed: false,
                    message: format!("Editor error: {e}"),
                    show_solution: false,
                });
            }
            Ok(code) => self.current_code = code,
        }
        self.view = "editor".into();
    }

    pub fn draw(&self, frame: &mut Frame) {
        let area = frame.area();
        let text = self.render_text(area);
        let paragraph = Paragraph::new(text)
            .wrap(Wrap { trim: true })
            .block(ratatui::widgets::Block::default());
        frame.render_widget(paragraph, area);
    }

    fn render_text(&self, area: Rect) -> Vec<Line<'_>> {
        match self.view.as_str() {
            "list" => self.render_chapter_list(),
            "jump" => self.render_jump_list(),
            "theory" => self.render_theory(area.height as usize),
            "exercise_list" => self.render_exercise_list(),
            "editor" | "result" => self.render_exercise_view(),
            "stats" => self.render_stats(),
            "help" => self.render_help(),
            _ => vec![Line::from("Unknown view")],
        }
    }

    fn header_style() -> Style {
        Style::default()
            .fg(Color::LightGreen)
            .add_modifier(Modifier::BOLD)
    }

    fn cursor_style() -> Style {
        Style::default().fg(Color::Yellow).add_modifier(Modifier::BOLD)
    }

    fn dim_style() -> Style {
        Style::default().fg(Color::DarkGray)
    }

    fn key_style() -> Style {
        Style::default().fg(Color::Gray).add_modifier(Modifier::ITALIC)
    }

    fn success_style() -> Style {
        Style::default().fg(Color::LightGreen).add_modifier(Modifier::BOLD)
    }

    fn error_style() -> Style {
        Style::default().fg(Color::LightRed).add_modifier(Modifier::BOLD)
    }

    fn hint_style() -> Style {
        Style::default().fg(Color::LightBlue)
    }

    fn code_style() -> Style {
        Style::default()
            .fg(Color::Rgb(228, 228, 200))
            .bg(Color::Rgb(40, 40, 40))
    }

    fn chapter_num_style() -> Style {
        Style::default().fg(Color::LightCyan).add_modifier(Modifier::BOLD)
    }

    fn render_chapter_list(&self) -> Vec<Line<'_>> {
        let mut lines = vec![
            Line::from(Span::styled(
                "Learn Rust - Select a Chapter",
                Self::header_style(),
            )),
            Line::from(""),
        ];

        for (i, chapter) in self.chapters.iter().enumerate() {
            let prefix = if self.cursor == i {
                Span::styled("▶ ", Self::cursor_style())
            } else {
                Span::raw("  ")
            };
            let num = Span::styled(format!("[{}] ", i + 1), Self::chapter_num_style());
            let title = Span::raw(chapter.title.clone());
            lines.push(Line::from(vec![prefix, num, title]));

            let mut info = format!(
                "   {} ({} exercises)",
                chapter.description, chapter.exercise_count
            );
            if chapter.exercise_count > 0 {
                let completed = self
                    .progress
                    .get_completed_exercises(&chapter.id)
                    .len();
                let pct = (completed as f64 / chapter.exercise_count as f64 * 100.0) as i32;
                info.push_str(&format!(" ({pct}% done)"));
            }
            lines.push(Line::from(Span::styled(info, Self::dim_style())));
            lines.push(Line::from(""));
        }

        lines.push(Line::from(Span::styled(
            "↑/↓ Navigate  •  Enter Select  •  / Jump  •  q Quit  •  s Stats  •  ? Help",
            Self::key_style(),
        )));
        lines
    }

    fn render_jump_list(&self) -> Vec<Line<'_>> {
        let mut lines = vec![
            Line::from(Span::styled("Jump to Chapter", Self::header_style())),
            Line::from(""),
        ];

        for (i, chapter) in self.chapters.iter().enumerate() {
            let mut num = i + 1;
            if num > 9 {
                num = 0;
            }
            lines.push(Line::from(vec![
                Span::styled(format!("[{num}] "), Self::chapter_num_style()),
                Span::raw(chapter.title.clone()),
            ]));
            lines.push(Line::from(Span::styled(
                format!(
                    "   {} ({} exercises)",
                    chapter.description, chapter.exercise_count
                ),
                Self::dim_style(),
            )));
            lines.push(Line::from(""));
        }

        lines.push(Line::from(Span::styled(
            "1-9,0 Select  •  / Jump menu  •  ← Back  •  q Quit",
            Self::key_style(),
        )));
        lines
    }

    fn render_theory(&self, term_height: usize) -> Vec<Line<'_>> {
        let Some(ch_idx) = self.selected_chapter_idx else {
            return vec![Line::from("No chapter selected")];
        };
        let chapter = &self.chapters[ch_idx];
        let mut lines = vec![Line::from(Span::styled(
            format!("{} - Theory", chapter.title),
            Self::header_style(),
        ))];
        lines.push(Line::from(""));

        let all_lines: Vec<&str> = chapter.theory.lines().collect();
        let visible = (term_height.saturating_sub(8)).max(8);
        let mut start = self.theory_scroll;
        if start + visible > all_lines.len() {
            start = all_lines.len().saturating_sub(visible);
        }
        let end = (start + visible).min(all_lines.len());

        for line in &all_lines[start..end] {
            lines.push(Line::from(*line));
        }

        if self.theory_scroll > 0 {
            lines.push(Line::from(Span::styled(
                "(scroll up for more)",
                Self::dim_style(),
            )));
        }
        if end < all_lines.len() {
            lines.push(Line::from(Span::styled(
                "(scroll down for more)",
                Self::dim_style(),
            )));
        }

        lines.push(Line::from(""));
        lines.push(Line::from(Span::styled(
            "↑/↓ Scroll  •  Enter Continue  •  ← Back  •  q Quit",
            Self::key_style(),
        )));
        lines
    }

    fn render_exercise_list(&self) -> Vec<Line<'_>> {
        let Some(ch_idx) = self.selected_chapter_idx else {
            return vec![Line::from("No chapter selected")];
        };
        let chapter = &self.chapters[ch_idx];
        let mut lines = vec![Line::from(Span::styled(
            format!("{} - Exercises", chapter.title),
            Self::header_style(),
        ))];
        lines.push(Line::from(""));

        for (i, ex) in chapter.exercises.iter().enumerate() {
            let prefix = if self.exercise_cursor == i {
                Span::styled("▶ ", Self::cursor_style())
            } else {
                Span::raw("  ")
            };
            lines.push(Line::from(vec![prefix, Span::raw(ex.title.clone())]));
            lines.push(Line::from(Span::styled(
                format!("   {}", ex.description),
                Self::dim_style(),
            )));
            lines.push(Line::from(""));
        }

        lines.push(Line::from(Span::styled(
            "↑/↓ Navigate  •  Enter Start  •  ← Back  •  q Quit",
            Self::key_style(),
        )));
        lines
    }

    fn render_exercise_view(&self) -> Vec<Line<'_>> {
        let (Some(ch_idx), Some(ex_idx)) = (self.selected_chapter_idx, self.selected_exercise_idx)
        else {
            return vec![Line::from("No exercise selected")];
        };
        let exercise = &self.chapters[ch_idx].exercises[ex_idx];

        let mut lines = vec![Line::from(Span::styled(
            exercise.title.clone(),
            Self::header_style(),
        ))];
        lines.push(Line::from(""));
        lines.push(Line::from(exercise.description.as_str()));
        lines.push(Line::from(""));
        lines.push(Line::from(Span::styled("--- Your Code ---", Self::dim_style())));
        for cl in self.current_code.lines() {
            lines.push(Line::from(Span::styled(cl, Self::code_style())));
        }
        lines.push(Line::from(Span::styled("-----------------", Self::dim_style())));
        lines.push(Line::from(""));

        if self.view == "result" {
            if let Some(v) = &self.validation_result {
                if v.passed {
                    lines.push(Line::from(Span::styled(
                        format!("✓ {}", v.message),
                        Self::success_style(),
                    )));
                    lines.push(Line::from(""));
                } else {
                    for l in v.message.lines() {
                        lines.push(Line::from(Span::styled(l, Self::error_style())));
                    }
                    lines.push(Line::from(""));
                    if v.show_solution {
                        lines.push(Line::from(Span::styled(
                            "--- Solution ---",
                            Self::hint_style(),
                        )));
                        for l in exercise.solution.lines() {
                            lines.push(Line::from(l));
                        }
                    }
                }
            }
        } else {
            lines.push(Line::from(Span::styled(
                "e Open editor  •  r Run  •  h Hint  •  ← Back  •  q Quit",
                Self::key_style(),
            )));
        }

        lines
    }

    fn render_stats(&self) -> Vec<Line<'_>> {
        let mut total_exercises = 0usize;
        let mut completed_exercises = 0usize;
        let mut total_hints = 0i32;

        for chapter in &self.chapters {
            total_exercises += chapter.exercise_count;
            let completed = self.progress.get_completed_exercises(&chapter.id);
            completed_exercises += completed.len();
            for p in self.progress.entries() {
                if p.chapter_id == chapter.id && p.completed {
                    total_hints += p.hints_used;
                }
            }
        }

        let pct = if total_exercises > 0 {
            (completed_exercises as f64 / total_exercises as f64 * 100.0).round() as i32
        } else {
            0
        };

        vec![
            Line::from(Span::styled("Stats Dashboard", Self::header_style())),
            Line::from(""),
            Line::from(Span::styled(
                format!("Total Exercises:  {total_exercises}"),
                Self::dim_style(),
            )),
            Line::from(Span::styled(
                format!("Completed:        {completed_exercises}"),
                Self::dim_style(),
            )),
            Line::from(Span::styled(
                format!("Completion:       {pct}%"),
                Self::dim_style(),
            )),
            Line::from(Span::styled(
                format!("Hints Used:       {total_hints}"),
                Self::dim_style(),
            )),
            Line::from(""),
            Line::from(Span::styled("← Back  •  q Quit", Self::key_style())),
        ]
    }

    fn render_help(&self) -> Vec<Line<'_>> {
        let mut lines = vec![
            Line::from(Span::styled(
                "Keyboard Shortcuts",
                Self::header_style(),
            )),
            Line::from(""),
        ];

        let rows = [
            ("q", "Quit application (from chapter list)"),
            ("↑/↓ or k/j", "Navigate up/down"),
            ("Enter", "Select (chapter or exercise)"),
            ("Esc, Backspace, or b", "Go back to previous view"),
            ("/", "Jump to chapter by number"),
            ("s", "Show stats dashboard"),
            ("?", "Show this help screen"),
            ("e", "Open editor for exercise"),
            ("r", "Run current code (rustc + run)"),
            ("h", "Show hint (on failed result view)"),
        ];

        for (k, d) in rows {
            lines.push(Line::from(vec![
                Span::styled(k, Self::key_style()),
                Span::raw("\t"),
                Span::styled(d, Self::dim_style()),
            ]));
        }

        lines.push(Line::from(""));
        lines.push(Line::from(Span::styled(
            "← Back  •  q Quit",
            Self::key_style(),
        )));
        lines
    }
}
