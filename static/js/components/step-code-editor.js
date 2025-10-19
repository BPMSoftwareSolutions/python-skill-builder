/**
 * Step Code Editor Component
 * Enhanced code editor with step-specific features
 */

class StepCodeEditor {
  constructor(step = 1, starterCode = '', previousCode = '') {
    this.step = step;
    this.starterCode = starterCode;
    this.previousCode = previousCode;
    this.currentCode = starterCode;
    this.container = null;
    this.editor = null;
    this.onCodeChange = null;
  }

  /**
   * Render the code editor
   * @param {HTMLElement} container - The container to render into
   */
  render(container) {
    this.container = container;
    container.innerHTML = '';

    const wrapper = document.createElement('div');
    wrapper.className = 'step-code-editor';

    // Editor header
    const header = document.createElement('div');
    header.className = 'editor-header';
    header.innerHTML = `
      <h4>💻 Code Editor - Step ${this.step}</h4>
      <div class="editor-actions">
        <button class="btn-sm" onclick="this.parentElement.parentElement.parentElement.resetCode()">🔄 Reset</button>
        <button class="btn-sm" onclick="this.parentElement.parentElement.parentElement.showPreviousCode()">📋 Previous</button>
      </div>
    `;
    wrapper.appendChild(header);

    // Editor area
    const editorArea = document.createElement('div');
    editorArea.className = 'editor-area';

    this.editor = document.createElement('textarea');
    this.editor.className = 'code-editor';
    this.editor.spellcheck = false;
    this.editor.value = this.currentCode;
    this.editor.addEventListener('input', (e) => {
      this.currentCode = e.target.value;
      if (this.onCodeChange) {
        this.onCodeChange(this.currentCode);
      }
    });

    // Handle tab key
    this.editor.addEventListener('keydown', (e) => {
      if (e.key === 'Tab') {
        e.preventDefault();
        const start = this.editor.selectionStart;
        const end = this.editor.selectionEnd;
        this.currentCode = this.currentCode.substring(0, start) + '\t' + this.currentCode.substring(end);
        this.editor.value = this.currentCode;
        this.editor.selectionStart = this.editor.selectionEnd = start + 1;
        if (this.onCodeChange) {
          this.onCodeChange(this.currentCode);
        }
      }
    });

    editorArea.appendChild(this.editor);
    wrapper.appendChild(editorArea);

    // Metrics display
    const metricsArea = document.createElement('div');
    metricsArea.className = 'metrics-area';
    metricsArea.id = 'metrics-display';
    wrapper.appendChild(metricsArea);

    container.appendChild(wrapper);
  }

  /**
   * Get current code
   * @returns {string}
   */
  getCode() {
    return this.currentCode;
  }

  /**
   * Set code
   * @param {string} code - The new code
   */
  setCode(code) {
    this.currentCode = code;
    if (this.editor) {
      this.editor.value = code;
    }
  }

  /**
   * Set starter code
   * @param {string} code - The starter code
   */
  setStarterCode(code) {
    this.starterCode = code;
  }

  /**
   * Reset to starter code
   */
  resetCode() {
    this.setCode(this.starterCode);
  }

  /**
   * Show previous code
   */
  showPreviousCode() {
    if (!this.previousCode) {
      alert('No previous code available');
      return;
    }

    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
      <div class="modal-content">
        <div class="modal-header">
          <h4>Previous Step Code</h4>
          <button class="modal-close" onclick="this.parentElement.parentElement.remove()">×</button>
        </div>
        <div class="modal-body">
          <pre><code>${this.escapeHtml(this.previousCode)}</code></pre>
        </div>
        <div class="modal-footer">
          <button class="btn-primary" onclick="this.parentElement.parentElement.remove()">Close</button>
        </div>
      </div>
    `;
    document.body.appendChild(modal);
  }

  /**
   * Highlight errors
   * @param {Array<Object>} errors - Array of error objects with line and message
   */
  highlightErrors(errors) {
    if (!this.editor) return;

    // Clear previous highlights
    this.editor.classList.remove('has-errors');

    if (errors && errors.length > 0) {
      this.editor.classList.add('has-errors');
      // In a real implementation, you'd use a library like CodeMirror for better highlighting
    }
  }

  /**
   * Show metrics
   * @param {Object} metrics - Metrics object with complexity, coverage, etc.
   */
  showMetrics(metrics) {
    const metricsDisplay = document.getElementById('metrics-display');
    if (!metricsDisplay) return;

    metricsDisplay.innerHTML = '';
    const metricsEl = document.createElement('div');
    metricsEl.className = 'metrics-display';
    metricsEl.innerHTML = `
      <div class="metric-item">
        <span class="metric-label">Complexity:</span>
        <span class="metric-value">${metrics.complexity || 'N/A'}</span>
      </div>
      <div class="metric-item">
        <span class="metric-label">Coverage:</span>
        <span class="metric-value">${metrics.coverage || 'N/A'}%</span>
      </div>
      <div class="metric-item">
        <span class="metric-label">Duplication:</span>
        <span class="metric-value">${metrics.duplication || 'N/A'}%</span>
      </div>
      <div class="metric-item">
        <span class="metric-label">Type Hints:</span>
        <span class="metric-value">${metrics.has_type_hints ? '✓' : '✗'}</span>
      </div>
      <div class="metric-item">
        <span class="metric-label">Docstring:</span>
        <span class="metric-value">${metrics.has_docstring ? '✓' : '✗'}</span>
      </div>
    `;
    metricsDisplay.appendChild(metricsEl);
  }

  /**
   * Set code change callback
   * @param {Function} callback - Callback function
   */
  setOnCodeChange(callback) {
    this.onCodeChange = callback;
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
  module.exports = StepCodeEditor;
}

