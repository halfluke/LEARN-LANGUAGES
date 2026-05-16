package main

import (
	"os"
	"path/filepath"
	"testing"
)

func TestParseSourceFiles_splitTest(t *testing.T) {
	code := "package main\n\nfunc Sum(a, b int) int { return a + b }\n\nfunc main() {}\n\n---\npackage main\n\nimport \"testing\"\n\nfunc TestSum(t *testing.T) {\n    if Sum(2, 3) != 5 { t.Fail() }\n}"
	files, err := parseSourceFiles(code, "PASS")
	if err != nil {
		t.Fatal(err)
	}
	if len(files) != 2 {
		t.Fatalf("got %d files", len(files))
	}
	if files["main_test.go"] == "" {
		t.Fatal("missing main_test.go")
	}
}

func TestParseSourceFiles_fileMarkers(t *testing.T) {
	code := "// File: main.go\npackage main\n\nimport \"learnsnippet/utils\"\n\nfunc main() { utils.Greet() }\n\n// File: utils/utils.go\npackage utils\n\nimport \"fmt\"\n\nfunc Greet() { fmt.Println(\"Hello from utils\") }\n"
	files, err := parseSourceFiles(code, "Hello from utils")
	if err != nil {
		t.Fatal(err)
	}
	if len(files) != 2 {
		t.Fatalf("got %v", files)
	}
}

func TestPrepareSnippetWorkspace_goTest(t *testing.T) {
	dir := t.TempDir()
	code := "package main\n\nfunc N() int { return 1 }\n\n---\npackage main\n\nimport \"testing\"\n\nfunc TestN(t *testing.T) { if N() != 1 { t.Fail() } }"
	mode, err := prepareSnippetWorkspace(dir, code, "PASS")
	if err != nil {
		t.Fatal(err)
	}
	if mode != runModeGoTest {
		t.Fatalf("mode %v", mode)
	}
	if _, err := os.Stat(filepath.Join(dir, "go.mod")); err != nil {
		t.Fatal(err)
	}
}
