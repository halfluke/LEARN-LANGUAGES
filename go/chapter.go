package main

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"sort"
)

// Chapter represents a learning chapter loaded from JSON
type Chapter struct {
	ID            string     `json:"id"`
	Title         string     `json:"title"`
	Description   string     `json:"description"`
	Theory        string     `json:"theory"`
	Exercises     []Exercise `json:"exercises"`
	ExerciseCount int        `json:"exercise_count"`
}

// Exercise represents a single exercise in a chapter
type Exercise struct {
	ID             string   `json:"id"`
	Title          string   `json:"title"`
	Description    string   `json:"description"`
	StarterCode    string   `json:"starter_code"`
	ExpectedOutput string   `json:"expected_output"`
	Hints          []string `json:"hints"`
	Solution       string   `json:"solution"`
}

// ChapterLoader loads chapters from JSON files
type ChapterLoader struct {
	chaptersDir string
}

// NewChapterLoader creates a new chapter loader
func NewChapterLoader(chaptersDir string) *ChapterLoader {
	return &ChapterLoader{chaptersDir: chaptersDir}
}

// LoadChapters loads all chapters from the chapters directory
func (cl *ChapterLoader) LoadChapters() ([]Chapter, error) {
	// Read directory
	entries, err := os.ReadDir(cl.chaptersDir)
	if err != nil {
		return nil, fmt.Errorf("failed to read chapters directory: %w", err)
	}

	var paths []string
	for _, entry := range entries {
		if entry.IsDir() {
			continue
		}
		if filepath.Ext(entry.Name()) != ".json" {
			continue
		}
		paths = append(paths, entry.Name())
	}
	sort.Strings(paths)

	var chapters []Chapter
	for _, name := range paths {
		chapter, err := cl.loadChapterFile(filepath.Join(cl.chaptersDir, name))
		if err != nil {
			return nil, fmt.Errorf("failed to load %s: %w", name, err)
		}
		chapters = append(chapters, chapter)
	}

	if len(chapters) == 0 {
		return nil, fmt.Errorf("no chapters found in %s", cl.chaptersDir)
	}

	return chapters, nil
}

// loadChapterFile loads a single chapter from a JSON file
func (cl *ChapterLoader) loadChapterFile(path string) (Chapter, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return Chapter{}, fmt.Errorf("failed to read file: %w", err)
	}

	var chapter Chapter
	if err := json.Unmarshal(data, &chapter); err != nil {
		return Chapter{}, fmt.Errorf("failed to parse JSON: %w", err)
	}

	// Validate required fields
	if chapter.ID == "" {
		return Chapter{}, fmt.Errorf("missing required field: id")
	}
	if chapter.Title == "" {
		return Chapter{}, fmt.Errorf("missing required field: title")
	}
	if chapter.Description == "" {
		return Chapter{}, fmt.Errorf("missing required field: description")
	}

	// Validate exercises
	if len(chapter.Exercises) == 0 {
		return Chapter{}, fmt.Errorf("chapter has no exercises")
	}

	// Validate each exercise
	for i, ex := range chapter.Exercises {
		if ex.ID == "" {
			return Chapter{}, fmt.Errorf("exercise %d: missing id", i)
		}
		if ex.Title == "" {
			return Chapter{}, fmt.Errorf("exercise %d (%s): missing title", i, ex.ID)
		}
		if ex.StarterCode == "" {
			return Chapter{}, fmt.Errorf("exercise %d (%s): missing starter_code", i, ex.ID)
		}
		if ex.ExpectedOutput == "" {
			return Chapter{}, fmt.Errorf("exercise %d (%s): missing expected_output", i, ex.ID)
		}
		// Solution is optional but recommended
	}

	// Set exercise count
	chapter.ExerciseCount = len(chapter.Exercises)

	return chapter, nil
}

// LoadChapter loads a single chapter by ID
func (cl *ChapterLoader) LoadChapter(id string) (*Chapter, error) {
	chapters, err := cl.LoadChapters()
	if err != nil {
		return nil, err
	}

	for i := range chapters {
		if chapters[i].ID == id {
			return &chapters[i], nil
		}
	}

	return nil, fmt.Errorf("chapter not found: %s", id)
}

// GetDefaultChaptersDir returns the default chapters directory
func GetDefaultChaptersDir() string {
	return "chapters"
}
