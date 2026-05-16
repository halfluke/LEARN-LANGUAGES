package main

import (
	"os"
	"path/filepath"
	"strings"
)

const chaptersEnvVar = "LEARN_GO_CHAPTERS"

// GetDefaultChaptersDir resolves where chapter JSON lives.
//
// Order: LEARN_GO_CHAPTERS → ./chapters (cwd) → chapters next to repo root (walk up from executable) → "chapters".
func GetDefaultChaptersDir() string {
	if v := strings.TrimSpace(os.Getenv(chaptersEnvVar)); v != "" {
		return v
	}
	if cwd, err := os.Getwd(); err == nil {
		if p := filepath.Join(cwd, "chapters"); chaptersDirValid(p) {
			return p
		}
	}
	if exe, err := os.Executable(); err == nil {
		dir := filepath.Dir(exe)
		for i := 0; i < 6; i++ {
			if p := filepath.Join(dir, "chapters"); chaptersDirValid(p) {
				return p
			}
			parent := filepath.Dir(dir)
			if parent == dir {
				break
			}
			dir = parent
		}
	}
	// Dev default when run from go/ via hub or `go run .`
	if chaptersDirValid("chapters") {
		return "chapters"
	}
	return "chapters"
}

func chaptersDirValid(path string) bool {
	entries, err := os.ReadDir(path)
	if err != nil {
		return false
	}
	for _, e := range entries {
		if !e.IsDir() && strings.HasSuffix(strings.ToLower(e.Name()), ".json") {
			return true
		}
	}
	return false
}
