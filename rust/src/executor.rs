use std::io::Read;
use std::path::PathBuf;
use std::process::{Command, Stdio};
use std::thread;
use std::time::{Duration, Instant};

#[derive(Debug, Clone)]
pub struct ExecutionResult {
    pub stdout: String,
    pub stderr: String,
    pub exit_code: i32,
    pub timed_out: bool,
    /// Set when the snippet was run with `cargo test` (see `#[test]` exercises).
    pub was_cargo_test: bool,
}

pub struct Executor {
    timeout: Duration,
    cargo_timeout: Duration,
}

impl Executor {
    pub fn new() -> Self {
        Self {
            timeout: Duration::from_secs(10),
            cargo_timeout: Duration::from_secs(120),
        }
    }

    pub fn execute_code(&self, code: &str) -> Result<ExecutionResult, String> {
        if needs_cargo_test(code) {
            self.execute_cargo_test(code)
        } else if needs_cargo(code) {
            self.execute_cargo_run(code)
        } else {
            self.execute_rustc_single_file(code)
        }
    }

    /// `rustc` only (fast). Use for exercises that stick to the standard library.
    fn execute_rustc_single_file(&self, code: &str) -> Result<ExecutionResult, String> {
        let tmp = unique_tmp_dir();
        std::fs::create_dir_all(&tmp).map_err(|e| format!("failed to create temp directory: {e}"))?;

        let main_rs = tmp.join("main.rs");
        let bin_path = tmp.join("learn_rust_run");

        std::fs::write(&main_rs, code).map_err(|e| format!("failed to write code file: {e}"))?;

        let compile = run_command_limited(
            Command::new("rustc")
                .arg(&main_rs)
                .arg("-o")
                .arg(&bin_path)
                .stdin(Stdio::null()),
            self.timeout,
        )?;

        if compile.timed_out {
            let _ = std::fs::remove_dir_all(&tmp);
            return Ok(ExecutionResult {
                stdout: compile.stdout,
                stderr: compile.stderr,
                exit_code: -1,
                timed_out: true,
                was_cargo_test: false,
            });
        }

        if compile.exit_code != 0 {
            let _ = std::fs::remove_dir_all(&tmp);
            return Ok(ExecutionResult {
                stdout: compile.stdout,
                stderr: compile.stderr,
                exit_code: compile.exit_code,
                timed_out: false,
                was_cargo_test: false,
            });
        }

        let run = run_command_limited(
            Command::new(&bin_path).stdin(Stdio::null()),
            self.timeout,
        )?;

        let _ = std::fs::remove_dir_all(&tmp);

        Ok(ExecutionResult {
            stdout: run.stdout,
            stderr: run.stderr,
            exit_code: run.exit_code,
            timed_out: run.timed_out,
            was_cargo_test: false,
        })
    }

    /// Same temp crate as `execute_cargo_run`, but runs `cargo test` for `#[test]` snippets.
    fn execute_cargo_test(&self, code: &str) -> Result<ExecutionResult, String> {
        let tmp = unique_tmp_dir();
        std::fs::create_dir_all(&tmp).map_err(|e| format!("failed to create temp directory: {e}"))?;

        let st = Command::new("cargo")
            .args(["init", "--name", "snippet", "--bin"])
            .current_dir(&tmp)
            .stdout(Stdio::null())
            .stderr(Stdio::piped())
            .status()
            .map_err(|e| format!("failed to run cargo init: {e}"))?;

        if !st.success() {
            let _ = std::fs::remove_dir_all(&tmp);
            return Err("cargo init failed (is cargo installed?)".into());
        }

        std::fs::write(tmp.join("Cargo.toml"), cargo_snippet_toml())
            .map_err(|e| format!("failed to write Cargo.toml: {e}"))?;
        std::fs::write(tmp.join("src").join("main.rs"), code)
            .map_err(|e| format!("failed to write main.rs: {e}"))?;

        let run = run_command_limited(
            Command::new("cargo")
                .args(["test", "--quiet"])
                .current_dir(&tmp)
                .stdin(Stdio::null()),
            self.cargo_timeout,
        )?;

        let _ = std::fs::remove_dir_all(&tmp);

        Ok(ExecutionResult {
            stdout: run.stdout,
            stderr: run.stderr,
            exit_code: run.exit_code,
            timed_out: run.timed_out,
            was_cargo_test: true,
        })
    }

    /// Temporary Cargo project with common crates (serde JSON, chrono / time zones).
    fn execute_cargo_run(&self, code: &str) -> Result<ExecutionResult, String> {
        let tmp = unique_tmp_dir();
        std::fs::create_dir_all(&tmp).map_err(|e| format!("failed to create temp directory: {e}"))?;

        let st = Command::new("cargo")
            .args(["init", "--name", "snippet", "--bin"])
            .current_dir(&tmp)
            .stdout(Stdio::null())
            .stderr(Stdio::piped())
            .status()
            .map_err(|e| format!("failed to run cargo init: {e}"))?;

        if !st.success() {
            let _ = std::fs::remove_dir_all(&tmp);
            return Err("cargo init failed (is cargo installed?)".into());
        }

        std::fs::write(tmp.join("Cargo.toml"), cargo_snippet_toml())
            .map_err(|e| format!("failed to write Cargo.toml: {e}"))?;
        std::fs::write(tmp.join("src").join("main.rs"), code)
            .map_err(|e| format!("failed to write main.rs: {e}"))?;

        let run = run_command_limited(
            Command::new("cargo")
                .args(["run", "--quiet"])
                .current_dir(&tmp)
                .stdin(Stdio::null()),
            self.cargo_timeout,
        )?;

        let _ = std::fs::remove_dir_all(&tmp);

        Ok(ExecutionResult {
            stdout: run.stdout,
            stderr: run.stderr,
            exit_code: run.exit_code,
            timed_out: run.timed_out,
            was_cargo_test: false,
        })
    }
}

fn cargo_snippet_toml() -> &'static str {
    r#"[package]
name = "snippet"
version = "0.1.0"
edition = "2021"

[dependencies]
serde = { version = "1", features = ["derive"] }
serde_json = "1"
chrono = { version = "0.4", default-features = false, features = ["clock", "std"] }
chrono-tz = "0.10"
"#
}

fn needs_cargo_test(code: &str) -> bool {
    code.contains("#[test]")
}

/// Crates not available to plain `rustc` on a single file.
fn needs_cargo(code: &str) -> bool {
    code.contains("serde_json::")
        || code.contains("serde::")
        || code.contains("chrono::")
        || code.contains("chrono_tz::")
}

struct CmdOutput {
    stdout: String,
    stderr: String,
    exit_code: i32,
    timed_out: bool,
}

fn run_command_limited(cmd: &mut Command, timeout: Duration) -> Result<CmdOutput, String> {
    cmd.stdout(Stdio::piped()).stderr(Stdio::piped());

    let mut child = cmd
        .spawn()
        .map_err(|e| format!("failed to spawn process: {e}"))?;

    let mut stdout_pipe = child.stdout.take().ok_or("missing stdout pipe")?;
    let mut stderr_pipe = child.stderr.take().ok_or("missing stderr pipe")?;

    let stdout_handle = thread::spawn(move || {
        let mut buf = Vec::new();
        let _ = stdout_pipe.read_to_end(&mut buf);
        buf
    });
    let stderr_handle = thread::spawn(move || {
        let mut buf = Vec::new();
        let _ = stderr_pipe.read_to_end(&mut buf);
        buf
    });

    let deadline = Instant::now() + timeout;

    loop {
        match child
            .try_wait()
            .map_err(|e| format!("error waiting for child: {e}"))?
        {
            Some(status) => {
                let stdout_bytes = stdout_handle.join().map_err(|_| "stdout join failed")?;
                let stderr_bytes = stderr_handle.join().map_err(|_| "stderr join failed")?;
                return Ok(CmdOutput {
                    stdout: String::from_utf8_lossy(&stdout_bytes).into_owned(),
                    stderr: String::from_utf8_lossy(&stderr_bytes).into_owned(),
                    exit_code: status.code().unwrap_or(-1),
                    timed_out: false,
                });
            }
            None => {
                if Instant::now() >= deadline {
                    let _ = child.kill();
                    let _ = child.wait();
                    let stdout_bytes = stdout_handle.join().map_err(|_| "stdout join failed")?;
                    let stderr_bytes = stderr_handle.join().map_err(|_| "stderr join failed")?;
                    return Ok(CmdOutput {
                        stdout: String::from_utf8_lossy(&stdout_bytes).into_owned(),
                        stderr: String::from_utf8_lossy(&stderr_bytes).into_owned(),
                        exit_code: -1,
                        timed_out: true,
                    });
                }
                thread::sleep(Duration::from_millis(10));
            }
        }
    }
}

fn unique_tmp_dir() -> PathBuf {
    let nanos = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .unwrap_or_default()
        .as_nanos();
    std::env::temp_dir().join(format!("learn-rust-{nanos}"))
}
