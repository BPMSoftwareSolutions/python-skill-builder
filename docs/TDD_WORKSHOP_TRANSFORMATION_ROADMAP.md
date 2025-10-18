# TDD Workshop UI Transformation Roadmap

## Overview

This document outlines the complete transformation of the Python Skill Builder workshop interface from a linear code submission model to a **Test-Driven Development (TDD) training platform** following the **Red → Green → Refactor** pedagogy.

**Main Issue**: [#3 - Transform Workshop UI to TDD-First Training Platform](https://github.com/BPMSoftwareSolutions/python-skill-builder/issues/3)

## Current State vs Target State

### Current Architecture
```
Workshop View (Vertical Layout)
├── Header (title, progress, nav)
├── Prompt Section
├── Code Editor
├── Hints Section
├── Actions Section
└── Feedback Section
```

**Workflow**: Write code → Submit → Get feedback

### Target Architecture
```
Workshop View (3-Panel Horizontal Layout)
├── Header (title, phase buttons, nav)
├── Main Content
│   ├── LEFT: Test Panel (Tests visible from start)
│   ├── CENTER: Code Editor (with run tests button)
│   └── RIGHT: Mock Data + Metrics (phase-aware)
└── Footer (status, navigation)
```

**Workflow**: See tests → Write code → Run tests → Refactor

## Transformation Phases

### Phase 1: UI Layout Restructuring (3-Panel Design)
**Issue**: [#4](https://github.com/BPMSoftwareSolutions/python-skill-builder/issues/4)
- **Duration**: 2-3 days
- **Complexity**: Medium
- **Deliverables**:
  - 3-panel horizontal layout (Tests | Editor | Mock Data)
  - Responsive design (desktop, tablet, mobile)
  - Phase indicator buttons (RED/GREEN/REFACTOR)
  - Tailwind-compatible color palette
- **Learning Value**: Foundation for all TDD features
- **Acceptance**: Layout renders correctly on all screen sizes, all tests pass

### Phase 2: Test Panel Implementation (RED Phase Visibility)
**Issue**: [#5](https://github.com/BPMSoftwareSolutions/python-skill-builder/issues/5)
- **Duration**: 3-4 days
- **Complexity**: Medium
- **Depends On**: Phase 1
- **Deliverables**:
  - Test case display with pass/fail indicators
  - Expandable test details (assertion, expected, actual, error)
  - Test progress bar (X/Y tests passing)
  - Mock data inputs visible for each test
- **Learning Value**: Learners see requirements before coding
- **Acceptance**: All tests display correctly, progress updates in real-time

### Phase 3: Mock Data System (Multiple Test Scenarios)
**Issue**: [#6](https://github.com/BPMSoftwareSolutions/python-skill-builder/issues/6)
- **Duration**: 3-4 days
- **Complexity**: Medium
- **Depends On**: Phase 1
- **Deliverables**:
  - Mock data selector UI (Valid, Edge Cases, Stress Test)
  - Mock data preview panel
  - Mock data editor for custom scenarios
  - Multiple mock sets per workshop
- **Learning Value**: Learners understand edge cases and robust code
- **Acceptance**: Mock sets display, switch correctly, tests use selected data

### Phase 4: Code Metrics & Refactor Guide (REFACTOR Phase Support)
**Issue**: [#7](https://github.com/BPMSoftwareSolutions/python-skill-builder/issues/7)
- **Duration**: 4-5 days
- **Complexity**: High
- **Depends On**: Phase 1
- **Deliverables**:
  - Code metrics display (complexity, coverage, lines, duplication)
  - Refactor suggestions panel
  - Mentor solution comparison
  - Phase-aware display (only in REFACTOR phase)
- **Learning Value**: Learners learn code quality and refactoring
- **Acceptance**: Metrics display accurately, suggestions are actionable

### Phase 5: Test Runner Service (Execute Tests Safely)
**Issue**: [#8](https://github.com/BPMSoftwareSolutions/python-skill-builder/issues/8)
- **Duration**: 5-6 days
- **Complexity**: Very High
- **Depends On**: Phase 1
- **Deliverables**:
  - Safe Python code execution sandbox
  - Test runner service with timeout/memory limits
  - Assertion parser for detailed feedback
  - API endpoint `/api/workshops/{id}/run-tests`
  - Coverage analyzer
- **Learning Value**: Learners run tests and see immediate feedback
- **Acceptance**: Tests execute safely, results accurate, < 2 second response

### Phase 6: Data Structure Evolution (Workshop TDD Format)
**Issue**: [#9](https://github.com/BPMSoftwareSolutions/python-skill-builder/issues/9)
- **Duration**: 3-4 days
- **Complexity**: Medium
- **Depends On**: All previous phases
- **Deliverables**:
  - Extended workshop schema with phases, tests, mock data
  - Test suite schema with assertions and metadata
  - Mock data schema with data points
  - Phase guidance schema (RED/GREEN/REFACTOR)
  - Data migration script for existing workshops
  - Sample TDD workshop (reference implementation)
- **Learning Value**: Complete TDD learning experience
- **Acceptance**: Schema supports all features, migrations successful

### Phase 7: Achievement System & Gamification (TDD Milestones)
**Issue**: [#10](https://github.com/BPMSoftwareSolutions/python-skill-builder/issues/10)
- **Duration**: 2-3 days
- **Complexity**: Low-Medium
- **Depends On**: All previous phases
- **Deliverables**:
  - 15-20 TDD-specific achievements (Red Phase Master, Green Achiever, Refactor Wizard, etc.)
  - Achievement tracking system
  - Achievement display components and notifications
  - Dashboard integration with achievements showcase
  - Streak tracking and statistics
- **Learning Value**: Recognition and motivation for TDD mastery
- **Acceptance**: Achievements unlock correctly, display on dashboard, learners see progress

## Implementation Timeline

```
Week 1: Phase 1 (Layout) + Phase 2 (Tests)
├── Phase 1: UI Layout Restructuring (2-3 days)
└── Phase 2: Test Panel Implementation (3-4 days)

Week 2: Phase 3 (Mock Data) + Phase 4 (Metrics)
├── Phase 3: Mock Data System (3-4 days)
└── Phase 4: Code Metrics & Refactor (4-5 days)

Week 3: Phase 5 (Test Runner)
└── Phase 5: Test Runner Service (5-6 days)

Week 4: Phase 6 (Data Structure) + Phase 7 (Achievements)
├── Phase 6: Data Structure Evolution (3-4 days)
├── Phase 7: Achievement System (2-3 days)
└── Integration & Testing (2-3 days)

Total Estimated Effort: 5-6 weeks
```

## Success Criteria

### Technical
- ✅ All 88+ unit tests pass
- ✅ Code coverage ≥ 92%
- ✅ ESLint: 0 errors
- ✅ Responsive design verified on 3+ screen sizes
- ✅ Test execution < 2 seconds
- ✅ No security vulnerabilities

### Learning
- ✅ Learners see tests first (RED phase)
- ✅ Learners write test-driven code (GREEN phase)
- ✅ Learners understand mock data and edge cases
- ✅ Learners learn refactoring (REFACTOR phase)
- ✅ Learners build confidence through explicit phases

### Product
- ✅ Product manager approval after exploratory testing
- ✅ Backward compatibility maintained
- ✅ Sample workshop demonstrates best practices
- ✅ Documentation complete

## Key Design Decisions

1. **Three-Panel Layout**: Tests | Code | Mock Data + Metrics
   - Rationale: Makes all learning elements visible simultaneously
   - Responsive: Stacks on mobile, 2-column on tablet, 3-column on desktop

2. **Explicit RED/GREEN/REFACTOR Phases**
   - Rationale: Makes TDD pedagogy explicit and visible
   - Guidance: Phase-specific hints and metrics

3. **Mock Data System**
   - Rationale: Teaches edge cases and robust code
   - Scenarios: Valid inputs, edge cases, stress tests

4. **Safe Test Execution**
   - Rationale: Prevent malicious code, infinite loops, resource exhaustion
   - Sandbox: RestrictedPython or similar, timeout, memory limits

5. **Backward Compatibility**
   - Rationale: Existing workshops continue to work
   - Migration: Script converts existing data to new format

## Related Documentation

- `docs/TDD_TRAINING_CAMP.md` - Comprehensive TDD strategy
- `docs/prototypes/tdd_workshop_ui.tsx` - Target UI prototype
- `docs/workshop-schema.md` - Workshop data schema (to be created)

## GitHub Issues

| Phase | Issue | Status | Effort |
|-------|-------|--------|--------|
| Main | [#3](https://github.com/BPMSoftwareSolutions/python-skill-builder/issues/3) | Open | 5-6 weeks |
| 1 | [#4](https://github.com/BPMSoftwareSolutions/python-skill-builder/issues/4) | Open | 2-3 days |
| 2 | [#5](https://github.com/BPMSoftwareSolutions/python-skill-builder/issues/5) | Open | 3-4 days |
| 3 | [#6](https://github.com/BPMSoftwareSolutions/python-skill-builder/issues/6) | Open | 3-4 days |
| 4 | [#7](https://github.com/BPMSoftwareSolutions/python-skill-builder/issues/7) | Open | 4-5 days |
| 5 | [#8](https://github.com/BPMSoftwareSolutions/python-skill-builder/issues/8) | Open | 5-6 days |
| 6 | [#9](https://github.com/BPMSoftwareSolutions/python-skill-builder/issues/9) | Open | 3-4 days |
| 7 | [#10](https://github.com/BPMSoftwareSolutions/python-skill-builder/issues/10) | Open | 2-3 days |

## Next Steps

1. **Review & Approve**: Product team reviews main issue #3 and sub-issues
2. **Start Phase 1**: Begin UI layout restructuring
3. **Exploratory Testing**: Product manager tests each phase
4. **Iterate**: Refine based on feedback
5. **Launch**: Deploy complete TDD platform

---

**Created**: 2025-10-18
**Last Updated**: 2025-10-18
**Status**: Planning Phase

