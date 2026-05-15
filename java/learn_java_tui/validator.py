"""Compare program stdout to expected_output (trimmed), exit code 0."""

from __future__ import annotations

from dataclasses import dataclass

from learn_java_tui.chapters import Exercise
from learn_java_tui.executor import ExecutionResult


@dataclass
class ValidationResult:
    passed: bool
    message: str
    show_solution: bool


class Validator:
    def __init__(self, max_hints: int = 2) -> None:
        self.max_hints = max_hints

    def validate(
        self,
        exec_res: ExecutionResult,
        exercise: Exercise,
        hints_used: int,
    ) -> ValidationResult:
        if exec_res.timed_out:
            return ValidationResult(
                passed=False,
                message="Execution timed out after the configured limit.\n"
                + exec_res.stderr.strip(),
                show_solution=False,
            )

        if exec_res.exit_code != 0:
            msg = "Compile or run did not complete successfully.\n"
            if exec_res.stderr.strip():
                msg += exec_res.stderr.strip() + "\n"
            if exec_res.stdout.strip():
                msg += "stdout:\n" + exec_res.stdout.strip()
            return self._attach_hints(msg, exercise, hints_used, from_error=True)

        out = exec_res.stdout.strip()
        exp = exercise.expected_output.strip()
        if out == exp:
            return ValidationResult(
                passed=True,
                message="Correct! Your program produces the expected output.",
                show_solution=False,
            )

        msg = "Output doesn't match.\n"
        msg += f"Expected: {exp}\n"
        msg += f"Got:      {out}\n"
        return self._attach_hints(msg, exercise, hints_used, from_error=False)

    def _attach_hints(
        self,
        base: str,
        exercise: Exercise,
        hints_used: int,
        *,
        from_error: bool,
    ) -> ValidationResult:
        _ = from_error
        hint_idx = hints_used - 1
        if hints_used > 0 and hint_idx < len(exercise.hints):
            msg = base + "\n\nHint:\n" + exercise.hints[hint_idx]
            return ValidationResult(passed=False, message=msg, show_solution=False)

        if hints_used >= self.max_hints or hint_idx >= max(len(exercise.hints) - 1, 0):
            msg = base
            if exercise.solution.strip():
                msg += "\n\nHere's the solution:\n" + exercise.solution
            return ValidationResult(passed=False, message=msg, show_solution=True)

        return ValidationResult(passed=False, message=base, show_solution=False)
