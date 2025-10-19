/**
 * TDD Workflow Component
 * Main component that orchestrates the 6-step TDD workflow
 */

class TDDWorkflowComponent {
  constructor(workshopId, workflowId) {
    this.workshopId = workshopId;
    this.workflowId = workflowId;
    this.currentStep = 1;
    this.stepsStatus = [];
    this.codePerStep = {};
    this.api = new WorkflowAPI();
    this.container = null;

    // Sub-components
    this.phaseProgress = null;
    this.checklist = null;
    this.codeEditor = null;
    this.validationFeedback = null;
    this.hintsPanel = null;
  }

  /**
   * Initialize the workflow
   */
  async initialize() {
    try {
      const workflow = await this.api.getWorkflow(this.workshopId, this.workflowId);
      this.currentStep = workflow.current_step;
      this.stepsStatus = workflow.steps_status;
      this.codePerStep = workflow.code_per_step;
    } catch (error) {
      console.error('Failed to initialize workflow:', error);
      throw error;
    }
  }

  /**
   * Render the workflow
   * @param {HTMLElement} container - The container to render into
   */
  render(container) {
    this.container = container;
    container.innerHTML = '';

    const wrapper = document.createElement('div');
    wrapper.className = 'tdd-workflow-container';

    // Phase progress
    const progressContainer = document.createElement('div');
    progressContainer.className = 'workflow-section phase-progress-section';
    this.phaseProgress = new PhaseProgress(this.currentStep, this.stepsStatus);
    this.phaseProgress.render(progressContainer);
    wrapper.appendChild(progressContainer);

    // Main content area
    const contentArea = document.createElement('div');
    contentArea.className = 'workflow-content';

    // Left panel: Requirements checklist
    const leftPanel = document.createElement('div');
    leftPanel.className = 'workflow-panel left-panel';
    const checklistContainer = document.createElement('div');
    checklistContainer.id = 'checklist-container';
    this.checklist = new RequirementsChecklist(this.getRequirementsForStep(this.currentStep));
    this.checklist.render(checklistContainer);
    leftPanel.appendChild(checklistContainer);
    contentArea.appendChild(leftPanel);

    // Center panel: Code editor
    const centerPanel = document.createElement('div');
    centerPanel.className = 'workflow-panel center-panel';
    const editorContainer = document.createElement('div');
    editorContainer.id = 'editor-container';
    const previousCode = this.currentStep > 1 ? this.codePerStep[this.currentStep - 1] : '';
    this.codeEditor = new StepCodeEditor(
      this.currentStep,
      this.getStarterCodeForStep(this.currentStep),
      previousCode
    );
    this.codeEditor.render(editorContainer);
    centerPanel.appendChild(editorContainer);

    // Validation and action buttons
    const actionButtons = document.createElement('div');
    actionButtons.className = 'action-buttons';
    actionButtons.innerHTML = `
      <button class="btn-primary" onclick="window.tddWorkflow.validateStep()">✓ Validate Step</button>
      <button class="btn-secondary" onclick="window.tddWorkflow.getHint()">💡 Get Hint</button>
      <button class="btn-secondary" onclick="window.tddWorkflow.skipStep()">⏭️ Skip Step</button>
      <button class="btn-secondary" onclick="window.tddWorkflow.goBack()">← Go Back</button>
    `;
    centerPanel.appendChild(actionButtons);
    contentArea.appendChild(centerPanel);

    // Right panel: Hints and feedback
    const rightPanel = document.createElement('div');
    rightPanel.className = 'workflow-panel right-panel';

    const hintsContainer = document.createElement('div');
    hintsContainer.id = 'hints-container';
    this.hintsPanel = new HintsPanel(this.workshopId, this.currentStep);
    this.hintsPanel.render(hintsContainer);
    rightPanel.appendChild(hintsContainer);

    const feedbackContainer = document.createElement('div');
    feedbackContainer.id = 'feedback-container';
    this.validationFeedback = new ValidationFeedback();
    this.validationFeedback.render(feedbackContainer);
    rightPanel.appendChild(feedbackContainer);

    contentArea.appendChild(rightPanel);
    wrapper.appendChild(contentArea);

    container.appendChild(wrapper);

    // Store reference for button callbacks
    window.tddWorkflow = this;
  }

  /**
   * Validate current step
   */
  async validateStep() {
    try {
      const code = this.codeEditor.getCode();
      const result = await this.api.validateStep(
        this.workshopId,
        this.workflowId,
        this.currentStep,
        code
      );

      this.validationFeedback.showValidationResult(result);
      this.checklist.autoCheckRequirements(result);

      if (result.valid && result.can_advance) {
        // Show advance button
        this.showAdvanceButton();
      }
    } catch (error) {
      console.error('Validation failed:', error);
      this.validationFeedback.showErrors([error.message]);
    }
  }

  /**
   * Show advance button
   * @private
   */
  showAdvanceButton() {
    const actionButtons = document.querySelector('.action-buttons');
    if (actionButtons && !actionButtons.querySelector('.btn-advance')) {
      const advanceBtn = document.createElement('button');
      advanceBtn.className = 'btn-primary btn-advance';
      advanceBtn.textContent = '→ Advance to Next Step';
      advanceBtn.onclick = () => this.advanceStep();
      actionButtons.appendChild(advanceBtn);
    }
  }

  /**
   * Advance to next step
   */
  async advanceStep() {
    try {
      const result = await this.api.advanceStep(this.workshopId, this.workflowId);
      this.currentStep = result.current_step;
      this.render(this.container);
    } catch (error) {
      console.error('Failed to advance:', error);
      this.validationFeedback.showErrors([error.message]);
    }
  }

  /**
   * Get hint
   */
  async getHint() {
    await this.hintsPanel.showNextHint();
  }

  /**
   * Skip step
   */
  skipStep() {
    if (confirm('Are you sure you want to skip this step?')) {
      this.advanceStep();
    }
  }

  /**
   * Go back to previous step
   */
  async goBack() {
    if (this.currentStep > 1) {
      try {
        const result = await this.api.goBackStep(
          this.workshopId,
          this.workflowId,
          this.currentStep - 1
        );
        this.currentStep = result.current_step;
        this.render(this.container);
      } catch (error) {
        console.error('Failed to go back:', error);
        this.validationFeedback.showErrors([error.message]);
      }
    }
  }

  /**
   * Get requirements for a step
   * @private
   */
  getRequirementsForStep(step) {
    const requirements = {
      1: [
        'Function name starts with test_',
        'At least one assertion present',
        'Valid Python syntax',
        'Test fails when executed'
      ],
      2: ['Test validation complete'],
      3: [
        'Valid Python syntax',
        'Required function exists',
        'Function is callable'
      ],
      4: ['Code passes all tests'],
      5: [
        'Valid Python syntax',
        'Tests still pass',
        'Code quality improved'
      ],
      6: ['Refactoring complete']
    };
    return requirements[step] || [];
  }

  /**
   * Get starter code for a step
   * @private
   */
  getStarterCodeForStep(step) {
    const starterCode = {
      1: 'def test_add():\n    # Write your test here\n    pass',
      2: '# Validation step - no code needed',
      3: 'def add(a, b):\n    # Write your implementation here\n    pass',
      4: '# Validation step - no code needed',
      5: 'def add(a, b):\n    # Refactor your code here\n    pass',
      6: '# Validation step - no code needed'
    };
    return starterCode[step] || '';
  }

  /**
   * Update current step
   * @param {number} step - The new step
   */
  updateCurrentStep(step) {
    this.currentStep = step;
    if (this.container) {
      this.render(this.container);
    }
  }

  /**
   * Save code for step
   * @param {number} step - The step number
   * @param {string} code - The code to save
   */
  saveCodeForStep(step, code) {
    this.codePerStep[step] = code;
  }

  /**
   * Load code for step
   * @param {number} step - The step number
   * @returns {string}
   */
  loadCodeForStep(step) {
    return this.codePerStep[step] || '';
  }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = TDDWorkflowComponent;
}

