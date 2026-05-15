package main

import (
	"bytes"
	"context"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
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
		timeout: 10 * time.Second, // 10 second timeout
	}
}

// ExecuteCode runs the user code and returns the result
func (e *Executor) ExecuteCode(code string) (*ExecutionResult, error) {
	// Create temporary directory
	tmpDir, err := os.MkdirTemp("", "learn-go-*")
	if err != nil {
		return nil, fmt.Errorf("failed to create temp directory: %w", err)
	}
	defer os.RemoveAll(tmpDir)

	// Write code to main.go
	mainFile := filepath.Join(tmpDir, "main.go")
	if err := os.WriteFile(mainFile, []byte(code), 0644); err != nil {
		return nil, fmt.Errorf("failed to write code file: %w", err)
	}

	// Create context with timeout
	ctx, cancel := context.WithTimeout(context.Background(), e.timeout)
	defer cancel()

	// Run go run
	cmd := exec.CommandContext(ctx, "go", "run", mainFile)

	var stdout, stderr bytes.Buffer
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr

	err = cmd.Run()
	exitCode := 0
	if err != nil {
		if exitErr, ok := err.(*exec.ExitError); ok {
			exitCode = exitErr.ExitCode()
		} else {
			// Check if it was a timeout
			if ctx.Err() == context.DeadlineExceeded {
				return &ExecutionResult{
					Stdout:   stdout.String(),
					Stderr:   stderr.String(),
					ExitCode: -1,
					Error:    fmt.Errorf("execution timed out after %s", e.timeout),
					TimedOut: true,
				}, nil
			}
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

	return "go" // fallback
}
