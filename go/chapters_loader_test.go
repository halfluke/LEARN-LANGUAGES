package main

import (
	"os"
	"testing"
)

func TestNewChapterFilesLoad(t *testing.T) {
	loader := NewChapterLoader("chapters")
	chapters, err := loader.LoadChapters()
	if err != nil {
		t.Fatalf("Failed to load chapters: %v", err)
	}

	// Count all loaded chapters
	t.Logf("Loaded %d chapters total", len(chapters))
	for _, ch := range chapters {
		t.Logf("  - %s: %s (%d exercises)", ch.ID, ch.Title, ch.ExerciseCount)
	}

	// Find and verify time chapter
	timeChapter := findChapter(chapters, "time")
	if timeChapter == nil {
		t.Fatal("time chapter not found in loaded chapters")
	}
	if timeChapter.Title != "Time" {
		t.Errorf("time chapter title = %q, want %q", timeChapter.Title, "Time")
	}
	if timeChapter.ExerciseCount != 9 {
		t.Errorf("time chapter has %d exercises, want 9", timeChapter.ExerciseCount)
	}
	for _, ex := range timeChapter.Exercises {
		if ex.ID == "" || ex.Title == "" || ex.StarterCode == "" || ex.ExpectedOutput == "" {
			t.Errorf("time exercise %s has missing required field", ex.ID)
		}
	}

	// Find and verify json chapter
	jsonChapter := findChapter(chapters, "json")
	if jsonChapter == nil {
		t.Fatal("json chapter not found in loaded chapters")
	}
	if jsonChapter.Title != "JSON" {
		t.Errorf("json chapter title = %q, want %q", jsonChapter.Title, "JSON")
	}
	if jsonChapter.ExerciseCount != 9 {
		t.Errorf("json chapter has %d exercises, want 9", jsonChapter.ExerciseCount)
	}
	for _, ex := range jsonChapter.Exercises {
		if ex.ID == "" || ex.Title == "" || ex.StarterCode == "" || ex.ExpectedOutput == "" {
			t.Errorf("json exercise %s has missing required field", ex.ID)
		}
	}

	// Total chapters should match curriculum (18 Go chapters: no lifetimes slot)
	if len(chapters) != 18 {
		t.Errorf("total chapters = %d, want 18", len(chapters))
	}
}

func findChapter(chapters []Chapter, id string) *Chapter {
	for i := range chapters {
		if chapters[i].ID == id {
			return &chapters[i]
		}
	}
	return nil
}

func TestChapterFileContents(t *testing.T) {
	// Verify files are valid JSON and not empty
	for _, name := range []string{"19_time.json", "18_json.json"} {
		data, err := os.ReadFile("chapters/" + name)
		if err != nil {
			t.Fatalf("%s: failed to read: %v", name, err)
		}
		if len(data) == 0 {
			t.Errorf("%s: file is empty", name)
		}
	}
}
