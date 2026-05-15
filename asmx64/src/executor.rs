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
}

pub struct Executor {
    assemble_timeout: Duration,
    run_timeout: Duration,
}

impl Executor {
    pub fn new() -> Self {
        Self {
            assemble_timeout: Duration::from_secs(30),
            run_timeout: Duration::from_secs(10),
        }
    }

    /// Assemble NASM Intel → ELF64, link with `ld` (syscall-only) or `gcc` (libc `extern`),
    /// then run the binary.
    pub fn execute_code(&self, code: &str) -> Result<ExecutionResult, String> {
        let tmp = unique_tmp_dir();
        std::fs::create_dir_all(&tmp).map_err(|e| format!("failed to create temp directory: {e}"))?;

        let asm_path = tmp.join("solution.asm");
        let obj_path = tmp.join("solution.o");
        let bin_path = tmp.join("solution");

        std::fs::write(&asm_path, code).map_err(|e| format!("failed to write solution.asm: {e}"))?;

        let nasm = run_command_limited(
            Command::new("nasm")
                .args(["-f", "elf64", "-o"])
                .arg(&obj_path)
                .arg(&asm_path)
                .stdin(Stdio::null()),
            self.assemble_timeout,
        )?;

        if nasm.timed_out {
            let _ = std::fs::remove_dir_all(&tmp);
            return Ok(timed_out_result(nasm));
        }
        if nasm.exit_code != 0 {
            let _ = std::fs::remove_dir_all(&tmp);
            return Ok(ExecutionResult {
                stdout: nasm.stdout,
                stderr: nasm.stderr,
                exit_code: nasm.exit_code,
                timed_out: false,
            });
        }

        let link = if needs_gcc_link(code) {
            run_command_limited(
                Command::new("gcc")
                    .args(["-no-pie", "-o"])
                    .arg(&bin_path)
                    .arg(&obj_path)
                    .stdin(Stdio::null()),
                self.assemble_timeout,
            )?
        } else {
            run_command_limited(
                Command::new("ld")
                    .arg("-o")
                    .arg(&bin_path)
                    .arg(&obj_path)
                    .stdin(Stdio::null()),
                self.assemble_timeout,
            )?
        };

        if link.timed_out {
            let _ = std::fs::remove_dir_all(&tmp);
            return Ok(timed_out_result(link));
        }
        if link.exit_code != 0 {
            let _ = std::fs::remove_dir_all(&tmp);
            return Ok(ExecutionResult {
                stdout: link.stdout,
                stderr: link.stderr,
                exit_code: link.exit_code,
                timed_out: false,
            });
        }

        let run = run_command_limited(
            Command::new(&bin_path).stdin(Stdio::null()),
            self.run_timeout,
        )?;

        let _ = std::fs::remove_dir_all(&tmp);

        Ok(ExecutionResult {
            stdout: run.stdout,
            stderr: run.stderr,
            exit_code: run.exit_code,
            timed_out: run.timed_out,
        })
    }
}

fn timed_out_result(c: CmdOutput) -> ExecutionResult {
    ExecutionResult {
        stdout: c.stdout,
        stderr: c.stderr,
        exit_code: -1,
        timed_out: true,
    }
}

/// Link with **gcc** when the snippet declares libc symbols (`extern`).
fn needs_gcc_link(code: &str) -> bool {
    code.to_ascii_lowercase().contains("extern")
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
    std::env::temp_dir().join(format!("learn-asmx64-{nanos}"))
}
