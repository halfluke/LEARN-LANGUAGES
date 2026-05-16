package main

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
)

// Editor handles launching the user's editor
type Editor struct {
	editorPath string
}

// NewEditor creates a new editor handler
func NewEditor() (*Editor, error) {
	editorPath := os.Getenv("EDITOR")
	if editorPath == "" {
		// Try common editors
		editors := []string{"nano", "micro", "vim", "nvim", "code", "subl"}
		for _, ed := range editors {
			if path, err := findEditor(ed); err == nil {
				editorPath = path
				break
			}
		}
	}

	if editorPath == "" {
		return nil, fmt.Errorf("no editor found. Set $EDITOR or install nano/vim/code")
	}

	return &Editor{editorPath: editorPath}, nil
}

func findEditor(name string) (string, error) {
	// Check if editor exists
	cmd := exec.Command("which", name)
	if err := cmd.Run(); err != nil {
		return "", fmt.Errorf("editor not found: %s", name)
	}
	return name, nil
}

// LaunchEditor opens the editor with the given code and returns the edited code
func (e *Editor) LaunchEditor(initialCode string) (string, error) {
	// Create temporary file
	tmpDir, err := os.MkdirTemp("", "learn-go-editor-*")
	if err != nil {
		return "", fmt.Errorf("failed to create temp dir: %w", err)
	}
	defer os.RemoveAll(tmpDir)

	tmpFile := filepath.Join(tmpDir, "main.go")

	// Write initial code
	if err := os.WriteFile(tmpFile, []byte(initialCode), 0644); err != nil {
		return "", fmt.Errorf("failed to write temp file: %w", err)
	}

	// Launch editor
	cmd := exec.Command(e.editorPath, tmpFile)
	cmd.Stdin = os.Stdin
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	if err := cmd.Run(); err != nil {
		return "", fmt.Errorf("editor exited with error: %w", err)
	}

	// Read back the file
	data, err := os.ReadFile(tmpFile)
	if err != nil {
		return "", fmt.Errorf("failed to read edited file: %w", err)
	}

	return string(data), nil
}

// GetEditorPath returns the editor path
func (e *Editor) GetEditorPath() string {
	return e.editorPath
}

// HasEditor checks if an editor is available
func HasEditor() bool {
	editorPath := os.Getenv("EDITOR")
	if editorPath != "" {
		return true
	}

	editors := []string{"nano", "micro", "vim", "nvim", "code", "subl"}
	for _, ed := range editors {
		if _, err := findEditor(ed); err == nil {
			return true
		}
	}

	return false
}
