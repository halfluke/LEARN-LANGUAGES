use serde::Deserialize;
use std::fs;
use std::path::{Path, PathBuf};

#[derive(Debug, Clone, Deserialize)]
pub struct Chapter {
    pub id: String,
    pub title: String,
    pub description: String,
    pub theory: String,
    pub exercises: Vec<Exercise>,
    #[serde(default)]
    pub exercise_count: usize,
}

#[derive(Debug, Clone, Deserialize)]
pub struct Exercise {
    pub id: String,
    pub title: String,
    pub description: String,
    #[serde(rename = "starter_code")]
    pub starter_code: String,
    #[serde(rename = "expected_output")]
    pub expected_output: String,
    #[serde(default)]
    pub hints: Vec<String>,
    #[serde(default)]
    pub solution: String,
}

pub struct ChapterLoader {
    chapters_dir: PathBuf,
}

impl ChapterLoader {
    pub fn new(chapters_dir: impl Into<PathBuf>) -> Self {
        Self {
            chapters_dir: chapters_dir.into(),
        }
    }

    pub fn load_chapters(&self) -> Result<Vec<Chapter>, String> {
        let entries = fs::read_dir(&self.chapters_dir)
            .map_err(|e| format!("failed to read chapters directory: {e}"))?;

        let mut paths: Vec<PathBuf> = entries
            .filter_map(|e| e.ok())
            .map(|e| e.path())
            .filter(|p| p.extension().and_then(|s| s.to_str()) == Some("json"))
            .collect();

        paths.sort();

        if paths.is_empty() {
            return Err(format!(
                "no chapters found in {}",
                self.chapters_dir.display()
            ));
        }

        let mut chapters = Vec::new();
        for path in paths {
            chapters.push(self.load_chapter_file(&path)?);
        }

        Ok(chapters)
    }

    fn load_chapter_file(&self, path: &Path) -> Result<Chapter, String> {
        let data = fs::read_to_string(path).map_err(|e| format!("failed to read file: {e}"))?;

        let mut chapter: Chapter =
            serde_json::from_str(&data).map_err(|e| format!("failed to parse JSON: {e}"))?;

        if chapter.id.is_empty() {
            return Err("missing required field: id".into());
        }
        if chapter.title.is_empty() {
            return Err("missing required field: title".into());
        }
        if chapter.description.is_empty() {
            return Err("missing required field: description".into());
        }
        if chapter.exercises.is_empty() {
            return Err("chapter has no exercises".into());
        }

        for (i, ex) in chapter.exercises.iter().enumerate() {
            if ex.id.is_empty() {
                return Err(format!("exercise {i}: missing id"));
            }
            if ex.title.is_empty() {
                return Err(format!("exercise {i} ({}): missing title", ex.id));
            }
            if ex.starter_code.is_empty() {
                return Err(format!("exercise {i} ({}): missing starter_code", ex.id));
            }
            if ex.expected_output.is_empty() {
                return Err(format!(
                    "exercise {i} ({}): missing expected_output",
                    ex.id
                ));
            }
        }

        chapter.exercise_count = chapter.exercises.len();
        Ok(chapter)
    }

    /// Load a single chapter by `id` (must match the `id` field inside the JSON file).
    #[allow(dead_code)]
    pub fn load_chapter(&self, id: &str) -> Result<Chapter, String> {
        self.load_chapters()?
            .into_iter()
            .find(|c| c.id == id)
            .ok_or_else(|| format!("chapter not found: {id}"))
    }
}

pub fn default_chapters_dir() -> PathBuf {
    PathBuf::from("chapters")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn load_chapters_smoke() {
        let loader = ChapterLoader::new("chapters");
        let chapters = loader.load_chapters().expect("load chapters");
        assert!(
            chapters.len() >= 19,
            "expected at least 19 chapters, got {}",
            chapters.len()
        );
    }

    #[test]
    fn load_chapter_by_id() {
        let loader = ChapterLoader::new("chapters");
        let ch = loader.load_chapter("variables").expect("variables");
        assert_eq!(ch.id, "variables");
        assert!(!ch.exercises.is_empty());
    }

    #[test]
    fn load_missing_chapter_errors() {
        let loader = ChapterLoader::new("chapters");
        assert!(loader.load_chapter("nonexistent").is_err());
    }
}
