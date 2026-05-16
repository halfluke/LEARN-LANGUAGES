use std::fs;
use std::process::Command;

pub struct Editor {
    editor_path: String,
}

impl Editor {
    pub fn new() -> Result<Self, String> {
        let editor_path = std::env::var("EDITOR").unwrap_or_default();
        if !editor_path.is_empty() {
            return Ok(Editor { editor_path });
        }

        for ed in ["nano", "micro", "vim", "nvim", "code", "subl"] {
            if which_available(ed) {
                return Ok(Editor {
                    editor_path: ed.to_string(),
                });
            }
        }

        Err("no editor found. Set $EDITOR or install nano/vim/code".into())
    }

    pub fn launch_editor(&self, initial_code: &str) -> Result<String, String> {
        let nanos = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap_or_default()
            .as_nanos();
        let tmp_dir = std::env::temp_dir().join(format!("learn-asmx64-editor-{nanos}"));
        fs::create_dir_all(&tmp_dir).map_err(|e| format!("failed to create temp dir: {e}"))?;

        let tmp_file = tmp_dir.join("solution.asm");
        fs::write(&tmp_file, initial_code).map_err(|e| format!("failed to write temp file: {e}"))?;

        let status = Command::new(&self.editor_path)
            .arg(&tmp_file)
            .stdin(std::process::Stdio::inherit())
            .stdout(std::process::Stdio::inherit())
            .stderr(std::process::Stdio::inherit())
            .status()
            .map_err(|e| format!("failed to launch editor: {e}"))?;

        if !status.success() {
            return Err("editor exited with a non-zero status".into());
        }

        fs::read_to_string(&tmp_file).map_err(|e| format!("failed to read edited file: {e}"))
    }
}

fn which_available(name: &str) -> bool {
    Command::new("which")
        .arg(name)
        .status()
        .map(|s| s.success())
        .unwrap_or(false)
}
