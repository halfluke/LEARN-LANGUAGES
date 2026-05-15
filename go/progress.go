package main

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"time"
)

// Progress represents user progress
type Progress struct {
	ChapterID   string `json:"chapter_id"`
	ExerciseID  string `json:"exercise_id"`
	Completed   bool   `json:"completed"`
	Attempts    int    `json:"attempts"`
	HintsUsed   int    `json:"hints_used"`
	LastAttempt int64  `json:"last_attempt"` // unix timestamp
}

// ProgressStore manages progress persistence
type ProgressStore struct {
	filePath string
	progress []Progress
}

// NewProgressStore creates a new progress store
func NewProgressStore() *ProgressStore {
	homeDir, _ := os.UserHomeDir()
	storeDir := filepath.Join(homeDir, ".learn-go-tui")

	return &ProgressStore{
		filePath: filepath.Join(storeDir, "progress.json"),
		progress: []Progress{},
	}
}

// Load loads progress from file
func (ps *ProgressStore) Load() error {
	data, err := os.ReadFile(ps.filePath)
	if err != nil {
		if os.IsNotExist(err) {
			return nil // No progress file yet
		}
		return fmt.Errorf("failed to read progress: %w", err)
	}

	if err := json.Unmarshal(data, &ps.progress); err != nil {
		return fmt.Errorf("failed to parse progress: %w", err)
	}

	return nil
}

// Save saves progress to file
func (ps *ProgressStore) Save() error {
	// Ensure directory exists
	dir := filepath.Dir(ps.filePath)
	if err := os.MkdirAll(dir, 0755); err != nil {
		return fmt.Errorf("failed to create directory: %w", err)
	}

	data, err := json.MarshalIndent(ps.progress, "", "  ")
	if err != nil {
		return fmt.Errorf("failed to marshal progress: %w", err)
	}

	if err := os.WriteFile(ps.filePath, data, 0644); err != nil {
		return fmt.Errorf("failed to write progress: %w", err)
	}

	return nil
}

// GetProgress returns progress for a specific exercise
func (ps *ProgressStore) GetProgress(chapterID, exerciseID string) *Progress {
	for i := range ps.progress {
		p := &ps.progress[i]
		if p.ChapterID == chapterID && p.ExerciseID == exerciseID {
			return p
		}
	}
	return nil
}

// SaveProgress saves or updates progress for an exercise
func (ps *ProgressStore) SaveProgress(chapterID, exerciseID string, completed bool, attempts, hintsUsed int) {
	// Find existing progress
	for i := range ps.progress {
		p := &ps.progress[i]
		if p.ChapterID == chapterID && p.ExerciseID == exerciseID {
			p.Completed = completed || p.Completed
			if attempts > 0 {
				p.Attempts = attempts
			}
			if hintsUsed > 0 {
				p.HintsUsed = hintsUsed
			}
			p.LastAttempt = time.Now().Unix()
			return
		}
	}

	// Add new progress
	ps.progress = append(ps.progress, Progress{
		ChapterID:   chapterID,
		ExerciseID:  exerciseID,
		Completed:   completed,
		Attempts:    attempts,
		HintsUsed:   hintsUsed,
		LastAttempt: time.Now().Unix(),
	})
}

// GetCompletedExercises returns all completed exercise IDs for a chapter
func (ps *ProgressStore) GetCompletedExercises(chapterID string) []string {
	var completed []string
	for _, p := range ps.progress {
		if p.ChapterID == chapterID && p.Completed {
			completed = append(completed, p.ExerciseID)
		}
	}
	return completed
}

// IsCompleted checks if an exercise is completed
func (ps *ProgressStore) IsCompleted(chapterID, exerciseID string) bool {
	p := ps.GetProgress(chapterID, exerciseID)
	return p != nil && p.Completed
}
