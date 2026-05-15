use crate::chapter::Exercise;
use crate::executor::ExecutionResult;

#[derive(Debug, Clone)]
pub struct ValidationResult {
    pub passed: bool,
    pub message: String,
    pub show_solution: bool,
}

pub struct Validator {
    max_hints: usize,
}

impl Validator {
    pub fn new() -> Self {
        Self { max_hints: 2 }
    }

    pub fn validate(
        &self,
        exec_res: &ExecutionResult,
        exercise: &Exercise,
        hints_used: usize,
    ) -> ValidationResult {
        if exec_res.timed_out {
            return ValidationResult {
                passed: false,
                message: format!(
                    "Execution timed out after the configured limit.\n{}",
                    exec_res.stderr.trim()
                ),
                show_solution: false,
            };
        }

        let expected = exercise.expected_output.trim();
        if exec_res.was_cargo_test && expected == "PASS" {
            if exec_res.exit_code == 0 {
                return ValidationResult {
                    passed: true,
                    message: "Correct! All tests passed.".into(),
                    show_solution: false,
                };
            }
            return self.handle_nonzero_exit(exec_res, exercise, hints_used);
        }

        if exec_res.exit_code != 0 {
            return self.handle_nonzero_exit(exec_res, exercise, hints_used);
        }

        let output = exec_res.stdout.trim();

        if output == expected {
            return ValidationResult {
                passed: true,
                message: "Correct! Your code produces the expected output.".into(),
                show_solution: false,
            };
        }

        self.handle_output_mismatch(exec_res, exercise, hints_used)
    }

    fn handle_nonzero_exit(
        &self,
        exec_res: &ExecutionResult,
        exercise: &Exercise,
        hints_used: usize,
    ) -> ValidationResult {
        let mut msg = String::from("Program did not complete successfully.\n");
        if !exec_res.stderr.trim().is_empty() {
            msg.push_str(exec_res.stderr.trim());
            msg.push('\n');
        }
        if !exec_res.stdout.trim().is_empty() {
            msg.push_str("stdout:\n");
            msg.push_str(exec_res.stdout.trim());
        }

        self.attach_hints_or_solution(&mut msg, exercise, hints_used, true)
    }

    fn handle_output_mismatch(
        &self,
        exec_res: &ExecutionResult,
        exercise: &Exercise,
        hints_used: usize,
    ) -> ValidationResult {
        let output = exec_res.stdout.trim();
        let expected = exercise.expected_output.trim();

        let mut msg = String::from("Output doesn't match.\n");
        msg.push_str(&format!("Expected: {expected}\n"));
        msg.push_str(&format!("Got:      {output}\n"));

        self.attach_hints_or_solution(&mut msg, exercise, hints_used, false)
    }

    fn attach_hints_or_solution(
        &self,
        msg: &mut String,
        exercise: &Exercise,
        hints_used: usize,
        _from_error: bool,
    ) -> ValidationResult {
        let hint_idx = hints_used.saturating_sub(1);

        if hints_used > 0 && hint_idx < exercise.hints.len() {
            msg.push_str("\nHint:\n");
            msg.push_str(&exercise.hints[hint_idx]);
            return ValidationResult {
                passed: false,
                message: msg.clone(),
                show_solution: false,
            };
        }

        if hints_used >= self.max_hints || hint_idx >= exercise.hints.len().saturating_sub(1) {
            if !exercise.solution.trim().is_empty() {
                msg.push_str("\n\nHere's the solution:\n");
                msg.push_str(&exercise.solution);
            }
            return ValidationResult {
                passed: false,
                message: msg.clone(),
                show_solution: true,
            };
        }

        ValidationResult {
            passed: false,
            message: msg.clone(),
            show_solution: false,
        }
    }
}
