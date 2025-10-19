# Transform Python Skill Builder to TDD Training Camp - Guided Workflow

## Overview
Refactor the Python Skill Builder application from a traditional code submission model to a **guided TDD workflow** that walks learners through the Red-Green-Refactor cycle **step by step**. Instead of showing all phases simultaneously, users progress through a wizard-like experience where each phase is a distinct, gated step with specific objectives.

## Problem Statement
The current application:
- Treats tests as invisible backend validation
- Doesn't teach test-first thinking
- Doesn't guide users through the TDD cycle
- Users skip directly to code without understanding requirements
- Missing the discipline of writing tests *before* code

## Solution Overview
Create a **step-by-step TDD workflow wizard** where:

1. **STEP 1 - Design Tests** → User defines mock data scenarios
2. **STEP 2 - RED: Write Test** → User writes a failing test using the mock data
3. **STEP 3 - RED Validation** → System validates test syntax and confirms it fails
4. **STEP 4 - GREEN: Write Code** → User writes minimal code to pass the test
5. **STEP 5 - GREEN Validation** → System validates code passes the test
6. **STEP 6 - Add More Tests** → User adds additional tests with different mock data (edge cases, etc.)
7. **STEP 7 - REFACTOR: Improve Code** → User refactors code while keeping all tests green
8. **STEP 8 - REFACTOR Validation** → System validates code is improved and all tests still pass

Each step is **gated**—users cannot advance until requirements are met.

---

## User Experience Flow

### Workshop Entry
```
User clicks "Start Workshop"
│
├─ Read workshop description
├─ See learning objective
└─ Click "Begin TDD Cycle" → Enter STEP 1
```

### STEP 1: Define Mock Data Scenarios (DESIGN)
```
┌─────────────────────────────────────────────┐
│ STEP 1 of 8: Design Test Scenarios          │
├─────────────────────────────────────────────┤
│                                             │
│ Objective: Plan your test cases by          │
│ defining different mock data scenarios      │
│                                             │
│ Feature: Add two numbers                    │
│                                             │
│ Plan your test scenarios:                   │
│                                             │
│ Scenario 1: Positive Numbers                │
│   Input: a=2, b=3                          │
│   Expected: 5                              │
│                                             │
│ Scenario 2: Negative Numbers                │
│   Input: a=-1, b=-2                        │
│   Expected: -3                             │
│                                             │
│ Scenario 3: Zero Handling                   │
│   Input: a=5, b=0                          │
│   Expected: 5                              │
│                                             │
│ Scenario 4: Large Numbers (optional)        │
│   Input: a=999999, b=1                     │
│   Expected: 1000000                        │
│                                             │
├─────────────────────────────────────────────┤
│ Requirements:                               │
│  • Define at least 2 mock scenarios         │
│  • Include inputs and expected outputs      │
│  • One happy path, one edge case            │
│                                             │
│ [Add Scenario] [Remove Last]                │
│                                             │
│ [Continue to Test Writing] →                │
└─────────────────────────────────────────────┘
```

### STEP 2: Write a Failing Test (RED)
```
┌─────────────────────────────────────────────┐
│ STEP 2 of 8: Write a Failing Test           │
├─────────────────────────────────────────────┤
│                                             │
│ Objective: Write a test that currently     │
│ fails (because the feature doesn't exist)  │
│                                             │
│ Your First Mock Scenario:                   │
│  Scenario: Positive Numbers                 │
│  Input: a=2, b=3                           │
│  Expected: 5                               │
│                                             │
│ Task: Create a test using this mock data   │
│                                             │
│ Requirements:                               │
│  • Test function name starts with test_    │
│  • Use the mock inputs: add(2, 3)          │
│  • Assert the result equals 5              │
│  • Test must fail initially                 │
│                                             │
│ Example test structure:                     │
│  def test_add_positive_numbers():          │
│      result = add(2, 3)                   │
│      assert result == 5                   │
│                                             │
├─────────────────────────────────────────────┤
│ [Code Editor - Write Your Test]             │
│                                             │
│ def test_():                               │
│     pass                                    │
│                                             │
├─────────────────────────────────────────────┤
│ [Validate Test] [Get Hint] [See Example]   │
└─────────────────────────────────────────────┘
```

### STEP 3: Validate Test Fails (RED Confirmation)
```
┌─────────────────────────────────────────────┐
│ STEP 3 of 8: Test Validation (RED)          │
├─────────────────────────────────────────────┤
│                                             │
│ ✅ Test syntax is valid                    │
│ ✅ Test executed successfully              │
│ ✅ Test failed as expected                 │
│                                             │
│ Test Output:                                │
│ ❌ test_add_positive_numbers FAILED         │
│    AssertionError: add(2, 3) returned None │
│                                             │
│ Perfect! Now we know what we need to build.│
│                                             │
├─────────────────────────────────────────────┤
│         [Continue to GREEN] →               │
└─────────────────────────────────────────────┘
```

### STEP 4: Write Code to Pass Test (GREEN)
```
┌─────────────────────────────────────────────┐
│ STEP 4 of 8: Write Code to Pass Test        │
├─────────────────────────────────────────────┤
│                                             │
│ Objective: Write minimal code to make      │
│ the test pass (no over-engineering)        │
│                                             │
│ Your Test (read-only):                     │
│  def test_add_positive_numbers():           │
│      result = add(2, 3)                    │
│      assert result == 5                    │
│                                             │
│ Task: Implement the add() function         │
│                                             │
│ Starter Code:                               │
│  def add(a, b):                            │
│      pass                                   │
│                                             │
├─────────────────────────────────────────────┤
│ [Code Editor - Implement Function]          │
│                                             │
│ def add(a, b):                             │
│     return a + b                           │
│                                             │
├─────────────────────────────────────────────┤
│ [Run Test] [Get Hint] [Show Solution]      │
└─────────────────────────────────────────────┘
```

### STEP 5: Validate Code Passes Test (GREEN Confirmation)
```
┌─────────────────────────────────────────────┐
│ STEP 5 of 8: Test Validation (GREEN)        │
├─────────────────────────────────────────────┤
│                                             │
│ ✅ Code syntax is valid                    │
│ ✅ Test executed successfully              │
│ ✅ Test passed!                            │
│                                             │
│ Test Output:                                │
│ ✅ test_add_positive_numbers PASSED        │
│    assert 5 == 5 ✓                         │
│                                             │
│ Excellent! Now let's add more test cases.  │
│                                             │
├─────────────────────────────────────────────┤
│    [Continue to More Tests] →               │
└─────────────────────────────────────────────┘
```

### STEP 6: Add More Test Cases (Expand RED)
```
┌─────────────────────────────────────────────┐
│ STEP 6 of 8: Write Additional Tests         │
├─────────────────────────────────────────────┤
│                                             │
│ Objective: Add test cases for other        │
│ scenarios to ensure robustness             │
│                                             │
│ ✅ Test 1 PASSING: test_add_positive       │
│                                             │
│ Your Next Mock Scenario:                    │
│  Scenario: Negative Numbers                 │
│  Input: a=-1, b=-2                         │
│  Expected: -3                              │
│                                             │
│ Requirements:                               │
│  • Add at least one more test case         │
│  • Use a different mock scenario           │
│  • Test must initially fail (add works     │
│    for positive, but needs validation)     │
│                                             │
├─────────────────────────────────────────────┤
│ [Code Editor - Add More Tests]              │
│                                             │
│ def test_add_negative_numbers():            │
│     result = add(-1, -2)                   │
│     assert result == -3                    │
│                                             │
│ def test_add_with_zero():                  │
│     result = add(5, 0)                     │
│     assert result == 5                     │
│                                             │
├─────────────────────────────────────────────┤
│ [Validate Tests] [Get Hint]                │
│                                             │
│ Or skip to refactoring: [Skip to Refactor] │
└─────────────────────────────────────────────┘
```

### STEP 7: Validate All Tests Still Green
```
┌─────────────────────────────────────────────┐
│ STEP 7 of 8: All Tests Green                │
├─────────────────────────────────────────────┤
│                                             │
│ ✅ All tests pass!                         │
│                                             │
│ Test Results:                               │
│ ✅ test_add_positive_numbers PASSED        │
│ ✅ test_add_negative_numbers PASSED        │
│ ✅ test_add_with_zero PASSED               │
│                                             │
│ Current Implementation:                     │
│  def add(a, b):                            │
│      return a + b                          │
│                                             │
│ Your code handles multiple test scenarios! │
│ Now let's refactor for quality.            │
│                                             │
├─────────────────────────────────────────────┤
│    [Continue to REFACTOR] →                 │
└─────────────────────────────────────────────┘
``` Added docstring                         │
│  ✓ More maintainable                       │
│                                             │
│ Compare to Mentor Solution:                 │
│  [Show/Hide Mentor Code]                    │
│                                             │
├─────────────────────────────────────────────┤
│  Score: 95/100 | 🏆 Great work!            │
│                                             │
│  [Complete Workshop] [Next Workshop] →     │
└─────────────────────────────────────────────┘
```

---

## Detailed Requirements

### Phase 1: Workflow Engine & Mock Data Integration (MVP)

#### 1.1 Mock Data Design Component (STEP 1)
- [ ] Create `MockDataDesignStep` component for defining test scenarios
- [ ] Allow users to define multiple scenarios with:
  - Scenario name (e.g., "Positive Numbers")
  - Input values (e.g., a=2, b=3)
  - Expected output (e.g., 5)
  - Description/rationale
- [ ] UI to add/remove scenarios
- [ ] Validation:
  - At least 2 scenarios required (happy path + edge case)
  - Each scenario must have inputs and expected output
  - Scenario names should be descriptive
- [ ] Display scenarios as editable cards
- [ ] Save scenarios to workflow state

**Files to create:**
- `components/workflow/mock-data-design.js` - Scenario editor
- `components/workflow/scenario-card.js` - Individual scenario UI
- `logic/mock-data-validator.js` - Validate mock scenarios

#### 1.2 TDD Workflow State Machine
- [ ] Create `TDDWorkflowState` class to manage steps 1-8
- [ ] Track current step: `step`, `completed`, `locked`
- [ ] Store mock scenarios defined in STEP 1
- [ ] Store all tests written (STEP 2, 6)
- [ ] Store implementation code (STEP 4)
- [ ] Store refactored code (STEP 7)
- [ ] Define step progression rules:
  ```javascript
  {
    step: 1,
    name: 'design_mock_data',
    status: 'in_progress|completed|locked',
    mockScenarios: [
      { id: 1, name: 'Positive Numbers', inputs: [2, 3], expected: 5 },
      { id: 2, name: 'Negative Numbers', inputs: [-1, -2], expected: -3 }
    ],
    validation: {
      rules: ['at_least_2_scenarios', 'all_scenarios_valid'],
      errors: [],
      warnings: []
    }
  }
  ```
- [ ] Prevent advancing without meeting step requirements
- [ ] Allow "going back" to previous steps (for edits)

**Files to create:**
- `state/tdd-workflow.js` - Step management
- `logic/tdd-validator.js` - Validation rules per step

#### 1.2 Step Display Component
- [ ] Create `TDDWorkflowStep` component that renders:
  - Step number and title (e.g., "STEP 2 of 8: Write a Failing Test")
  - Objective and learning goal
  - Current mock scenario context (for test-writing steps)
  - Requirements checklist
  - Code editor (for test/code)
  - Action buttons (Validate, Get Hint, Show Solution, Skip)
  - Status indicators (requirements met?)
- [ ] Dynamic content based on current step
- [ ] Show current mock scenario prominently in STEP 2, 6
- [ ] Hide/show elements based on step type

**Files to create:**
- `components/workflow/step-display.js`
- `components/workflow/step-objective.js`
- `components/workflow/step-requirements.js`
- `components/workflow/step-actions.js`
- `components/workflow/scenario-context.js` - Display current mock scenario being tested

#### 1.3 Step Validation Engine
- [ ] **STEP 1 Validation**: Mock data scenarios
  - At least 2 scenarios defined
  - Each scenario has inputs, expected output, name
  - Inputs are appropriate for feature (e.g., numbers for add)
  - Return errors if validation fails

- [ ] **STEP 2 Validation**: Test syntax and execution
  - Parse test function definition
  - Validate test name starts with `test_`
  - Validate at least one assertion
  - Run test to confirm it fails (add() doesn't exist)
  - Return errors/warnings if invalid

- [ ] **STEP 4 Validation**: Code implementation
  - Parse function definition
  - Validate function exists and is callable
  - Run user's first test against user's code
  - Confirm test passes
  - Return errors/warnings if invalid

- [ ] **STEP 6 Validation**: Additional tests
  - Parse all test functions
  - Validate at least 2 total tests exist
  - Validate each test has different mock data
  - Run all tests to confirm they fail initially (optional stricter mode)
  - Return errors/warnings if invalid

- [ ] **STEP 7 Validation**: Refactored code
  - Validate code syntax
  - Run ALL tests to confirm still pass
  - Calculate code metrics (complexity, coverage)
  - Check if code improved from STEP 4 version
  - Suggest refactoring if metrics not improved

**Files to create:**
- `services/step-validator.js`
- `services/mock-data-validator.js` - Validate mock scenarios
- `services/test-parser.js` - Extract test function
- `services/code-parser.js` - Extract function definition
- `services/code-metrics.js` - Calculate complexity, coverage

#### 1.4 Mock Data Persistence
- [ ] Store mock scenarios in workflow state during STEP 1
- [ ] Display selected scenario in STEP 2 and STEP 6
- [ ] Pass scenario inputs/expected to test validator
- [ ] Allow editing mock scenarios mid-workflow (go back to STEP 1)
- [ ] Show all scenarios with pass/fail status after code is written

**Files to create:**
- `state/mock-data-store.js` - Store and retrieve scenarios

#### 1.4 Execution Sandbox
- [ ] Build safe test runner that executes:
  - User-written tests (STEP 1)
  - User-written code with their tests (STEP 3)
  - User-refactored code with their tests (STEP 5)
- [ ] Capture output, errors, and timing
- [ ] Return structured results:
  ```javascript
  {
    success: true|false,
    testsPassed: 5,
    testsFailed: 0,
    executionTime: 245,
    output: "...",
    errors: []
  }
  ```
- [ ] Implement timeout protection (max 5s execution)

**Files to create:**
- `services/code-executor.js` - Safe execution
- `services/test-runner.js` - Test-specific execution

---

### Phase 2: Workshop Content & Hints System

#### 2.1 Enhanced Workshop Schema
```javascript
{
  id: "workshop_add_function",
  title: "Build an Add Function",
  description: "Learn TDD by building a function step by step",
  
  // TDD Workflow Definition
  tddWorkflow: {
    feature: "add(a, b) - Add two numbers",
    
    steps: {
      design_mock_data: {
        objective: "Plan your test scenarios with mock data",
        instruction: "Define what inputs you want to test and what outputs you expect",
        requirements: [
          "Define at least 2 mock scenarios",
          "Each scenario has inputs and expected output",
          "Include one happy path scenario",
          "Include one edge case scenario"
        ],
        suggestedScenarios: [
          { name: "Positive Numbers", inputs: [2, 3], expected: 5 },
          { name: "Negative Numbers", inputs: [-1, -2], expected: -3 },
          { name: "Zero Handling", inputs: [5, 0], expected: 5 },
          { name: "Large Numbers", inputs: [999999, 1], expected: 1000000 }
        ],
        hints: [
          "Start with simple cases (positive numbers)",
          "Then add edge cases (zero, negatives)",
          "Think about what could break your code"
        ]
      },
      
      red_write_test: {
        objective: "Write a test for the first mock scenario",
        instruction: "Write a test that uses the mock data you defined",
        requirements: [
          "Function name starts with test_",
          "Uses mock inputs from your scenario",
          "Has an assertion checking for expected output",
          "Test must fail (add() doesn't exist yet)"
        ],
        starterCode: "def test_():\n    pass",
        exampleCode: "def test_add_positive_numbers():\n    result = add(2, 3)\n    assert result == 5",
        hints: [
          "Use the mock data: inputs [2, 3], expected 5",
          "The test should fail because add() isn't implemented",
          "Follow naming convention: test_<function>_<scenario>"
        ]
      },
      
      green_write_code: {
        objective: "Write minimal code to pass your test",
        instruction: "Implement add() to make your test pass",
        requirements: [
          "Function named add()",
          "Accepts two parameters",
          "Returns sum of parameters",
          "User's test passes"
        ],
        starterCode: "def add(a, b):\n    pass",
        exampleCode: "def add(a, b):\n    return a + b",
        hints: [
          "Start simple - don't over-engineer",
          "Your test expects add(2, 3) to return 5",
          "Minimum code wins in GREEN phase"
        ]
      },
      
      add_more_tests: {
        objective: "Add tests for your other mock scenarios",
        instruction: "Create tests for edge cases and different scenarios",
        requirements: [
          "Add at least one more test",
          "Use a different mock scenario",
          "All existing tests still pass",
          "New tests should work with your implementation"
        ],
        hints: [
          "Test the negative numbers scenario next",
          "Your implementation should handle these too",
          "More tests = more confidence"
        ]
      },
      
      refactor_improve_code: {
        objective: "Improve code quality while keeping all tests green",
        instruction: "Refactor add() to be more professional",
        requirements: [
          "All tests still pass",
          "Add type hints",
          "Add docstring",
          "Code complexity unchanged or improved"
        ],
        exampleCode: 'def add(a: int, b: int) -> int:\n    """Add two integers and return the sum."""\n    return a + b',
        hints: [
          "Type hints make code clearer",
          "A docstring explains what the function does",
          "Refactoring improves style, not functionality"
        ],
        codeMetrics: {
          targetComplexity: 1,
          targetCoverage: 100
        }
      }
    }
  }
}
```

**Files to update:**
- `services/modules.js` - Load TDD workflow with mock data definitions
- `config.js` - Add workflow constants

#### 2.2 Adaptive Hints System
- [ ] Context-aware hints based on current step
- [ ] Progressive hint reveals (Get Hint 1 → Get Hint 2 → Show Solution)
- [ ] Detect common errors and suggest specific hints
- [ ] Show example code if user requests
- [ ] Allow skipping step (with penalty/badge)

**Files to create:**
- `services/hints-analyzer.js` - Detect errors and suggest hints
- `components/workflow/step-hints.js` - Display hints UI

---

### Phase 3: Progress & Achievement Tracking

#### 3.1 Workflow Progress State
- [ ] Track completion of each step per workshop:
  ```javascript
  {
    workshopId: {
      currentStep: 3,
      steps: {
        1: { completed: true, code: "...", timestamp: "..." },
        2: { completed: true, validationResult: {...} },
        3: { completed: false, code: "...", attempts: 2 }
      },
      totalAttempts: 5,
      timeSpent: 450, // seconds
      hintRequests: 2,
      skipped: false
    }
  }
  ```
- [ ] Save progress after each step validation
- [ ] Allow resuming from last completed step

**Files to update:**
- `state/progress.js` - Add workflow tracking
- `state/storage.js` - Persist workflow state

#### 3.2 Achievement Badges (TDD-Specific)
- [ ] 🔴 **Red Analyst** - Wrote 5 test cases
- [ ] 🟢 **Green Engineer** - Passed 20 code validations
- [ ] 🔵 **Refactor Master** - Completed 10 refactor steps
- [ ] 🎯 **Full Cycle** - Completed RED-GREEN-REFACTOR on 5 workshops
- [ ] ⚡ **No Hints** - Completed workshop without using hints
- [ ] 🏃 **Speed Demon** - Completed workshop in <5 minutes
- [ ] 🔒 **Strict Mode** - Completed without skipping any steps

**Files to create:**
- `services/achievement-tracker.js`
- `components/achievements/badge-display.js`

---

### Phase 4: Error Handling & User Feedback

#### 4.1 Step-Specific Error Messages
- [ ] **STEP 1 Errors**:
  ```
  ❌ Test name must start with 'test_'
     Your function: my_test() → Should be: test_my_feature()
  
  ❌ No assertions found in test
     Use: assert result == expected
  
  ❌ Test didn't fail as expected
     Your test passed, but it should fail (add() doesn't exist yet)
  ```

- [ ] **STEP 3 Errors**:
  ```
  ❌ Function 'add' not defined
     Your code doesn't have a function called add()
  
  ❌ add() requires 2 arguments but you provided 1
     add(a, b) needs two parameters
  
  ❌ Test failed with your code
     test_add_positive_numbers: expected 5, got None
  ```

- [ ] **STEP 5 Errors**:
  ```
  ⚠️  Test still passes, but code not improved
     Current complexity: 1 (same as before)
     Try adding type hints or a docstring
  ```

**Files to create:**
- `services/error-messages.js` - Human-friendly error display
- `components/workflow/step-errors.js` - Error visualization

#### 4.2 Validation Result Display
```javascript
{
  step: 3,
  valid: false,
  issues: [
    { type: 'error', message: '...', code: 'TEST_FAILED' },
    { type: 'warning', message: '...', code: 'NO_TYPE_HINTS' }
  ],
  details: {
    testOutput: "FAILED: expected 5, got None",
    metrics: { complexity: 2, coverage: 80 }
  }
}
```

---

## Data Structures

### TDDWorkflowState
```javascript
class TDDWorkflowState {
  constructor(workshopId) {
    this.workshopId = workshopId;
    this.currentStep = 1;
    this.steps = {
      1: { 
        completed: false, 
        locked: false, 
        name: 'design_mock_data',
        mockScenarios: [] 
      },
      2: { 
        completed: false, 
        locked: true, 
        name: 'red_write_test',
        code: '',
        currentScenarioId: 0 // Which scenario user is testing
      },
      3: { 
        completed: false, 
        locked: true, 
        name: 'red_validate_test',
        validationResult: null 
      },
      4: { 
        completed: false, 
        locked: true, 
        name: 'green_write_code',
        code: '' 
      },
      5: { 
        completed: false, 
        locked: true, 
        name: 'green_validate_code',
        validationResult: null 
      },
      6: { 
        completed: false, 
        locked: true, 
        name: 'add_more_tests',
        code: '' 
      },
      7: { 
        completed: false, 
        locked: true, 
        name: 'refactor_code',
        code: '' 
      },
      8: { 
        completed: false, 
        locked: true, 
        name: 'refactor_validate',
        validationResult: null 
      }
    };
    this.allTests = []; // All test functions user wrote
    this.implementation = ''; // Final implementation code
    this.metrics = {
      attempts: 0,
      hintsUsed: 0,
      solutionViewed: false,
      timeSpent: 0
    };
  }
  
  getCurrentStep() { /* ... */ }
  getMockScenarios() { /* ... */ }
  getCurrentMockScenario() { /* ... */ }
  addMockScenario(scenario) { /* ... */ }
  canAdvance() { /* ... */ }
  advanceToNextStep() { /* ... */ }
  markStepComplete(stepNum, validationResult) { /* ... */ }
}
```

---

## UI Layout

```
TDDWorkshop
├── Header
│   ├── Workshop Title
│   ├── Step Progress: [STEP X of 6]
│   └── Time Elapsed
├── Main Content
│   ├── StepDisplay
│   │   ├── Objective + Instructions
│   │   ├── Requirements Checklist
│   │   ├── Code Editor (input)
│   │   └── Previous Step Context (read-only, when relevant)
│   └── StepActions
│       ├── [Validate/Continue] (primary button)
│       ├── [Get Hint] (secondary)
│       ├── [Show Example] (secondary)
│       ├── [Show Solution] (tertiary)
│       └── [Skip Step] (low priority)
├── Sidebar
│   ├── Step Checklist (1-6)
│   │   └── Visual progress (completed/current/locked)
│   ├── Requirements Status
│   │   └── ✓ Test syntax valid
│   │   └─ ✗ Test must fail
│   └── Hints Counter
└── Footer
    └── [Back] [Workshop Menu] [Next Workshop]
```

---

## Implementation Roadmap

### Milestone 1: Core Workflow Engine (Week 1)
- [ ] TDDWorkflowState class and step management
- [ ] Mock data design component (STEP 1)
- [ ] Basic step display component
- [ ] Mock data validator
- [ ] Storage for mock scenarios

**Deliverable**: Users can define mock scenarios and see them in workflow

### Milestone 2: Test Writing & Validation (Week 2)
- [ ] Test parser and syntax validation
- [ ] Simple test executor (validate test fails)
- [ ] STEP 2 and 3 validation
- [ ] Error message generation

**Deliverable**: Users can write tests using mock data, validate they fail

### Milestone 3: Code Execution (Week 3)
- [ ] Code parser and function extraction
- [ ] Safe code execution sandbox
- [ ] STEP 4 and 5 validation (code passes test)
- [ ] Multi-test support (STEP 6)

**Deliverable**: Users can write code, validate all tests pass

### Milestone 4: Refactor & Metrics (Week 4)
- [ ] Code metrics (complexity, coverage)
- [ ] STEP 7 and 8 validation
- [ ] Code comparison (before/after)
- [ ] Mentor solution display

**Deliverable**: Users can refactor and validate improvements

### Milestone 5: Polish & Launch (Week 5)
- [ ] Hints system with progressive reveals
- [ ] Achievement system
- [ ] Progress persistence
- [ ] Sample workshop content (5 complete workflows with mock data scenarios)

**Deliverable**: Production-ready TDD workshop with mock data integration

---

## Testing Strategy

### Unit Tests
- [ ] `TDDWorkflowState` step transitions and validation
- [ ] `TestParser` - Parse and validate test code
- [ ] `CodeParser` - Parse and validate implementation code
- [ ] `CodeMetrics` - Calculate complexity and coverage
- [ ] Error message generation

### Integration Tests
- [ ] Complete STEP 1 → STEP 2 flow
- [ ] Complete STEP 3 → STEP 4 flow
- [ ] Complete STEP 5 → STEP 6 flow
- [ ] Full RED-GREEN-REFACTOR cycle
- [ ] Progress persistence and recovery

### E2E Tests
- [ ] User writes failing test → sees validation failure → corrects it → sees validation pass
- [ ] User writes code → sees test pass → advances to refactor
- [ ] User refactors code → sees metrics improve → completes workshop

---

## Success Criteria

1. ✅ Users cannot skip STEP 1 - they must define mock scenarios first
2. ✅ STEP 2: Users can see mock scenario data and write tests for it
3. ✅ STEP 3: Tests are validated and must fail with clear feedback
4. ✅ STEP 4: Users can write code to pass the test
5. ✅ STEP 5: Code is validated and tests pass
6. ✅ STEP 6: Users can add more tests using different mock scenarios
7. ✅ STEP 7-8: Users can refactor code while all tests stay green
8. ✅ Mock scenarios are displayed prominently at each relevant step
9. ✅ Users understand what they're testing and why (through mock data design)
10. ✅ At least 85% of users complete all 8 steps per workshop
11. ✅ Average time per workshop: 12-18 minutes (longer due to mock data + multi-test)
12. ✅ Mock data teaching helps users understand edge case testing

---

## Sample Workshop Data (Example)

See: `docs/sample-workshops/add-function.json`

---

## Notes for Implementation

- **Step validation must be robust**: Parse user code carefully, handle syntax errors gracefully
- **Execution sandboxing is critical**: Use a safe execution environment for code
- **Progressive disclosure**: Show exactly what the user needs to complete current step
- **Fail fast, help quickly**: When validation fails, provide immediate feedback and hints
- **Save progress**: Users should be able to leave and return to their work
- **Test-first discipline**: Make it impossible to skip the test-writing step (no shortcuts)

---

## Acceptance Checklist

- [ ] All 6 steps implemented with gating logic
- [ ] Test parser validates test syntax and execution
- [ ] Code parser validates function definition
- [ ] Code executor safely runs user code
- [ ] Error messages are clear and actionable
- [ ] Hints system provides progressive guidance
- [ ] Progress persists across sessions
- [ ] At least one complete sample workshop available
- [ ] Performance: <1s validation per step
- [ ] All unit tests passing
- [ ] All E2E tests passing
- [ ] Accessibility review passed (WCAG AA)
- [ ] Team approval