package main

import (
	"bytes"
	"context"
	"fmt"
	"os"
	"os/exec"
	"time"
)

// ExecutionResult contains the result of code execution
type ExecutionResult struct {
	Stdout   string
	Stderr   string
	ExitCode int
	Error    error
	TimedOut bool
}

// Executor handles code execution
type Executor struct {
	timeout time.Duration
}

// NewExecutor creates a new executor
func NewExecutor() *Executor {
	return &Executor{
		timeout: 30 * time.Second,
	}
}

// ExecuteCode runs learner code in a temp module (go run . or go test).
func (e *Executor) ExecuteCode(code string, expectedOutput string) (*ExecutionResult, error) {
	tmpDir, err := os.MkdirTemp("", "learn-go-*")
	if err != nil {
		return nil, fmt.Errorf("failed to create temp directory: %w", err)
	}
	defer os.RemoveAll(tmpDir)

	mode, err := prepareSnippetWorkspace(tmpDir, code, expectedOutput)
	if err != nil {
		return nil, err
	}

	ctx, cancel := context.WithTimeout(context.Background(), e.timeout)
	defer cancel()

	var cmd *exec.Cmd
	switch mode {
	case runModeGoTest:
		cmd = exec.CommandContext(ctx, "go", "test", "-count=1")
	default:
		cmd = exec.CommandContext(ctx, "go", "run", ".")
	}
	cmd.Dir = tmpDir

	var stdout, stderr bytes.Buffer
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr

	err = cmd.Run()
	exitCode := 0
	if err != nil {
		if exitErr, ok := err.(*exec.ExitError); ok {
			exitCode = exitErr.ExitCode()
		} else if ctx.Err() == context.DeadlineExceeded {
			return &ExecutionResult{
				Stdout:   stdout.String(),
				Stderr:   stderr.String(),
				ExitCode: -1,
				Error:    fmt.Errorf("execution timed out after %s", e.timeout),
				TimedOut: true,
			}, nil
		} else {
			exitCode = 1
		}
	}

	return &ExecutionResult{
		Stdout:   stdout.String(),
		Stderr:   stderr.String(),
		ExitCode: exitCode,
		Error:    err,
	}, nil
}

// GetGoPath returns the path to the Go binary
func GetGoPath() string {
	paths := []string{
		"go",
		"/usr/local/go/bin/go",
		"/usr/local/go/bin/go.exe",
	}

	for _, path := range paths {
		cmd := exec.Command(path, "version")
		if err := cmd.Run(); err == nil {
			return path
		}
	}

	return "go"
}
