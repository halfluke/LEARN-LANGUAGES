package main

import (
	"fmt"
	"os"
	"strings"

	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
)

// Lipgloss styles
var (
	headerStyle     = lipgloss.NewStyle().Bold(true).Foreground(lipgloss.Color("86")).PaddingBottom(1)
	cursorStyle     = lipgloss.NewStyle().Foreground(lipgloss.Color("227")).Bold(true)
	dimStyle        = lipgloss.NewStyle().Foreground(lipgloss.Color("240"))
	keyStyle        = lipgloss.NewStyle().Foreground(lipgloss.Color("245")).Italic(true)
	successStyle    = lipgloss.NewStyle().Foreground(lipgloss.Color("82")).Bold(true)
	errorStyle      = lipgloss.NewStyle().Foreground(lipgloss.Color("203")).Bold(true)
	hintStyle       = lipgloss.NewStyle().Foreground(lipgloss.Color("69"))
	codeStyle       = lipgloss.NewStyle().Foreground(lipgloss.Color("228")).Background(lipgloss.Color("235"))
	chapterNumStyle = lipgloss.NewStyle().Foreground(lipgloss.Color("75")).Bold(true)
)

// ResultMsg is sent when code execution completes
type ResultMsg struct {
	execRes   *ExecutionResult
	err       error
	hintsUsed int
}

// EditorResultMsg is sent when the editor closes
type EditorResultMsg struct {
	Code string
	Err  error
}

// LaunchEditorCmd launches the user's editor and returns the edited code
func LaunchEditorCmd(initialCode string) tea.Cmd {
	return func() tea.Msg {
		editor, err := NewEditor()
		if err != nil {
			return EditorResultMsg{Code: initialCode, Err: err}
		}
		code, err := editor.LaunchEditor(initialCode)
		if err != nil {
			return EditorResultMsg{Code: initialCode, Err: err}
		}
		return EditorResultMsg{Code: code, Err: nil}
	}
}

// runCmd executes the current code asynchronously and returns a Cmd
func runCmd(m *Model) tea.Cmd {
	return func() tea.Msg {
		execRes, execErr := m.executor.ExecuteCode(m.currentCode)
		return ResultMsg{
			execRes:   execRes,
			err:       execErr,
			hintsUsed: m.hintsUsed,
		}
	}
}

// Model is the main application model
type Model struct {
	// Current view: "list", "theory", "exercise_list", "editor", "result", "jump"
	view string

	// For chapter list navigation
	chapters []Chapter
	cursor   int

	// For theory view
	theoryScroll int

	// For exercise view
	selectedChapter  *Chapter
	selectedExercise *Exercise
	exerciseCursor   int
	hintsUsed        int
	executionResult  *ExecutionResult
	validationResult *ValidationResult
	currentCode      string

	// Services
	executor  *Executor
	validator *Validator
	progress  *ProgressStore
}

// newModel creates the initial model state
func newModel() Model {
	loader := NewChapterLoader(GetDefaultChaptersDir())
	chapters, err := loader.LoadChapters()
	if err != nil {
		chapters = []Chapter{}
	}

	progress := NewProgressStore()
	if err := progress.Load(); err != nil {
		fmt.Fprintf(os.Stderr, "Warning: could not load progress: %v\n", err)
	}

	return Model{
		view:           "list",
		chapters:       chapters,
		cursor:         0,
		executor:       NewExecutor(),
		validator:      NewValidator(),
		progress:       progress,
		exerciseCursor: 0,
		hintsUsed:      0,
	}
}

// Init implements tea.Model
func (m Model) Init() tea.Cmd {
	return nil
}

// updateView handles internal navigation state changes
func (m *Model) updateView(view string) {
	m.view = view
}

// handleResult processes a ResultMsg and updates the model
func (m *Model) handleResult(msg ResultMsg) {
	if msg.err != nil {
		m.validationResult = &ValidationResult{
			Passed:  false,
			Message: "Execution error: " + msg.err.Error(),
		}
		m.view = "result"
		return
	}

	m.executionResult = msg.execRes
	m.validationResult = m.validator.Validate(msg.execRes, m.selectedExercise, msg.hintsUsed)
	m.view = "result"

	if m.validationResult.Passed && m.progress != nil {
		m.progress.SaveProgress(
			m.selectedChapter.ID,
			m.selectedExercise.ID,
			true,
			1,
			msg.hintsUsed,
		)
		if err := m.progress.Save(); err != nil {
			fmt.Fprintf(os.Stderr, "Warning: could not save progress: %v\n", err)
		}
	}
}

// Update implements tea.Model
func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case ResultMsg:
		m.handleResult(msg)
		return m, nil

	case EditorResultMsg:
		if msg.Err != nil {
			m.validationResult = &ValidationResult{
				Passed:  false,
				Message: "Editor error: " + msg.Err.Error(),
			}
		} else {
			m.currentCode = msg.Code
		}
		m.view = "editor"
		return m, nil

	case tea.KeyMsg:
		return m.handleKey(msg)
	}

	return m, nil
}

// handleKey dispatches key events to the correct view handler
func (m Model) handleKey(key tea.KeyMsg) (tea.Model, tea.Cmd) {
	switch key.String() {
	case "ctrl+c", "q":
		return m, tea.Quit
	case "s":
		if m.view == "list" || m.view == "stats" {
			m.view = "stats"
		}
		return m, nil
	case "?":
		if m.view == "list" || m.view == "help" {
			m.view = "help"
		}
		return m, nil
	}

	switch m.view {
	case "list":
		return m.handleListView(key)
	case "theory":
		return m.handleTheoryView(key)
	case "jump":
		return m.handleJumpView(key)
	case "exercise_list":
		return m.handleExerciseListView(key)
	case "editor", "result":
		return m.handleEditorView(key)
	case "stats":
		return m.handleStatsView(key)
	case "help":
		return m.handleHelpView(key)
	}

	return m, nil
}

func (m Model) handleListView(key tea.KeyMsg) (tea.Model, tea.Cmd) {
	switch key.String() {
	case "/":
		m.view = "jump"
	case "up", "k":
		if m.cursor > 0 {
			m.cursor--
		}
	case "down", "j":
		if m.cursor < len(m.chapters)-1 {
			m.cursor++
		}
	case "enter":
		m.selectedChapter = &m.chapters[m.cursor]
		m.theoryScroll = 0
		m.view = "theory"
	}
	return m, nil
}

func (m Model) handleJumpView(key tea.KeyMsg) (tea.Model, tea.Cmd) {
	switch key.String() {
	case "up", "k", "esc", "backspace", "b":
		m.view = "list"
	case "1", "2", "3", "4", "5", "6", "7", "8", "9":
		idx := int(key.String()[0] - '1')
		if idx < len(m.chapters) {
			m.selectedChapter = &m.chapters[idx]
			m.theoryScroll = 0
			m.view = "theory"
		}
	case "0":
		if len(m.chapters) >= 10 {
			m.selectedChapter = &m.chapters[9]
			m.theoryScroll = 0
			m.view = "theory"
			m.exerciseCursor = 0
		}
	default:
		m.view = "list"
	}
	return m, nil
}

func (m Model) handleExerciseListView(key tea.KeyMsg) (tea.Model, tea.Cmd) {
	switch key.String() {
	case "up", "k":
		if m.exerciseCursor > 0 {
			m.exerciseCursor--
		}
	case "down", "j":
		if m.exerciseCursor < len(m.selectedChapter.Exercises)-1 {
			m.exerciseCursor++
		}
	case "enter":
		m.selectedExercise = &m.selectedChapter.Exercises[m.exerciseCursor]
		m.currentCode = m.selectedExercise.StarterCode
		m.hintsUsed = 0
		m.view = "editor"
	case "esc", "backspace", "b":
		m.view = "list"
		m.selectedChapter = nil
		m.selectedExercise = nil
		m.exerciseCursor = 0
	}
	return m, nil
}

func (m Model) handleEditorView(key tea.KeyMsg) (tea.Model, tea.Cmd) {
	switch key.String() {
	case "up", "k", "down", "j":
		// No-op in editor view
	case "r":
		return m, runCmd(&m)
	case "e":
		if m.selectedExercise != nil {
			return m, LaunchEditorCmd(m.currentCode)
		}
	case "h":
		if m.view == "result" && !m.validationResult.Passed {
			m.hintsUsed++
			return m, runCmd(&m)
		}
	case "esc", "backspace", "b":
		m.view = "list"
		m.selectedChapter = nil
		m.selectedExercise = nil
		m.exerciseCursor = 0
	}
	return m, nil
}

// theoryScrollMax returns the maximum scrollable rows for theory content
func theoryScrollMax(m Model) int {
	if m.selectedChapter == nil {
		return 0
	}
	lines := strings.Split(m.selectedChapter.Theory, "\n")
	termHeight := 24 // approximate terminal height for scroll bound
	if len(lines) <= termHeight {
		return 0
	}
	return len(lines) - termHeight + 4
}

func (m Model) handleTheoryView(key tea.KeyMsg) (tea.Model, tea.Cmd) {
	switch key.String() {
	case "up", "k":
		if m.theoryScroll > 0 {
			m.theoryScroll--
		}
	case "down", "j":
		if m.theoryScroll < theoryScrollMax(m) {
			m.theoryScroll++
		}
	case "enter":
		m.view = "exercise_list"
		m.exerciseCursor = 0
	case "esc", "backspace", "b":
		m.view = "list"
	}
	return m, nil
}

func (m Model) handleStatsView(key tea.KeyMsg) (tea.Model, tea.Cmd) {
	switch key.String() {
	case "esc", "backspace", "b", "q":
		m.view = "list"
	}
	return m, nil
}

func (m Model) handleHelpView(key tea.KeyMsg) (tea.Model, tea.Cmd) {
	switch key.String() {
	case "esc", "backspace", "b", "q":
		m.view = "list"
	}
	return m, nil
}

// View renders the current state
func (m Model) View() string {
	switch m.view {
	case "list":
		return m.renderChapterList()
	case "jump":
		return m.renderJumpList()
	case "theory":
		return m.renderTheoryView()
	case "exercise_list":
		return m.renderExerciseList()
	case "editor", "result":
		return m.renderExerciseView()
	case "stats":
		return m.renderStatsView()
	case "help":
		return m.renderHelpView()
	default:
		return "Unknown view"
	}
}

func (m Model) renderTheoryView() string {
	if m.selectedChapter == nil {
		return "No chapter selected"
	}

	s := headerStyle.Render(m.selectedChapter.Title + " - Theory") + "\n\n"

	lines := strings.Split(m.selectedChapter.Theory, "\n")
	visibleLines := 20
	start := m.theoryScroll
	if start+visibleLines > len(lines) {
		start = len(lines) - visibleLines
		if start < 0 {
			start = 0
		}
	}
	end := start + visibleLines
	if end > len(lines) {
		end = len(lines)
	}

	for _, line := range lines[start:end] {
		s += line + "\n"
	}

	if m.theoryScroll > 0 {
		s += dimStyle.Render("(scroll up for more)") + "\n"
	}
	if end < len(lines) {
		s += dimStyle.Render("(scroll down for more)") + "\n"
	}

	s += "\n" + keyStyle.Render("↑/↓ Scroll  •  Enter Continue  •  ← Back  •  q Quit")
	return s
}

func (m Model) renderJumpList() string {
	s := headerStyle.Render("Jump to Chapter") + "\n\n"

	for i, chapter := range m.chapters {
		num := i + 1
		if num > 9 {
			num = 0
		}
		s += chapterNumStyle.Render(fmt.Sprintf("[%d] ", num)) + chapter.Title + "\n"
		s += dimStyle.Render(fmt.Sprintf("   %s (%d exercises)", chapter.Description, chapter.ExerciseCount)) + "\n\n"
	}

	s += "\n" + keyStyle.Render("1-9,0 Select  •  / Jump menu  •  ← Back  •  q Quit")
	return s
}

func (m Model) renderChapterList() string {
	s := headerStyle.Render("Learn Go - Select a Chapter") + "\n\n"

	for i, chapter := range m.chapters {
		prefix := "  "
		if m.cursor == i {
			prefix = cursorStyle.Render("▶ ")
		}
		chapterNumStyle := lipgloss.NewStyle().Foreground(lipgloss.Color("75")).Bold(true)
		s += prefix + chapterNumStyle.Render(fmt.Sprintf("[%d] ", i+1)) + chapter.Title + "\n"

		exerciseInfo := fmt.Sprintf("   %s (%d exercises)", chapter.Description, chapter.ExerciseCount)
		if m.progress != nil && chapter.ExerciseCount > 0 {
			completed := len(m.progress.GetCompletedExercises(chapter.ID))
			pct := int(float64(completed) / float64(chapter.ExerciseCount) * 100)
			exerciseInfo += fmt.Sprintf(" (%d%% done)", pct)
		}
		s += dimStyle.Render(exerciseInfo) + "\n\n"
	}

	s += "\n" + keyStyle.Render("↑/↓ Navigate  •  Enter Select  •  / Jump  •  q Quit  •  s Stats  •  ? Help")
	return s
}

func (m Model) renderExerciseList() string {
	if m.selectedChapter == nil {
		return "No chapter selected"
	}

	s := headerStyle.Render(m.selectedChapter.Title+" - Exercises") + "\n\n"

	for i, ex := range m.selectedChapter.Exercises {
		prefix := "  "
		if m.exerciseCursor == i {
			prefix = cursorStyle.Render("▶ ")
		}
		s += prefix + ex.Title + "\n"
		s += dimStyle.Render(fmt.Sprintf("   %s", ex.Description)) + "\n\n"
	}

	s += "\n" + keyStyle.Render("↑/↓ Navigate  •  Enter Start  •  ← Back  •  q Quit")
	return s
}

func (m Model) renderExerciseView() string {
	if m.selectedExercise == nil {
		return "No exercise selected"
	}

	s := headerStyle.Render(m.selectedExercise.Title) + "\n\n"
	s += m.selectedExercise.Description + "\n\n"

	s += dimStyle.Render("--- Your Code ---") + "\n"
	s += codeStyle.Render(m.currentCode) + "\n"
	s += dimStyle.Render("-----------------") + "\n\n"

	if m.view == "result" && m.validationResult != nil {
		if m.validationResult.Passed {
			s += successStyle.Render("✓ "+m.validationResult.Message) + "\n\n"
		} else {
			s += errorStyle.Render(m.validationResult.Message) + "\n\n"
		}
		if m.validationResult.ShowSolution {
			s += "\n" + hintStyle.Render("--- Solution ---") + "\n"
			s += m.selectedExercise.Solution + "\n"
		}
	} else {
		s += keyStyle.Render("e Open editor  •  r Run  •  h Hint  •  ← Back  •  q Quit")
	}

	return s
}

func (m Model) renderStatsView() string {
	s := headerStyle.Render("Stats Dashboard") + "\n\n"

	var totalExercises, completedExercises int
	var totalHints int

	for _, chapter := range m.chapters {
		totalExercises += chapter.ExerciseCount
		if m.progress != nil {
			completed := m.progress.GetCompletedExercises(chapter.ID)
			completedExercises += len(completed)
			for _, p := range m.progress.progress {
				if p.ChapterID == chapter.ID && p.Completed {
					totalHints += p.HintsUsed
				}
			}
		}
	}

	pct := 0.0
	if totalExercises > 0 {
		pct = float64(completedExercises) / float64(totalExercises) * 100
	}

	s += dimStyle.Render(fmt.Sprintf("Total Exercises:  %d", totalExercises)) + "\n"
	s += dimStyle.Render(fmt.Sprintf("Completed:        %d", completedExercises)) + "\n"
	s += dimStyle.Render(fmt.Sprintf("Completion:       %.0f%%", pct)) + "\n"
	s += dimStyle.Render(fmt.Sprintf("Hints Used:       %d", totalHints)) + "\n\n"

	s += keyStyle.Render("← Back  •  q Quit")
	return s
}

func (m Model) renderHelpView() string {
	s := headerStyle.Render("Keyboard Shortcuts") + "\n\n"

	type shortcut struct {
		key, desc string
	}

	shortcuts := []shortcut{
		{"q", "Quit application"},
		{"↑/↓ or k/j", "Navigate up/down"},
		{"Enter", "Select (chapter or exercise)"},
		{"Esc, Backspace, or b", "Go back to previous view"},
		{"/", "Jump to chapter by number"},
		{"s", "Show stats dashboard"},
		{"?", "Show this help screen"},
		{"e", "Open editor for exercise"},
		{"r", "Run current code"},
		{"h", "Show hint (in editor on failed exercise)"},
	}

	for _, sc := range shortcuts {
		s += keyStyle.Render(sc.key) + "\t" + dimStyle.Render(sc.desc) + "\n"
	}

	s += "\n" + keyStyle.Render("← Back  •  q Quit")
	return s
}
