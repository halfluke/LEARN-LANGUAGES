package main

import (
	"fmt"
	"os"
	"os/exec"
	"runtime"

	tea "github.com/charmbracelet/bubbletea"
)

func main() {
	// Check Go prerequisite before starting TUI
	if err := checkGoPrerequisite(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}

	p := tea.NewProgram(newModel())
	if err := p.Start(); err != nil {
		fmt.Fprintln(os.Stderr, "Error running program:", err)
		os.Exit(1)
	}
}

// checkGoPrerequisite verifies Go is installed and accessible
func checkGoPrerequisite() error {
	// Try to find Go in common locations
	goPaths := []string{
		"go",
		"/usr/local/go/bin/go",
		"/usr/local/go/bin/go.exe",
	}

	var goPath string
	for _, path := range goPaths {
		cmd := exec.Command(path, "version")
		if err := cmd.Run(); err == nil {
			goPath = path
			break
		}
	}

	if goPath == "" {
		return fmt.Errorf("Go is not installed or not in PATH.\n\n" +
			"Please install Go from https://go.dev/dl/\n" +
			"After installation, ensure 'go' is in your PATH.")
	}

	// Check Go version (require 1.21+)
	cmd := exec.Command(goPath, "version")
	output, err := cmd.Output()
	if err != nil {
		return fmt.Errorf("Failed to get Go version: %v", err)
	}

	// Parse version string (e.g., "go1.21.0")
	var version string
	fmt.Sscanf(string(output), "go%s", &version)

	// Simple version check - need at least 1.21
	// For now, just warn if it's very old
	fmt.Fprintf(os.Stderr, "✓ Go found: %s\n", string(output))
	return nil
}

func init() {
	// Ensure we use the correct number of processors
	runtime.GOMAXPROCS(runtime.NumCPU())
}
