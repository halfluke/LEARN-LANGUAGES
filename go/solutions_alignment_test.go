package main

import (
	"os"
	"strings"
	"testing"
)

// TestReferenceSolutionsViaExecutor ensures every bundled solution passes the same
// path learners use (ExecuteCode + Validator), not only check_solutions.py.
func TestReferenceSolutionsViaExecutor(t *testing.T) {
	if os.Getenv("SKIP_SOLUTION_ALIGNMENT") == "1" {
		t.Skip("SKIP_SOLUTION_ALIGNMENT=1")
	}

	loader := NewChapterLoader(GetDefaultChaptersDir())
	chapters, err := loader.LoadChapters()
	if err != nil {
		t.Fatalf("load chapters: %v", err)
	}

	executor := NewExecutor()
	validator := NewValidator()

	for i := range chapters {
		ch := &chapters[i]
		for j := range ch.Exercises {
			ex := &ch.Exercises[j]
			sol := strings.TrimSpace(ex.Solution)
			if sol == "" {
				continue
			}
			res, err := executor.ExecuteCode(sol, ex.ExpectedOutput)
			if err != nil {
				t.Fatalf("%s::%s: execute: %v", ch.ID, ex.ID, err)
			}
			v := validator.Validate(res, ex, 0)
			if !v.Passed {
				t.Errorf("%s::%s: %s", ch.ID, ex.ID, v.Message)
			}
		}
	}
}
