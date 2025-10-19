/**
 * Requirements Checklist Component
 * Displays step requirements and tracks completion
 */

class RequirementsChecklist {
  constructor(requirements = []) {
    this.requirements = requirements;
    this.completed = new Set();
    this.container = null;
  }

  /**
   * Render the checklist
   * @param {HTMLElement} container - The container to render into
   */
  render(container) {
    this.container = container;
    container.innerHTML = '';

    const wrapper = document.createElement('div');
    wrapper.className = 'requirements-checklist';

    const header = document.createElement('div');
    header.className = 'checklist-header';
    header.innerHTML = `
      <h4>📋 Requirements</h4>
      <span class="progress-text">${this.completed.size}/${this.requirements.length} met</span>
    `;
    wrapper.appendChild(header);

    const list = document.createElement('ul');
    list.className = 'requirements-list';

    this.requirements.forEach((req, index) => {
      const item = document.createElement('li');
      item.className = 'requirement-item';
      if (this.completed.has(index)) {
        item.classList.add('completed');
      }

      const checkbox = document.createElement('input');
      checkbox.type = 'checkbox';
      checkbox.className = 'requirement-checkbox';
      checkbox.checked = this.completed.has(index);
      checkbox.disabled = true;
      item.appendChild(checkbox);

      const label = document.createElement('span');
      label.className = 'requirement-text';
      label.textContent = req;
      item.appendChild(label);

      list.appendChild(item);
    });

    wrapper.appendChild(list);

    // Progress bar
    const progressBar = document.createElement('div');
    progressBar.className = 'requirements-progress-bar';
    const percentage = (this.completed.size / this.requirements.length) * 100;
    progressBar.innerHTML = `
      <div class="progress-fill" style="width: ${percentage}%"></div>
    `;
    wrapper.appendChild(progressBar);

    container.appendChild(wrapper);
  }

  /**
   * Mark a requirement as completed
   * @param {number} index - The requirement index
   */
  updateRequirement(index, completed) {
    if (completed) {
      this.completed.add(index);
    } else {
      this.completed.delete(index);
    }
    if (this.container) {
      this.render(this.container);
    }
  }

  /**
   * Check if all requirements are met
   * @returns {boolean}
   */
  areAllRequirementsMet() {
    return this.completed.size === this.requirements.length;
  }

  /**
   * Get unmet requirements
   * @returns {Array<string>}
   */
  getUnmetRequirements() {
    return this.requirements.filter((_, index) => !this.completed.has(index));
  }

  /**
   * Reset all requirements
   */
  reset() {
    this.completed.clear();
    if (this.container) {
      this.render(this.container);
    }
  }

  /**
   * Set requirements
   * @param {Array<string>} requirements - The new requirements
   */
  setRequirements(requirements) {
    this.requirements = requirements;
    this.completed.clear();
    if (this.container) {
      this.render(this.container);
    }
  }

  /**
   * Auto-check requirements based on validation results
   * @param {Object} validationResult - The validation result from API
   */
  autoCheckRequirements(validationResult) {
    if (!validationResult) return;

    // This would be customized per step
    // For now, we'll check based on errors
    const hasErrors = validationResult.errors && validationResult.errors.length > 0;

    if (!hasErrors) {
      // Mark all as complete if no errors
      for (let i = 0; i < this.requirements.length; i++) {
        this.completed.add(i);
      }
    }

    if (this.container) {
      this.render(this.container);
    }
  }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = RequirementsChecklist;
}

