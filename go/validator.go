package main

import (
	"strings"
)

// ValidationResult contains the result of validation
type ValidationResult struct {
	Passed       bool
	Message      string
	ShowSolution bool
}

// Validator validates code execution results
type Validator struct {
	maxHints int
}

// NewValidator creates a new validator
func NewValidator() *Validator {
	return &Validator{
		maxHints: 2,
	}
}

// Validate checks the execution result against expected output
func (v *Validator) Validate(execRes *ExecutionResult, exercise *Exercise, hintsUsed int) *ValidationResult {
	expected := strings.TrimSpace(exercise.ExpectedOutput)

	if expected == "PASS" {
		if execRes.TimedOut {
			return v.handleCompilationError(execRes, exercise, hintsUsed)
		}
		if execRes.ExitCode == 0 {
			return &ValidationResult{
				Passed:  true,
				Message: "Correct! All tests passed.",
			}
		}
		return v.handleCompilationError(execRes, exercise, hintsUsed)
	}

	// Build/run failure
	if execRes.ExitCode != 0 {
		return v.handleCompilationError(execRes, exercise, hintsUsed)
	}

	// Compare stdout (ignore stderr on success — e.g. go run cache lines)
	output := strings.TrimSpace(execRes.Stdout)

	if output == expected {
		return &ValidationResult{
			Passed:  true,
			Message: "Correct! Your code produces the expected output.",
		}
	}

	// Output doesn't match - provide hint
	return v.handleOutputMismatch(execRes, exercise, hintsUsed)
}

func (v *Validator) handleCompilationError(execRes *ExecutionResult, exercise *Exercise, hintsUsed int) *ValidationResult {
	msg := "Compilation failed:\n" + execRes.Stderr

	// Get hint for this hint request (hintUsed counts from 1)
	hintIdx := hintsUsed - 1
	if hintsUsed > 0 && hintIdx < len(exercise.Hints) {
		msg += "\n\nHint:\n" + exercise.Hints[hintIdx]
	} else if hintsUsed >= v.maxHints || hintIdx >= len(exercise.Hints)-1 {
		msg += "\n\nHere's the solution:\n" + exercise.Solution
		return &ValidationResult{
			Passed:       false,
			Message:      msg,
			ShowSolution: true,
		}
	}

	return &ValidationResult{
		Passed:  false,
		Message: msg,
	}
}

func (v *Validator) handleOutputMismatch(execRes *ExecutionResult, exercise *Exercise, hintsUsed int) *ValidationResult {
	output := strings.TrimSpace(execRes.Stdout)
	expected := strings.TrimSpace(exercise.ExpectedOutput)

	msg := "Output doesn't match.\n"
	msg += "Expected: " + expected + "\n"
	msg += "Got:      " + output

	// Show hint for this request
	hintIdx := hintsUsed - 1
	if hintsUsed > 0 && hintIdx < len(exercise.Hints) {
		msg += "\n\nHint:\n" + exercise.Hints[hintIdx]
	} else if hintsUsed >= v.maxHints || hintIdx >= len(exercise.Hints)-1 {
		msg += "\n\nHere's the solution:\n" + exercise.Solution
		return &ValidationResult{
			Passed:       false,
			Message:      msg,
			ShowSolution: true,
		}
	}

	return &ValidationResult{
		Passed:  false,
		Message: msg,
	}
}
