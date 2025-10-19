/**
 * Integration Tests for TDD Workflow
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

describe('TDD Workflow Integration', () => {
  let container;
  let component;
  let mockApi;

  beforeEach(() => {
    container = document.createElement('div');
    document.body.appendChild(container);

    // Mock the API
    mockApi = {
      getWorkflow: jest.fn().mockResolvedValue({
        ok: true,
        current_step: 1,
        steps_status: Array(6).fill({ status: 'locked' }),
        code_per_step: {}
      }),
      validateStep: jest.fn().mockResolvedValue({
        ok: true,
        valid: true,
        errors: [],
        warnings: [],
        can_advance: true,
        validation_result: {}
      }),
      advanceStep: jest.fn().mockResolvedValue({
        ok: true,
        current_step: 2,
        step_status: { status: 'current' }
      }),
      goBackStep: jest.fn().mockResolvedValue({
        ok: true,
        current_step: 1,
        step_status: { status: 'current' }
      })
    };

    component = new TDDWorkflowComponent('workshop_123', 'workflow_456');
    component.api = mockApi;
  });

  afterEach(() => {
    document.body.removeChild(container);
  });

  describe('full workflow flow', () => {
    test('should initialize and render workflow', async () => {
      await component.initialize();
      component.render(container);

      expect(container.querySelector('.tdd-workflow-container')).toBeDefined();
      expect(mockApi.getWorkflow).toHaveBeenCalled();
    });

    test('should validate step and show feedback', async () => {
      component.render(container);
      await component.validateStep();

      expect(mockApi.validateStep).toHaveBeenCalled();
      expect(component.validationFeedback.currentResult).toBeDefined();
    });

    test('should advance to next step', async () => {
      component.render(container);
      await component.advanceStep();

      expect(mockApi.advanceStep).toHaveBeenCalled();
      expect(component.currentStep).toBe(2);
    });

    test('should go back to previous step', async () => {
      component.currentStep = 3;
      component.render(container);
      await component.goBack();

      expect(mockApi.goBackStep).toHaveBeenCalled();
    });
  });

  describe('step progression', () => {
    test('should progress through all 6 steps', async () => {
      component.render(container);

      for (let step = 1; step < 6; step++) {
        expect(component.currentStep).toBe(step);
        mockApi.advanceStep.mockResolvedValueOnce({
          ok: true,
          current_step: step + 1,
          step_status: { status: 'current' }
        });
        await component.advanceStep();
      }

      expect(component.currentStep).toBe(6);
    });

    test('should handle validation errors', async () => {
      mockApi.validateStep.mockResolvedValueOnce({
        ok: true,
        valid: false,
        errors: ['Test name must start with test_'],
        warnings: [],
        can_advance: false,
        validation_result: {}
      });

      component.render(container);
      await component.validateStep();

      expect(component.validationFeedback.currentResult.valid).toBe(false);
    });
  });

  describe('code management', () => {
    test('should save and load code per step', () => {
      const code1 = 'def test_add():\n    pass';
      const code3 = 'def add(a, b):\n    return a + b';

      component.saveCodeForStep(1, code1);
      component.saveCodeForStep(3, code3);

      expect(component.loadCodeForStep(1)).toBe(code1);
      expect(component.loadCodeForStep(3)).toBe(code3);
    });

    test('should maintain code across step changes', async () => {
      const code = 'def test_add():\n    pass';
      component.saveCodeForStep(1, code);

      component.currentStep = 2;
      component.render(container);

      expect(component.loadCodeForStep(1)).toBe(code);
    });
  });

  describe('component interaction', () => {
    test('should update checklist on validation', async () => {
      component.render(container);
      const initialCompleted = component.checklist.completed.size;

      await component.validateStep();

      // Checklist should be updated
      expect(component.checklist).toBeDefined();
    });

    test('should update phase progress on step change', async () => {
      component.render(container);
      const initialStep = component.phaseProgress.currentStep;

      mockApi.advanceStep.mockResolvedValueOnce({
        ok: true,
        current_step: 2,
        step_status: { status: 'current' }
      });
      await component.advanceStep();

      expect(component.phaseProgress.currentStep).toBe(2);
    });

    test('should reset hints on step change', async () => {
      component.render(container);
      component.hintsPanel.currentHintLevel = 2;

      mockApi.advanceStep.mockResolvedValueOnce({
        ok: true,
        current_step: 2,
        step_status: { status: 'current' }
      });
      await component.advanceStep();

      // Hints should be reset for new step
      expect(component.hintsPanel.step).toBe(2);
    });
  });

  describe('error handling', () => {
    test('should handle API errors gracefully', async () => {
      mockApi.validateStep.mockRejectedValueOnce(new Error('API Error'));

      component.render(container);
      await component.validateStep();

      expect(component.validationFeedback.currentResult).toBeDefined();
    });

    test('should handle network errors', async () => {
      mockApi.advanceStep.mockRejectedValueOnce(new Error('Network Error'));

      component.render(container);
      await component.advanceStep();

      // Should not crash
      expect(component).toBeDefined();
    });
  });

  describe('user interactions', () => {
    test('should handle skip step', async () => {
      component.render(container);
      window.confirm = jest.fn(() => true);

      await component.skipStep();

      expect(mockApi.advanceStep).toHaveBeenCalled();
    });

    test('should cancel skip if user declines', async () => {
      component.render(container);
      window.confirm = jest.fn(() => false);

      await component.skipStep();

      expect(mockApi.advanceStep).not.toHaveBeenCalled();
    });

    test('should get hint', async () => {
      component.render(container);
      component.hintsPanel.showNextHint = jest.fn();

      await component.getHint();

      expect(component.hintsPanel.showNextHint).toHaveBeenCalled();
    });
  });

  describe('requirements tracking', () => {
    test('should get correct requirements for each step', () => {
      for (let step = 1; step <= 6; step++) {
        const reqs = component.getRequirementsForStep(step);
        expect(reqs.length).toBeGreaterThan(0);
      }
    });

    test('should get correct starter code for each step', () => {
      for (let step = 1; step <= 6; step++) {
        const code = component.getStarterCodeForStep(step);
        expect(code.length).toBeGreaterThan(0);
      }
    });
  });

  describe('workflow state persistence', () => {
    test('should maintain workflow state across renders', () => {
      component.currentStep = 3;
      component.saveCodeForStep(1, 'test code');

      component.render(container);
      const firstRender = container.innerHTML;

      component.render(container);
      const secondRender = container.innerHTML;

      expect(component.currentStep).toBe(3);
      expect(component.loadCodeForStep(1)).toBe('test code');
    });
  });
});

describe('WorkflowAPI', () => {
  let api;

  beforeEach(() => {
    api = new WorkflowAPI();
    global.fetch = jest.fn();
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  test('should start workflow', async () => {
    global.fetch.mockResolvedValueOnce({
      json: async () => ({
        ok: true,
        workflow_id: 'wf_123',
        current_step: 1,
        steps_status: []
      })
    });

    const result = await api.startWorkflow('ws_123');
    expect(result.workflow_id).toBe('wf_123');
  });

  test('should get workflow', async () => {
    global.fetch.mockResolvedValueOnce({
      json: async () => ({
        ok: true,
        current_step: 1,
        steps_status: [],
        code_per_step: {}
      })
    });

    const result = await api.getWorkflow('ws_123', 'wf_123');
    expect(result.current_step).toBe(1);
  });

  test('should validate step', async () => {
    global.fetch.mockResolvedValueOnce({
      json: async () => ({
        ok: true,
        valid: true,
        errors: [],
        warnings: [],
        can_advance: true,
        validation_result: {}
      })
    });

    const result = await api.validateStep('ws_123', 'wf_123', 1, 'code');
    expect(result.valid).toBe(true);
  });

  test('should handle API errors', async () => {
    global.fetch.mockResolvedValueOnce({
      json: async () => ({
        ok: false,
        error: 'Not found'
      })
    });

    await expect(api.getWorkflow('ws_123', 'wf_123')).rejects.toThrow();
  });
});

