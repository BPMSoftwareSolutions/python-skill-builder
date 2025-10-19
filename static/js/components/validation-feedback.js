/**
 * Validation Feedback Component
 * Displays validation results and error messages
 */

class ValidationFeedback {
  constructor() {
    this.container = null;
    this.currentResult = null;
  }

  /**
   * Render the feedback component
   * @param {HTMLElement} container - The container to render into
   */
  render(container) {
    this.container = container;
    container.innerHTML = '';
  }

  /**
   * Show validation result
   * @param {Object} result - The validation result
   */
  showValidationResult(result) {
    this.currentResult = result;
    if (!this.container) return;

    this.container.innerHTML = '';

    const wrapper = document.createElement('div');
    wrapper.className = 'validation-feedback';

    if (result.valid) {
      wrapper.appendChild(this.createSuccessMessage(result));
    } else {
      wrapper.appendChild(this.createErrorMessage(result));
    }

    if (result.warnings && result.warnings.length > 0) {
      wrapper.appendChild(this.createWarningsMessage(result.warnings));
    }

    this.container.appendChild(wrapper);
  }

  /**
   * Create success message
   * @private
   */
  createSuccessMessage(result) {
    const div = document.createElement('div');
    div.className = 'feedback-success';
    div.innerHTML = `
      <div class="feedback-icon">✅</div>
      <div class="feedback-content">
        <h4>Validation Passed!</h4>
        <p>${result.message || 'Your code meets all requirements.'}</p>
        ${result.can_advance ? '<p class="advance-hint">You can now advance to the next step.</p>' : ''}
      </div>
    `;
    return div;
  }

  /**
   * Create error message
   * @private
   */
  createErrorMessage(result) {
    const div = document.createElement('div');
    div.className = 'feedback-error';
    div.innerHTML = `
      <div class="feedback-icon">❌</div>
      <div class="feedback-content">
        <h4>Validation Failed</h4>
        ${this.createErrorsList(result.errors)}
      </div>
    `;
    return div;
  }

  /**
   * Create errors list
   * @private
   */
  createErrorsList(errors) {
    if (!errors || errors.length === 0) return '';

    let html = '<ul class="errors-list">';
    errors.forEach(error => {
      html += `<li>${this.escapeHtml(error)}</li>`;
    });
    html += '</ul>';
    return html;
  }

  /**
   * Show errors
   * @param {Array<string>} errors - The error messages
   */
  showErrors(errors) {
    if (!this.container) return;

    this.container.innerHTML = '';
    const wrapper = document.createElement('div');
    wrapper.className = 'validation-feedback feedback-error';

    const icon = document.createElement('div');
    icon.className = 'feedback-icon';
    icon.textContent = '❌';
    wrapper.appendChild(icon);

    const content = document.createElement('div');
    content.className = 'feedback-content';
    content.innerHTML = '<h4>Errors Found</h4>';
    content.appendChild(this.createErrorsListElement(errors));
    wrapper.appendChild(content);

    this.container.appendChild(wrapper);
  }

  /**
   * Create errors list element
   * @private
   */
  createErrorsListElement(errors) {
    const list = document.createElement('ul');
    list.className = 'errors-list';
    errors.forEach(error => {
      const li = document.createElement('li');
      li.textContent = error;
      list.appendChild(li);
    });
    return list;
  }

  /**
   * Show warnings
   * @param {Array<string>} warnings - The warning messages
   */
  showWarnings(warnings) {
    if (!this.container) return;

    const wrapper = document.createElement('div');
    wrapper.className = 'validation-feedback feedback-warning';

    const icon = document.createElement('div');
    icon.className = 'feedback-icon';
    icon.textContent = '⚠️';
    wrapper.appendChild(icon);

    const content = document.createElement('div');
    content.className = 'feedback-content';
    content.innerHTML = '<h4>Warnings</h4>';
    content.appendChild(this.createWarningsListElement(warnings));
    wrapper.appendChild(content);

    this.container.appendChild(wrapper);
  }

  /**
   * Create warnings list element
   * @private
   */
  createWarningsListElement(warnings) {
    const list = document.createElement('ul');
    list.className = 'warnings-list';
    warnings.forEach(warning => {
      const li = document.createElement('li');
      li.textContent = warning;
      list.appendChild(li);
    });
    return list;
  }

  /**
   * Create warnings message
   * @private
   */
  createWarningsMessage(warnings) {
    const div = document.createElement('div');
    div.className = 'feedback-warning';
    div.innerHTML = '<h5>⚠️ Warnings</h5>';
    div.appendChild(this.createWarningsListElement(warnings));
    return div;
  }

  /**
   * Show success message
   * @param {string} message - The success message
   */
  showSuccessMessage(message) {
    if (!this.container) return;

    this.container.innerHTML = '';
    const wrapper = document.createElement('div');
    wrapper.className = 'validation-feedback feedback-success';
    wrapper.innerHTML = `
      <div class="feedback-icon">✅</div>
      <div class="feedback-content">
        <p>${this.escapeHtml(message)}</p>
      </div>
    `;
    this.container.appendChild(wrapper);
  }

  /**
   * Show hint
   * @param {string} hint - The hint text
   */
  showHint(hint) {
    if (!this.container) return;

    const hintEl = document.createElement('div');
    hintEl.className = 'validation-hint';
    hintEl.innerHTML = `
      <div class="hint-icon">💡</div>
      <div class="hint-content">
        <p>${this.escapeHtml(hint)}</p>
      </div>
    `;
    this.container.appendChild(hintEl);
  }

  /**
   * Clear feedback
   */
  clear() {
    if (this.container) {
      this.container.innerHTML = '';
    }
    this.currentResult = null;
  }

  /**
   * Escape HTML
   * @private
   */
  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = ValidationFeedback;
}

