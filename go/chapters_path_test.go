package main

import (
	"os"
	"path/filepath"
	"testing"
)

func TestGetDefaultChaptersDir_fromCwd(t *testing.T) {
	t.Setenv(chaptersEnvVar, "")
	wd, err := os.Getwd()
	if err != nil {
		t.Fatal(err)
	}
	ch := filepath.Join(wd, "chapters")
	if !chaptersDirValid(ch) {
		t.Skip("no chapters/ in", wd)
	}
	got := GetDefaultChaptersDir()
	if !chaptersDirValid(got) {
		t.Fatalf("GetDefaultChaptersDir() = %q, not a valid chapters dir", got)
	}
}

func TestGetDefaultChaptersDir_envOverride(t *testing.T) {
	wd, _ := os.Getwd()
	ch := filepath.Join(wd, "chapters")
	if !chaptersDirValid(ch) {
		t.Skip("no chapters/")
	}
	t.Setenv(chaptersEnvVar, ch)
	got := GetDefaultChaptersDir()
	if got != ch {
		t.Fatalf("env override: got %q want %q", got, ch)
	}
}
