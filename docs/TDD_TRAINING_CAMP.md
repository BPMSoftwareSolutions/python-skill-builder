# TDD Training Camp: Brainstorm & Strategy

## Core Transformation Vision
Convert Python skill builder → TDD-focused training platform following **Red → Green → Refactor** pedagogy with integrated mock data, test assertions, and explicit test-first workflow.

---

## 1. CURRICULUM STRUCTURE

### Current State
- Linear module/workshop progression
- Single code submission with feedback

### TDD Transformation
- **Test-First Modules**: Each workshop starts with visible test cases (RED phase)
- **Incremental Requirements**: Tests reveal features progressively
- **Multiple Test Suites**: Unit tests, integration tests, edge cases
- **Test Coverage Tracking**: Visual progress on test success rate

**Example Workshop Flow:**
```
1. See 5 failing tests (RED)
   ├─ Test: test_add_positive_numbers()
   ├─ Test: test_add_negative_numbers()
   ├─ Test: test_add_zero()
   ├─ Test: test_add_large_numbers()
   └─ Test: test_add_string_error_handling()

2. Write minimal code to pass (GREEN)

3. Refactor for quality (REFACTOR)
   └─ Run tests to ensure no regression
```

---

## 2. TEST VISIBILITY & INTERACTION

### Key Feature: Test-Driven UI
- **Left Panel**: Test cases (pass/fail indicators)
- **Center Panel**: Code editor (standard)
- **Right Panel**: Test output & coverage metrics

### Test Display Options
- **Show Tests Before Coding**: Force test-first thinking
- **Progressive Test Reveals**: Unlock tests as requirements are met
- **Side-by-side Test/Output**: Real-time assertion feedback
- **Test Dependency Chain**: Pass Test 1 → unlock Test 2

### Mock Data Panel
- Inspect input data for each test
- Edit mock data to create edge cases
- Save custom test scenarios

---

## 3. MOCK DATA MANAGEMENT SYSTEM

### Mock Data Architecture
```
workshop/
├── tests.json (5-10 test cases per workshop)
├── mocks/
│   ├── valid_inputs.json
│   ├── edge_cases.json
│   ├── invalid_inputs.json
│   └── performance_data.json
└── assertions/
    ├── output_expectations.json
    └── performance_thresholds.json
```

### Interactive Mock Data Editing
- **Toggle Mock Sets**: "Basic" → "Edge Cases" → "Stress Test"
- **Custom Mock Creation**: User generates test data
- **Mock History**: Track which mocks they've tested
- **Mutation Testing**: Randomly flip boolean/number values in mocks

### Example Mock Management UI
```
Mock Data Set Selector:
┌─────────────────────────────────┐
│ Current: "Valid Inputs" (3/5)  │
├─────────────────────────────────┤
│ □ Valid Inputs                  │
│ ☑ Edge Cases                    │
│ □ Invalid Inputs                │
│ □ Performance Data              │
│ + Create Custom Mock Set        │
└─────────────────────────────────┘
```

---

## 4. RED-GREEN-REFACTOR PHASES AS FEATURES

### Phase Tracking & Guidance
Each workshop explicitly shows which phase user is in:

**RED Phase:**
- Show all failing tests upfront
- "Goal: Make tests pass (GREEN)"
- Tests are read-only
- Mock data is visible

**GREEN Phase:**
- User writes code
- Tests run continuously (or on-demand)
- Progress bar: "X of Y tests passing"
- Achievement: "First test passed!" 🎉

**REFACTOR Phase:**
- Lock in test requirements
- Show code quality metrics:
  - Cyclomatic complexity
  - Code duplication
  - Test coverage %
- "Can you improve this without breaking tests?"
- Optional: Show "mentor refactoring" as comparison

---

## 5. ASSERTION VISUALIZATION

### Explicit Assertion Display
Instead of generic "failed/passed", show:

```
✅ test_add_positive_numbers
   Expected: 5
   Got: 5
   
❌ test_add_negative_numbers
   Expected: -3
   Got: 0  ← MISMATCH HERE
   
⏸️  test_add_string_error_handling
   Expected: ValueError raised
   Got: Function returned normally
```

### Assertion Types as Learning Tools
- **Equality**: `assert result == expected`
- **Truthiness**: `assert condition is True`
- **Exceptions**: `assert ValueError raised`
- **Performance**: `assert execution_time < 1ms`
- **Side Effects**: `assert database.records == 2`

---

## 6. MOCK DATA-DRIVEN LEARNING

### Scenarios & Contexts
```
Workshop: "Sort Algorithm"

📊 Scenario: Small Lists
   Mock: [3, 1, 4, 1, 5]
   
🚀 Scenario: Large Lists (1M items)
   Mock: generated_random_list(1_000_000)
   
🛡️ Scenario: Edge Cases
   Mock: [], [1], duplicates, negatives, floats
   
💪 Scenario: Performance Challenge
   Mock: Sorted vs reverse sorted vs random
```

---

## 7. PROGRESS & ACHIEVEMENTS

### TDD-Specific Metrics
- **Test Coverage**: % of code covered by tests
- **Refactor Attempts**: How many times they improved code
- **Mock Scenarios Tested**: Breadth of testing
- **Test-First Ratio**: % of time tests written before code

### Badges & Milestones
- 🔴 "Red Phase Master" - Analyzed 20 test suites
- 🟢 "Green Achiever" - Passed 100 tests
- 🔵 "Refactor Wizard" - Improved 10 pieces of code
- 🎯 "Test Coverage Champion" - 95%+ coverage

---

## 8. CODE STRUCTURE CHANGES

### New Components Needed
```
components/
├── tests-panel/          (NEW)
│   ├── test-case.js
│   ├── assertion-display.js
│   └── test-progress.js
├── mock-data-panel/      (NEW)
│   ├── mock-selector.js
│   ├── mock-editor.js
│   └── mock-history.js
├── refactor-guide/       (NEW)
│   ├── code-metrics.js
│   └── refactor-suggestions.js
└── phase-indicator/      (NEW)
    └── phase-display.js

services/
├── test-runner.js        (NEW - execute tests)
├── mock-manager.js       (NEW - manage test data)
├── assertion-parser.js   (NEW - parse & display)
└── coverage-analyzer.js  (NEW - measure coverage)

logic/
├── tdd-phases.js         (NEW - RED/GREEN/REFACTOR)
└── test-progression.js   (NEW - unlock tests)
```

### Data Structure Evolution
```javascript
// Old: Single code submission
workshop = {
  id, title, prompt, starterCode, timeLimitMinutes
}

// New: TDD-focused with tests & mocks
workshop = {
  id, title, description,
  phases: {
    red: {
      tests: [...],           // Test suite
      mocks: {...},           // Mock data sets
      guidance: "..."         // Learning objective
    },
    green: {
      minimumRequirements: "Pass all RED tests",
      hints: [...]
    },
    refactor: {
      guidelines: "...",
      codeMetrics: {...},
      mentorSolution: "..." // Reference implementation
    }
  }
}
```

---

## 9. EXECUTION & FEEDBACK LOOP

### Test Execution Flow
```
1. User writes code in editor
2. Tests run (on-submit or continuous)
3. For each test:
   ├─ Run mock data through function
   ├─ Capture output
   ├─ Compare assertions
   └─ Highlight mismatches
4. Display detailed failure report
5. If all RED tests pass → Suggest REFACTOR
```

### Rich Assertion Feedback
```
Mock Data Used:
  Input: [3, 1, 4, 1, 5]
  
Expected: [1, 1, 3, 4, 5]
Got:      [3, 1, 4, 1, 5]

Why it failed:
  Your function returned the input unchanged.
  The sort algorithm isn't implemented yet.
  
Hint: Consider using a comparison approach.
```

---

## 10. INTERACTIVE MOCK DATA EDITOR

### Advanced Mock Management
```
Mock Data Editor for: "test_sort_large_list"
┌────────────────────────────────────────┐
│ Input Data                             │
├────────────────────────────────────────┤
│ [3, 1, 4, 1, 5, 9, 2, 6, 5]           │
│                                        │
│ ✏️ Edit | 🔄 Regenerate | 💾 Save     │
│ 🎲 Randomize | 📊 Show Stats          │
├────────────────────────────────────────┤
│ Expected Output                        │
├────────────────────────────────────────┤
│ [1, 1, 2, 3, 4, 5, 5, 6, 9]           │
│                                        │
│ Auto-update from input? [Toggle]      │
└────────────────────────────────────────┘

Test Now | Save & Close
```

---

## 11. LEARNING PATH PROGRESSION

### Scaffolded TDD Learning
```
Module 1: "TDD Fundamentals"
  ├─ Workshop 1: Simple assertion (see test, write code)
  ├─ Workshop 2: Multiple test cases
  ├─ Workshop 3: Edge cases in mocks
  └─ Workshop 4: Complete RED→GREEN→REFACTOR cycle

Module 2: "TDD Patterns"
  ├─ Workshop 1: AAA (Arrange-Act-Assert)
  ├─ Workshop 2: Mocking dependencies
  ├─ Workshop 3: Test fixtures
  └─ Workshop 4: Parameterized tests

Module 3: "Advanced TDD"
  ├─ Workshop 1: Property-based testing
  ├─ Workshop 2: Mutation testing
  ├─ Workshop 3: Performance testing
  └─ Workshop 4: Contract testing
```

---

## 12. QUICK WINS FOR MVP

### Phase 1: Core TDD Mechanics
- [ ] Test case display panel (RED phase visibility)
- [ ] Mock data sidebar
- [ ] Assertion-by-assertion feedback
- [ ] Simple RED/GREEN/REFACTOR phase indicators

### Phase 2: Mock Data System
- [ ] Mock data editor UI
- [ ] Multiple mock sets per test
- [ ] History tracking
- [ ] Custom mock creation

### Phase 3: Rich Feedback
- [ ] Code metrics (complexity, coverage)
- [ ] Refactor suggestions
- [ ] Mentor solutions
- [ ] Progress badges

---

## 13. SPECIFIC ENHANCEMENTS TO EXISTING CODE

### Modify `workshop.js` Data Structure
```javascript
// Add test suite to workshop
workshop.testSuite = {
  tests: [
    {
      id: "test_1",
      name: "test_add_positive_numbers",
      phase: "red",
      mocks: { inputs: [2, 3], expected: 5 },
      assertion: "assertEqual"
    }
  ]
}
```

### New Service: `test-runner.js`
```javascript
export class TestRunnerService {
  static async runTests(code, testSuite, mockData) {
    // Execute user code against tests
    // Return detailed pass/fail per assertion
  }
}
```

### New Component: `test-panel.js`
```javascript
export class TestPanelComponent {
  static render(testSuite, execResults) {
    // Display tests with visual indicators
    // Show assertions side-by-side
  }
}
```

---

## 14. BENEFITS OF THIS TRANSFORMATION

| Benefit | How It Happens |
|---------|----------------|
| **Teaches TDD mindset** | Tests visible from start, code follows |
| **Reveals testing importance** | See how mocks catch edge cases |
| **Reduces debugging confusion** | Explicit assertion feedback |
| **Builds confidence** | Progress tracked through phases |
| **Improves code quality** | REFACTOR phase incentivizes clean code |
| **Mock data literacy** | Understanding what to test taught implicitly |

---

## Next Steps

1. **Choose MVP scope**: Start with RED/GREEN phases + basic mock system
2. **Design mock data format**: JSON structure for test cases & mocks
3. **Build test runner**: Safe code execution + assertion parsing
4. **Create UI panels**: Test display, mock editor, phase indicator
5. **Refactor existing state**: Integrate test data into workshop state