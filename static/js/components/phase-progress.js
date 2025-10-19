/**
 * Phase Progress Component
 * Visualizes progress through the 6 TDD steps
 */

class PhaseProgress {
  constructor(currentStep = 1, stepsStatus = []) {
    this.currentStep = currentStep;
    this.stepsStatus = stepsStatus;
    this.container = null;
  }

  /**
   * Render the phase progress visualization
   * @param {HTMLElement} container - The container to render into
   */
  render(container) {
    this.container = container;
    container.innerHTML = '';

    const wrapper = document.createElement('div');
    wrapper.className = 'phase-progress-wrapper';

    // RED Phase
    const redPhase = this.createPhaseGroup('RED Phase', [
      { step: 1, label: 'Write Test', icon: '✍️' },
      { step: 2, label: 'Validate Test', icon: '✓' }
    ]);
    wrapper.appendChild(redPhase);

    // GREEN Phase
    const greenPhase = this.createPhaseGroup('GREEN Phase', [
      { step: 3, label: 'Write Code', icon: '💻' },
      { step: 4, label: 'Validate Code', icon: '✓' }
    ]);
    wrapper.appendChild(greenPhase);

    // REFACTOR Phase
    const refactorPhase = this.createPhaseGroup('REFACTOR Phase', [
      { step: 5, label: 'Improve Code', icon: '✨' },
      { step: 6, label: 'Validate Improvement', icon: '✓' }
    ]);
    wrapper.appendChild(refactorPhase);

    container.appendChild(wrapper);
  }

  /**
   * Create a phase group with steps
   * @private
   */
  createPhaseGroup(phaseName, steps) {
    const group = document.createElement('div');
    group.className = 'phase-group';

    const title = document.createElement('h4');
    title.className = 'phase-title';
    title.textContent = phaseName;
    group.appendChild(title);

    const stepsContainer = document.createElement('div');
    stepsContainer.className = 'phase-steps';

    steps.forEach((stepInfo, index) => {
      const stepEl = this.createStepElement(stepInfo);
      stepsContainer.appendChild(stepEl);

      // Add arrow between steps (except after last step)
      if (index < steps.length - 1) {
        const arrow = document.createElement('div');
        arrow.className = 'step-arrow';
        arrow.textContent = '→';
        stepsContainer.appendChild(arrow);
      }
    });

    group.appendChild(stepsContainer);
    return group;
  }

  /**
   * Create a single step element
   * @private
   */
  createStepElement(stepInfo) {
    const stepEl = document.createElement('div');
    const status = this.getStepStatus(stepInfo.step);
    
    stepEl.className = `step-box step-${stepInfo.step} status-${status}`;
    if (stepInfo.step === this.currentStep) {
      stepEl.classList.add('current');
    }

    const icon = document.createElement('div');
    icon.className = 'step-icon';
    icon.textContent = stepInfo.icon;
    stepEl.appendChild(icon);

    const label = document.createElement('div');
    label.className = 'step-label';
    label.textContent = stepInfo.label;
    stepEl.appendChild(label);

    const stepNum = document.createElement('div');
    stepNum.className = 'step-number';
    stepNum.textContent = `Step ${stepInfo.step}`;
    stepEl.appendChild(stepNum);

    const statusBadge = document.createElement('div');
    statusBadge.className = `status-badge status-${status}`;
    statusBadge.textContent = this.getStatusText(status);
    stepEl.appendChild(statusBadge);

    return stepEl;
  }

  /**
   * Get status for a step
   * @private
   */
  getStepStatus(step) {
    if (step < this.currentStep) return 'complete';
    if (step === this.currentStep) return 'current';
    return 'locked';
  }

  /**
   * Get status text
   * @private
   */
  getStatusText(status) {
    const texts = {
      complete: '✓ Complete',
      current: '● Current',
      locked: '🔒 Locked'
    };
    return texts[status] || status;
  }

  /**
   * Update current step
   * @param {number} step - The new current step
   */
  updateCurrentStep(step) {
    this.currentStep = step;
    if (this.container) {
      this.render(this.container);
    }
  }

  /**
   * Update step status
   * @param {number} step - The step number
   * @param {string} status - The new status (complete, current, locked)
   */
  updateStepStatus(step, status) {
    if (this.stepsStatus[step - 1]) {
      this.stepsStatus[step - 1].status = status;
    }
    if (this.container) {
      this.render(this.container);
    }
  }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = PhaseProgress;
}

