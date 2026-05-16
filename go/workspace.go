package main

import (
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"strings"
)

const (
	snippetModule = "learnsnippet"
	goModTemplate = "module learnsnippet\n\ngo 1.21\n"
)

type runMode int

const (
	runModeGoRun runMode = iota
	runModeGoTest
)

var pathHeaderRe = regexp.MustCompile(`(?i)^\s*//\s*(?:File:\s*|path:\s*)(\S+)\s*$`)

// prepareSnippetWorkspace writes learner code into tmpDir as a small Go module.
func prepareSnippetWorkspace(tmpDir, code, expectedOutput string) (runMode, error) {
	files, err := parseSourceFiles(code, expectedOutput)
	if err != nil {
		return runModeGoRun, err
	}
	for rel, body := range files {
		rel = filepath.Clean(rel)
		if strings.HasPrefix(rel, "..") {
			return runModeGoRun, fmt.Errorf("invalid path %q", rel)
		}
		full := filepath.Join(tmpDir, rel)
		if err := os.MkdirAll(filepath.Dir(full), 0o755); err != nil {
			return runModeGoRun, err
		}
		if !strings.HasSuffix(body, "\n") {
			body += "\n"
		}
		if err := os.WriteFile(full, []byte(body), 0o644); err != nil {
			return runModeGoRun, err
		}
	}
	if err := os.WriteFile(filepath.Join(tmpDir, "go.mod"), []byte(goModTemplate), 0o644); err != nil {
		return runModeGoRun, err
	}
	if strings.TrimSpace(expectedOutput) == "PASS" {
		return runModeGoTest, nil
	}
	return runModeGoRun, nil
}

func parseSourceFiles(code, expectedOutput string) (map[string]string, error) {
	code = strings.TrimSpace(code)
	if code == "" {
		return nil, fmt.Errorf("empty source")
	}

	if strings.Contains(code, "\n---\n") {
		return parseSplitParts(code), nil
	}

	if markerFiles := parseFileMarkerSections(code); len(markerFiles) > 1 {
		return markerFiles, nil
	}

	if strings.TrimSpace(expectedOutput) == "PASS" {
		if main, test, ok := splitTestCompanion(code); ok {
			return map[string]string{"main.go": main, "main_test.go": test}, nil
		}
	}

	path, body := splitPathHeader(code)
	if path != "" {
		return map[string]string{path: body}, nil
	}

	return map[string]string{"main.go": code}, nil
}

func parseSplitParts(code string) map[string]string {
	parts := strings.Split(code, "\n---\n")
	files := make(map[string]string, len(parts))
	for i, part := range parts {
		part = strings.TrimSpace(part)
		if part == "" {
			continue
		}
		path, body := splitPathHeader(part)
		if path == "" {
			path = defaultFileName(part, i)
		}
		files[path] = body
	}
	return files
}

func parseFileMarkerSections(code string) map[string]string {
	lines := strings.Split(code, "\n")
	files := make(map[string]string)
	var currentPath string
	var bodyLines []string

	flush := func() {
		if currentPath == "" {
			return
		}
		files[currentPath] = strings.TrimSpace(strings.Join(bodyLines, "\n"))
		bodyLines = nil
	}

	for _, line := range lines {
		if m := pathHeaderRe.FindStringSubmatch(line); len(m) == 2 {
			flush()
			currentPath = m[1]
			continue
		}
		if currentPath != "" {
			bodyLines = append(bodyLines, line)
		}
	}
	flush()

	if len(files) <= 1 {
		return nil
	}
	return files
}

func splitTestCompanion(code string) (main string, test string, ok bool) {
	lines := strings.Split(code, "\n")
	for i, line := range lines {
		trim := strings.TrimSpace(line)
		if strings.EqualFold(trim, "// main_test.go") ||
			strings.HasPrefix(strings.ToLower(trim), "// file: main_test.go") {
			mainPart := strings.TrimSpace(strings.Join(lines[:i], "\n"))
			testPart := strings.TrimSpace(strings.Join(lines[i+1:], "\n"))
			if mainPart != "" && strings.Contains(testPart, "func Test") {
				mainPart = stripLeadingFileComment(mainPart)
				return mainPart, testPart, true
			}
		}
	}
	// package main ... func Test in same blob without marker
	if idx := strings.Index(code, "\npackage main\n\nimport \"testing\""); idx > 0 {
		mainPart := strings.TrimSpace(code[:idx])
		testPart := strings.TrimSpace(code[idx+1:])
		mainPart = stripLeadingFileComment(mainPart)
		return mainPart, testPart, strings.Contains(testPart, "func Test")
	}
	return "", "", false
}

func splitPathHeader(part string) (path string, body string) {
	lines := strings.Split(part, "\n")
	if len(lines) == 0 {
		return "", part
	}
	if m := pathHeaderRe.FindStringSubmatch(lines[0]); len(m) == 2 {
		return m[1], strings.TrimSpace(strings.Join(lines[1:], "\n"))
	}
	return "", part
}

func defaultFileName(part string, index int) string {
	if strings.Contains(part, "func Test") || strings.Contains(part, "func Benchmark") {
		return "main_test.go"
	}
	if index == 0 {
		return "main.go"
	}
	return fmt.Sprintf("file_%d.go", index+1)
}

func stripLeadingFileComment(code string) string {
	lines := strings.Split(code, "\n")
	for len(lines) > 0 && pathHeaderRe.MatchString(lines[0]) {
		lines = lines[1:]
	}
	return strings.TrimSpace(strings.Join(lines, "\n"))
}
