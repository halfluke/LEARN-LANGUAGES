use serde::{Deserialize, Serialize};
use std::fs;
use std::path::PathBuf;
use std::time::{SystemTime, UNIX_EPOCH};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Progress {
    pub chapter_id: String,
    pub exercise_id: String,
    pub completed: bool,
    pub attempts: i32,
    pub hints_used: i32,
    pub last_attempt: i64,
}

pub struct ProgressStore {
    file_path: PathBuf,
    progress: Vec<Progress>,
}

impl ProgressStore {
    pub fn new() -> Self {
        let home = dirs::home_dir().unwrap_or_else(|| PathBuf::from("."));
        let store_dir = home.join(".learn-rust-tui");
        Self {
            file_path: store_dir.join("progress.json"),
            progress: Vec::new(),
        }
    }

    pub fn load(&mut self) -> Result<(), String> {
        match fs::read_to_string(&self.file_path) {
            Ok(data) => {
                self.progress =
                    serde_json::from_str(&data).map_err(|e| format!("failed to parse progress: {e}"))?;
                Ok(())
            }
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => Ok(()),
            Err(e) => Err(format!("failed to read progress: {e}")),
        }
    }

    pub fn save(&self) -> Result<(), String> {
        let dir = self.file_path.parent().ok_or("invalid progress path")?;
        fs::create_dir_all(dir).map_err(|e| format!("failed to create directory: {e}"))?;

        let data = serde_json::to_string_pretty(&self.progress)
            .map_err(|e| format!("failed to marshal progress: {e}"))?;

        fs::write(&self.file_path, data).map_err(|e| format!("failed to write progress: {e}"))?;
        Ok(())
    }

    pub fn save_progress(
        &mut self,
        chapter_id: &str,
        exercise_id: &str,
        completed: bool,
        attempts: i32,
        hints_used: usize,
    ) {
        let now = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .map(|d| d.as_secs() as i64)
            .unwrap_or(0);

        for p in &mut self.progress {
            if p.chapter_id == chapter_id && p.exercise_id == exercise_id {
                p.completed = completed || p.completed;
                if attempts > 0 {
                    p.attempts = attempts;
                }
                if hints_used > 0 {
                    p.hints_used = hints_used as i32;
                }
                p.last_attempt = now;
                return;
            }
        }

        self.progress.push(Progress {
            chapter_id: chapter_id.to_string(),
            exercise_id: exercise_id.to_string(),
            completed,
            attempts,
            hints_used: hints_used as i32,
            last_attempt: now,
        });
    }

    pub fn get_completed_exercises(&self, chapter_id: &str) -> Vec<String> {
        self.progress
            .iter()
            .filter(|p| p.chapter_id == chapter_id && p.completed)
            .map(|p| p.exercise_id.clone())
            .collect()
    }

    pub fn entries(&self) -> &[Progress] {
        &self.progress
    }
}
