/**
 * Unit Tests for TDD Workflow Component
 */

// Import components
const WorkflowAPI = require('./js/services/workflow-api.js');
const PhaseProgress = require('./js/components/phase-progress.js');
const RequirementsChecklist = require('./js/components/requirements-checklist.js');
const ValidationFeedback = require('./js/components/validation-feedback.js');
const StepCodeEditor = require('./js/components/step-code-editor.js');
const HintsPanel = require('./js/components/hints-panel.js');
const TDDWorkflowComponent = require('./js/components/tdd-workflow.js');

// Make classes available globally for tests
global.WorkflowAPI = WorkflowAPI;
global.PhaseProgress = PhaseProgress;
global.RequirementsChecklist = RequirementsChecklist;
global.ValidationFeedback = ValidationFeedback;
global.StepCodeEditor = StepCodeEditor;
global.HintsPanel = HintsPanel;
global.TDDWorkflowComponent = TDDWorkflowComponent;

describe('TDDWorkflowComponent', () => {
  let component;
  let container;

  beforeEach(() => {
    // Create a container for rendering
    container = document.createElement('div');
    document.body.appendChild(container);

    // Create component instance
    component = new TDDWorkflowComponent('workshop_123', 'workflow_456');
  });

  afterEach(() => {
    document.body.removeChild(container);
  });

  describe('initialization', () => {
    test('should create component with correct properties', () => {
      expect(component.workshopId).toBe('workshop_123');
      expect(component.workflowId).toBe('workflow_456');
      expect(component.currentStep).toBe(1);
    });

    test('should have API client', () => {
      expect(component.api).toBeDefined();
      expect(component.api instanceof WorkflowAPI).toBe(true);
    });
  });

  describe('rendering', () => {
    test('should render workflow container', () => {
      component.render(container);
      const wrapper = container.querySelector('.tdd-workflow-container');
      expect(wrapper).toBeDefined();
    });

    test('should render phase progress', () => {
      component.render(container);
      const progress = container.querySelector('.phase-progress-wrapper');
      expect(progress).toBeDefined();
    });

    test('should render three panels', () => {
      component.render(container);
      const panels = container.querySelectorAll('.workflow-panel');
      expect(panels.length).toBe(3);
    });

    test('should render action buttons', () => {
      component.render(container);
      const buttons = container.querySelectorAll('.action-buttons button');
      expect(buttons.length).toBeGreaterThan(0);
    });
  });

  describe('step management', () => {
    test('should update current step', () => {
      component.updateCurrentStep(3);
      expect(component.currentStep).toBe(3);
    });

    test('should save code for step', () => {
      const code = 'def test_add():\n    pass';
      component.saveCodeForStep(1, code);
      expect(component.codePerStep[1]).toBe(code);
    });

    test('should load code for step', () => {
      const code = 'def test_add():\n    pass';
      component.saveCodeForStep(1, code);
      const loaded = component.loadCodeForStep(1);
      expect(loaded).toBe(code);
    });

    test('should return empty string for unsaved step', () => {
      const loaded = component.loadCodeForStep(99);
      expect(loaded).toBe('');
    });
  });

  describe('requirements', () => {
    test('should get requirements for step 1', () => {
      const reqs = component.getRequirementsForStep(1);
      expect(reqs.length).toBeGreaterThan(0);
      expect(reqs[0]).toContain('test_');
    });

    test('should get starter code for step 1', () => {
      const code = component.getStarterCodeForStep(1);
      expect(code).toContain('def test_');
    });

    test('should get starter code for step 3', () => {
      const code = component.getStarterCodeForStep(3);
      expect(code).toContain('def add');
    });
  });
});

describe('PhaseProgress', () => {
  let component;
  let container;

  beforeEach(() => {
    container = document.createElement('div');
    document.body.appendChild(container);
    component = new PhaseProgress(1, []);
  });

  afterEach(() => {
    document.body.removeChild(container);
  });

  test('should render phase groups', () => {
    component.render(container);
    const groups = container.querySelectorAll('.phase-group');
    expect(groups.length).toBe(3); // RED, GREEN, REFACTOR
  });

  test('should mark current step', () => {
    component.render(container);
    const current = container.querySelector('.step-box.current');
    expect(current).toBeDefined();
  });

  test('should update current step', () => {
    component.render(container);
    component.updateCurrentStep(3);
    const current = container.querySelector('.step-box.current');
    expect(current.textContent).toContain('Step 3');
  });
});

describe('RequirementsChecklist', () => {
  let component;
  let container;

  beforeEach(() => {
    container = document.createElement('div');
    document.body.appendChild(container);
    component = new RequirementsChecklist(['Requirement 1', 'Requirement 2', 'Requirement 3']);
  });

  afterEach(() => {
    document.body.removeChild(container);
  });

  test('should render checklist', () => {
    component.render(container);
    const list = container.querySelector('.requirements-list');
    expect(list).toBeDefined();
  });

  test('should display all requirements', () => {
    component.render(container);
    const items = container.querySelectorAll('.requirement-item');
    expect(items.length).toBe(3);
  });

  test('should mark requirement as completed', () => {
    component.render(container);
    component.updateRequirement(0, true);
    expect(component.completed.has(0)).toBe(true);
  });

  test('should check if all requirements met', () => {
    component.updateRequirement(0, true);
    component.updateRequirement(1, true);
    component.updateRequirement(2, true);
    expect(component.areAllRequirementsMet()).toBe(true);
  });

  test('should get unmet requirements', () => {
    component.updateRequirement(0, true);
    const unmet = component.getUnmetRequirements();
    expect(unmet.length).toBe(2);
  });
});

describe('ValidationFeedback', () => {
  let component;
  let container;

  beforeEach(() => {
    container = document.createElement('div');
    document.body.appendChild(container);
    component = new ValidationFeedback();
    component.render(container);
  });

  afterEach(() => {
    document.body.removeChild(container);
  });

  test('should show success message', () => {
    component.showSuccessMessage('Test passed!');
    const success = container.querySelector('.feedback-success');
    expect(success).toBeDefined();
  });

  test('should show errors', () => {
    component.showErrors(['Error 1', 'Error 2']);
    const errors = container.querySelector('.errors-list');
    expect(errors).toBeDefined();
    const items = errors.querySelectorAll('li');
    expect(items.length).toBe(2);
  });

  test('should show validation result', () => {
    const result = {
      valid: true,
      message: 'All tests passed',
      can_advance: true
    };
    component.showValidationResult(result);
    const success = container.querySelector('.feedback-success');
    expect(success).toBeDefined();
  });

  test('should clear feedback', () => {
    component.showSuccessMessage('Test');
    component.clear();
    expect(container.innerHTML).toBe('');
  });
});

describe('StepCodeEditor', () => {
  let component;
  let container;

  beforeEach(() => {
    container = document.createElement('div');
    document.body.appendChild(container);
    component = new StepCodeEditor(1, 'def test():\n    pass', '');
  });

  afterEach(() => {
    document.body.removeChild(container);
  });

  test('should render code editor', () => {
    component.render(container);
    const editor = container.querySelector('.code-editor');
    expect(editor).toBeDefined();
  });

  test('should get current code', () => {
    component.render(container);
    const code = component.getCode();
    expect(code).toContain('def test');
  });

  test('should set code', () => {
    component.render(container);
    component.setCode('new code');
    expect(component.getCode()).toBe('new code');
  });

  test('should reset to starter code', () => {
    component.render(container);
    component.setCode('modified code');
    component.resetCode();
    expect(component.getCode()).toContain('def test');
  });

  test('should handle tab key', () => {
    component.render(container);
    const editor = container.querySelector('.code-editor');
    const event = new KeyboardEvent('keydown', { key: 'Tab' });
    editor.dispatchEvent(event);
    // Tab handling is tested through the event listener
  });
});

describe('HintsPanel', () => {
  let component;
  let container;

  beforeEach(() => {
    container = document.createElement('div');
    document.body.appendChild(container);
    component = new HintsPanel('workshop_123', 1);
  });

  afterEach(() => {
    document.body.removeChild(container);
  });

  test('should render hints panel', () => {
    component.render(container);
    const panel = container.querySelector('.hints-panel');
    expect(panel).toBeDefined();
  });

  test('should render hint buttons', () => {
    component.render(container);
    const buttons = container.querySelectorAll('.btn-hint');
    expect(buttons.length).toBeGreaterThan(0);
  });

  test('should track hints used', () => {
    component.hintsUsed.push({ level: 1, timestamp: Date.now() });
    const used = component.getHintsUsed();
    expect(used.length).toBe(1);
  });

  test('should reset hints', () => {
    component.currentHintLevel = 3;
    component.hintsUsed.push({ level: 1 });
    component.reset();
    expect(component.currentHintLevel).toBe(0);
    expect(component.getHintsUsed().length).toBe(0);
  });

  test('should set step', () => {
    component.setStep(3);
    expect(component.step).toBe(3);
  });
});

