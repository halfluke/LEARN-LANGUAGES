package main

import (
	"encoding/json"
	"os"
	"path/filepath"
	"testing"
)

func TestLoadChapters(t *testing.T) {
	loader := NewChapterLoader("chapters")
	chapters, err := loader.LoadChapters()
	if err != nil {
		t.Fatalf("LoadChapters failed: %v", err)
	}

	if len(chapters) < 18 {
		t.Errorf("expected at least 18 chapters, got %d", len(chapters))
	}

	// Verify new chapters are present
	chapterMap := make(map[string]Chapter)
	for _, ch := range chapters {
		chapterMap[ch.ID] = ch
	}

	// Test packages chapter
	packages, ok := chapterMap["packages"]
	if !ok {
		t.Fatal("packages chapter not found in loaded chapters")
	}
	if packages.Title != "Packages" {
		t.Errorf("packages chapter title = %q, want %q", packages.Title, "Packages")
	}
	if packages.ExerciseCount != 7 {
		t.Errorf("packages exercise count = %d, want 7", packages.ExerciseCount)
	}
	for i, ex := range packages.Exercises {
		if ex.ID == "" {
			t.Errorf("packages exercise %d: missing id", i)
		}
		if ex.Title == "" {
			t.Errorf("packages exercise %d (%s): missing title", i, ex.ID)
		}
	}

	// Test strings chapter
	strings, ok := chapterMap["strings"]
	if !ok {
		t.Fatal("strings chapter not found in loaded chapters")
	}
	if strings.Title != "Strings & Runes" {
		t.Errorf("strings chapter title = %q, want %q", strings.Title, "Strings & Runes")
	}
	if strings.ExerciseCount != 7 {
		t.Errorf("strings exercise count = %d, want 7", strings.ExerciseCount)
	}
	for i, ex := range strings.Exercises {
		if ex.ID == "" {
			t.Errorf("strings exercise %d: missing id", i)
		}
		if ex.Title == "" {
			t.Errorf("strings exercise %d (%s): missing title", i, ex.ID)
		}
	}
}

func TestLoadSingleChapter(t *testing.T) {
	loader := NewChapterLoader("chapters")

	// Test packages
	ch, err := loader.LoadChapter("packages")
	if err != nil {
		t.Fatalf("LoadChapter(packages) failed: %v", err)
	}
	if ch.ID != "packages" {
		t.Errorf("packages chapter id = %q, want %q", ch.ID, "packages")
	}

	// Test strings
	ch, err = loader.LoadChapter("strings")
	if err != nil {
		t.Fatalf("LoadChapter(strings) failed: %v", err)
	}
	if ch.ID != "strings" {
		t.Errorf("strings chapter id = %q, want %q", ch.ID, "strings")
	}

	// Test missing chapter
	_, err = loader.LoadChapter("nonexistent")
	if err == nil {
		t.Fatal("LoadChapter(nonexistent) should return error")
	}
}

func TestChapterFileValidation(t *testing.T) {
	dir := "chapters"
	files, err := os.ReadDir(dir)
	if err != nil {
		t.Fatalf("ReadDir(chapters) failed: %v", err)
	}

	jsonCount := 0
	loader := NewChapterLoader(dir)
	for _, f := range files {
		if f.IsDir() {
			continue
		}
		if filepath.Ext(f.Name()) != ".json" {
			continue
		}
		jsonCount++
		data, err := os.ReadFile(filepath.Join(dir, f.Name()))
		if err != nil {
			t.Fatalf("read %s: %v", f.Name(), err)
		}
		var meta struct {
			ID string `json:"id"`
		}
		if err := json.Unmarshal(data, &meta); err != nil {
			t.Fatalf("parse %s: %v", f.Name(), err)
		}
		if meta.ID == "" {
			t.Errorf("%s: missing id in JSON", f.Name())
			continue
		}
		_, err = loader.LoadChapter(meta.ID)
		if err != nil {
			t.Errorf("Failed to load chapter id %q from %s: %v", meta.ID, f.Name(), err)
		}
	}

	if jsonCount < 10 {
		t.Errorf("expected at least 10 JSON chapter files, got %d", jsonCount)
	}
}
