# Transform Python Skill Builder to TDD Training Camp

## Overview
Refactor the Python Skill Builder application from a traditional code submission model to a **Test-Driven Development (TDD) training platform** that explicitly teaches the Red-Green-Refactor methodology. This transformation will make testing a first-class learning objective and provide learners with deep insights into test design and mock data management.

## Problem Statement
The current application:
- Treats tests as invisible backend validation
- Doesn't teach test-first thinking
- Provides minimal insight into test structure and mock data
- Doesn't help learners understand edge cases through strategic test data
- Missing progression through the three TDD phases: RED → GREEN → REFACTOR

## Solution Overview
Transform the workshop experience into an explicit TDD training environment where:
1. **RED Phase**: Tests are visible and failing before code is written
2. **GREEN Phase**: Learners write minimal code to pass tests
3. **REFACTOR Phase**: Code quality improvements happen with test safety nets

Key additions:
- Interactive test suite display with expandable assertion details
- Mock data management system with multiple test scenarios
- Code metrics and refactor guidance
- Phase-specific UI context and learning objectives

## Detailed Requirements

### Phase 1: Core TDD Mechanics (MVP)

#### 1.1 Test Suite Visibility Component
- [ ] Create `TestPanelComponent` to display test cases in left sidebar
- [ ] Show test status (pass/fail) with visual indicators
- [ ] Display mock data preview for each test (inputs → expected output)
- [ ] Implement expandable test details showing:
  - Full assertion statement
  - Actual vs expected values
  - Error message (if failed)
  - Mock data used
- [ ] Add test progress bar: `X of Y tests passing`

**Files to create:**
- `components/test-panel/test-case.js` - Individual test card component
- `components/test-panel/test-progress.js` - Progress visualization
- `components/test-panel/assertion-display.js` - Detailed assertion viewer

#### 1.2 Phase Indicator & Navigation
- [ ] Create phase selector buttons: RED → GREEN → REFACTOR
- [ ] Update UI context based on current phase:
  - **RED**: Show all tests failing, hide metrics, show "Analyze tests first"
  - **GREEN**: Show test progress, highlight passing tests
  - **REFACTOR**: Show code metrics, suggest improvements
- [ ] Update guidance text in footer based on phase
- [ ] Disable submission until RED tests are analyzed (optional strict mode)

**Files to create:**
- `components/phase-indicator/phase-display.js`
- `logic/tdd-phases.js` - Phase state management

#### 1.3 Test Execution Engine
- [ ] Build `TestRunnerService` to safely execute user code
- [ ] Parse test results into structured format:
  ```javascript
  {
    testId: "test_1",
    name: "test_add_positive_numbers",
    status: "pass|fail",
    mocks: { inputs: [2, 3], expected: 5 },
    actual: 5,
    assertion: "assertEqual(result, expected)",
    error: null|"Error message"
  }
  ```
- [ ] Implement assertion parsing for common patterns:
  - `assertEqual(a, b)`
  - `assertNotEqual(a, b)`
  - `assertTrue(condition)`
  - `assertRaises(ExceptionType)`
  - `assertAlmostEqual(a, b, places=n)`

**Files to create:**
- `services/test-runner.js` - Test execution
- `services/assertion-parser.js` - Assertion extraction and display

#### 1.4 Workshop Data Structure Enhancement
- [ ] Extend workshop schema to include test suite data:
  ```javascript
  {
    id: "workshop_1",
    title: "Build an Add Function",
    description: "...",
    testSuite: {
      phase: "red",
      tests: [
        {
          id: "test_1",
          name: "test_add_positive_numbers",
          assertion: "assertEqual(add(2, 3), 5)",
          mocks: {
            inputs: [2, 3],
            expected: 5
          }
        },
        // ... more tests
      ]
    },
    phases: {
      red: {
        guidance: "Analyze the failing tests...",
        hints: ["Read each test carefully", "Understand the mock data"]
      },
      green: {
        guidance: "Make all tests pass...",
        hints: ["Start with the simplest test"]
      },
      refactor: {
        guidance: "Improve code quality...",
        codeMetrics: { targetComplexity: 2 }
      }
    }
  }
  ```

**Files to update:**
- `services/modules.js` - Add test suite loading
- `config.js` - Add test suite configuration constants

---

### Phase 2: Mock Data Management System

#### 2.1 Mock Data Panel UI
- [ ] Create mock data selector in right sidebar
- [ ] Display multiple mock sets:
  - **Valid Inputs**: Basic happy path data
  - **Edge Cases**: Zero, negative, boundary values
  - **Stress Test**: Large numbers, performance scenarios
  - **Custom**: User-created test data
- [ ] Show mock data preview with syntax highlighting
- [ ] Add toggle to switch mock sets and re-run tests

**Files to create:**
- `components/mock-data-panel/mock-selector.js`
- `components/mock-data-panel/mock-preview.js`

#### 2.2 Mock Data Service
- [ ] Build `MockDataService` to manage test data sets
- [ ] Support per-workshop mock definitions:
  ```javascript
  mockSets: {
    valid: {
      name: "Valid Inputs",
      description: "Basic positive numbers",
      tests: { test_1: { inputs: [2, 3], expected: 5 }, ... }
    },
    edge: {
      name: "Edge Cases",
      description: "Zero, negatives, floats",
      tests: { test_1: { inputs: [0, 5], expected: 5 }, ... }
    }
  }
  ```
- [ ] Implement mock history tracking
- [ ] Support custom mock creation UI

**Files to create:**
- `services/mock-manager.js`

#### 2.3 Mock Data Editor (Stretch)
- [ ] Create inline mock data editor
- [ ] Allow modifying mock inputs and expected outputs
- [ ] Add data generation helpers (random arrays, edge values)
- [ ] Save custom mock sets to progress state
- [ ] Show "test with custom data" button

**Files to create:**
- `components/mock-data-panel/mock-editor.js`

---

### Phase 3: Code Metrics & Refactor Guidance

#### 3.1 Code Metrics Display
- [ ] Calculate and display when in REFACTOR phase:
  - **Cyclomatic Complexity**: Measure code branches
  - **Test Coverage %**: Lines covered by tests
  - **Lines of Code**: Indicator of solution complexity
  - **Code Duplication**: Detect repeated patterns
- [ ] Show as visual progress bars with target ranges
- [ ] Only visible in REFACTOR phase

**Files to create:**
- `services/code-metrics.js`
- `components/refactor-guide/code-metrics.js`

#### 3.2 Refactor Suggestions
- [ ] Generate mentor refactoring solutions
- [ ] Show side-by-side comparison: User code vs mentor code
- [ ] Highlight improvements (simplification, readability, performance)
- [ ] Include explanatory comments

**Files to create:**
- `components/refactor-guide/refactor-suggestions.js`
- `services/refactor-analyzer.js` (stretch)

---

### Phase 4: Enhanced Feedback & Learning Flow

#### 4.1 Assertion-by-Assertion Feedback
- [ ] When test fails, display:
  ```
  ❌ test_add_negative_numbers
  Assertion: assertEqual(add(-1, -2), -3)
  Expected: -3
  Got: None
  
  Mock Data Used:
  inputs: [-1, -2]
  ```
- [ ] Highlight specific mismatch points
- [ ] Suggest what's wrong (missing implementation, logic error)

#### 4.2 Hints System (Phase-Aware)
- [ ] **RED phase hints**: "Read the test names carefully", "What is the mock data?"
- [ ] **GREEN phase hints**: Progressive hint reveals (Hint 1 → Hint 2 → Hint 3)
- [ ] **REFACTOR phase hints**: "Can you reduce complexity?", "Any code duplication?"

**Files to update:**
- `logic/hints.js` - Extend with phase-awareness

#### 4.3 Achievement Badges & Milestones
- [ ] Add TDD-specific achievements:
  - 🔴 "Red Phase Master" - Analyzed 10 test suites
  - 🟢 "Green Achiever" - Passed 50 tests
  - 🔵 "Refactor Wizard" - Improved 5 code snippets
  - 🎯 "Test Coverage Champion" - 95%+ coverage achieved
- [ ] Track metrics in progress state
- [ ] Display in dashboard module cards

---

## Data Structure Changes

### Workshop Schema (New)
```javascript
{
  id: "workshop_add_function",
  title: "Build an Add Function",
  description: "Learn TDD by implementing a simple addition function",
  
  // Current fields (preserved)
  estimatedMinutes: 15,
  
  // NEW: Test suite definition
  testSuite: {
    tests: [
      {
        id: "test_1",
        name: "test_add_positive_numbers",
        description: "Test adding two positive numbers",
        assertion: "assertEqual(add(2, 3), 5)",
        mocks: {
          inputs: [2, 3],
          expected: 5
        }
      },
      // ... 4 more tests
    ],
    
    mockSets: {
      valid: {
        name: "Valid Inputs",
        description: "Basic positive numbers",
        dataPoints: 3,
        testData: { /* ... */ }
      },
      edge: {
        name: "Edge Cases",
        description: "Zero, negatives, boundary values",
        dataPoints: 5,
        testData: { /* ... */ }
      },
      stress: {
        name: "Stress Test",
        description: "Large numbers, performance scenarios",
        dataPoints: 2,
        testData: { /* ... */ }
      }
    }
  },
  
  // NEW: Phase-specific guidance
  phases: {
    red: {
      guidance: "Analyze the failing tests and understand requirements",
      objective: "What does each test expect?",
      hints: [
        "Read the test names carefully",
        "Check the mock data inputs",
        "Look at the expected outputs"
      ]
    },
    green: {
      guidance: "Write minimal code to make all tests pass",
      objective: "Get all tests green",
      hints: [
        "Start with the simplest test",
        "Implement just enough logic",
        "Don't over-engineer"
      ]
    },
    refactor: {
      guidance: "Improve code quality while keeping tests green",
      objective: "Reduce complexity, improve readability",
      codeMetrics: {
        targetComplexity: 2,
        targetCoverage: 100
      },
      hints: [
        "All tests still pass?",
        "Can you simplify the logic?",
        "Any repeated code?"
      ]
    }
  }
}
```

### Progress State (Enhanced)
```javascript
{
  moduleId: {
    completed: 0,
    scores: { workshopId: 85 },
    lastSeenAt: "2024-01-15T10:30:00Z",
    
    // NEW: Test and mock tracking
    testProgress: {
      workshopId: {
        testsRun: [
          { testId: "test_1", status: "pass", timestamp: "..." },
          { testId: "test_2", status: "fail", timestamp: "..." }
        ],
        phase: "green",
        mockSetUsed: "valid"
      }
    },
    
    // NEW: Achievements
    achievements: [
      "red_phase_master",
      "green_achiever"
    ]
  }
}
```

---

## UI Component Hierarchy

```
TDDWorkshopContainer
├── Header
│   ├── PhaseIndicator (RED / GREEN / REFACTOR)
│   └── WorkshopTitle + Navigation
├── MainContent (3-panel layout)
│   ├── LeftPanel: TestPanelComponent
│   │   ├── TestProgressBar
│   │   └── TestList
│   │       └── TestCase (expandable)
│   │           ├── AssertionDisplay
│   │           └── MockDataPreview
│   ├── CenterPanel: CodeEditor
│   │   ├── Editor (textarea)
│   │   └── EditorFooter (Run/Reset buttons)
│   └── RightPanel: Toolbox
│       ├── MockDataSelector
│       ├── MockDataPreview
│       ├── CodeMetrics (REFACTOR phase only)
│       ├── RefactorGuide (REFACTOR phase only)
│       └── HintsPanel (phase-aware)
└── Footer
    └── PhaseGuidance + Navigation
```

---

## Implementation Roadmap

### Milestone 1: RED Phase Core (Week 1)
- [ ] Test suite component with visual display
- [ ] Phase indicator and context switching
- [ ] Basic test runner service
- [ ] Workshop schema with test data

### Milestone 2: GREEN Phase & Execution (Week 2)
- [ ] Test execution engine
- [ ] Real test pass/fail display
- [ ] Assertion-by-assertion feedback
- [ ] Code editor integration

### Milestone 3: REFACTOR Phase & Metrics (Week 3)
- [ ] Code metrics calculation
- [ ] Refactor guidance display
- [ ] Phase-aware hints system
- [ ] Mentor solutions (optional)

### Milestone 4: Mock Data System (Week 4)
- [ ] Mock data selector UI
- [ ] Multiple mock set management
- [ ] Mock data preview and editing
- [ ] Custom mock creation

### Milestone 5: Polish & Launch (Week 5)
- [ ] Achievement system
- [ ] Performance optimization
- [ ] Sample workshop content (10-15 workshops)
- [ ] Documentation and tutorials

---

## Testing Requirements

- [ ] Unit tests for `TestRunnerService`
- [ ] Unit tests for `AssertionParser`
- [ ] Unit tests for `MockDataService`
- [ ] Integration tests for phase transitions
- [ ] E2E tests for complete RED-GREEN-REFACTOR workflow
- [ ] Mock data validation tests

---

## Success Criteria

1. ✅ Tests are visible and understandable before code is written (RED phase)
2. ✅ Learners can see which tests pass/fail with clear feedback
3. ✅ Mock data is transparent and inspectable
4. ✅ Refactor phase helps learners improve code quality
5. ✅ At least 80% of learners complete all three phases per workshop
6. ✅ Learning analytics show improvement in test coverage understanding
7. ✅ Completion time per workshop is reasonable (<20 min average)

---

## Design Resources

- [Figma: TDD Workshop UI Mockup](link-here)
- [UI Components Demo](link-to-interactive-demo)
- [Sample Workshop Data](link-to-sample-json)

---

## Related Issues
- #123 - Refactor progress state management
- #124 - Enhance code execution sandbox
- #125 - Update workshop content format

---

## Notes for Reviewers

- This is a **substantial transformation**—consider breaking into smaller PRs by milestone
- **Backward compatibility**: Existing workshops should still work; TDD features are opt-in per workshop
- **API changes**: Workshop schema updated but migrations handled gracefully
- **Performance**: Test execution needs to be fast (<500ms) for good UX
- **Security**: Code execution must be sandboxed safely

---

## Acceptance Checklist
- [ ] All Phase 1 requirements implemented and tested
- [ ] UI matches approved mockups
- [ ] Sample workshops demonstrate all three phases
- [ ] Documentation updated with TDD pedagogy
- [ ] Performance benchmarks met (<500ms test execution)
- [ ] Accessibility review passed (WCAG AA)
- [ ] Team review and approval