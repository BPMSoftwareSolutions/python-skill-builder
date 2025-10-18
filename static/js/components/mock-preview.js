/**
 * Mock Preview Component
 * Displays current mock data in readable format
 */

export class MockPreviewComponent {
  /**
   * Render mock data preview
   * @param {Object} mockSet - Mock set to display
   * @param {HTMLElement} container - Container element
   */
  static render(mockSet, container) {
    if (!container) return;

    container.innerHTML = '';

    if (!mockSet || !mockSet.dataPoints || mockSet.dataPoints.length === 0) {
      container.innerHTML = '<p class="no-mock-data">No mock data available</p>';
      return;
    }

    // Create preview wrapper
    const previewWrapper = document.createElement('div');
    previewWrapper.className = 'mock-preview-wrapper';

    // Create header with mock set info
    const header = document.createElement('div');
    header.className = 'mock-preview-header';
    header.innerHTML = `
      <div class="mock-preview-title">${this.escapeHtml(mockSet.name)}</div>
      <div class="mock-preview-count">${mockSet.dataPoints.length} test cases</div>
    `;
    previewWrapper.appendChild(header);

    // Create data points list
    const dataPointsList = document.createElement('div');
    dataPointsList.className = 'mock-preview-list';

    mockSet.dataPoints.forEach((dataPoint, index) => {
      const dataPointElement = this.createDataPointElement(dataPoint, index);
      dataPointsList.appendChild(dataPointElement);
    });

    previewWrapper.appendChild(dataPointsList);
    container.appendChild(previewWrapper);
  }

  /**
   * Create a single data point element
   * @param {Object} dataPoint - Data point object
   * @param {number} index - Data point index
   * @returns {HTMLElement} Data point element
   */
  static createDataPointElement(dataPoint, index) {
    const dataPointDiv = document.createElement('div');
    dataPointDiv.className = 'mock-preview-item';
    dataPointDiv.dataset.pointIndex = index;

    const header = document.createElement('div');
    header.className = 'mock-preview-item-header';
    header.innerHTML = `
      <span class="mock-preview-item-number">Test Case ${index + 1}</span>
      <span class="mock-preview-item-toggle">▼</span>
    `;

    const details = document.createElement('div');
    details.className = 'mock-preview-item-details hidden';

    // Format inputs
    const inputsDiv = document.createElement('div');
    inputsDiv.className = 'mock-preview-item-section';
    inputsDiv.innerHTML = `
      <div class="mock-preview-item-label">Inputs:</div>
      <div class="mock-preview-item-value inputs-value">
        ${this.formatInputs(dataPoint.inputs)}
      </div>
    `;

    // Format expected output
    const expectedDiv = document.createElement('div');
    expectedDiv.className = 'mock-preview-item-section';
    expectedDiv.innerHTML = `
      <div class="mock-preview-item-label">Expected Output:</div>
      <div class="mock-preview-item-value expected-value">
        ${this.escapeHtml(JSON.stringify(dataPoint.expected))}
      </div>
    `;

    details.appendChild(inputsDiv);
    details.appendChild(expectedDiv);

    // Add click handler to toggle details
    header.addEventListener('click', () => {
      details.classList.toggle('hidden');
      const toggle = header.querySelector('.mock-preview-item-toggle');
      toggle.textContent = details.classList.contains('hidden') ? '▼' : '▲';
    });

    dataPointDiv.appendChild(header);
    dataPointDiv.appendChild(details);

    return dataPointDiv;
  }

  /**
   * Format inputs for display
   * @param {Array} inputs - Input array
   * @returns {string} Formatted inputs HTML
   */
  static formatInputs(inputs) {
    if (!Array.isArray(inputs)) {
      return this.escapeHtml(JSON.stringify(inputs));
    }

    return inputs
      .map((input) => {
        if (typeof input === 'string') {
          return `<span class="input-string">"${this.escapeHtml(input)}"</span>`;
        } else if (typeof input === 'number') {
          return `<span class="input-number">${input}</span>`;
        } else if (typeof input === 'boolean') {
          return `<span class="input-boolean">${input}</span>`;
        } else if (input === null) {
          return '<span class="input-null">null</span>';
        } else {
          return `<span class="input-object">${this.escapeHtml(JSON.stringify(input))}</span>`;
        }
      })
      .join(', ');
  }

  /**
   * Escape HTML special characters
   * @param {string} text - Text to escape
   * @returns {string} Escaped text
   */
  static escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  /**
   * Update preview with new mock set
   * @param {Object} mockSet - New mock set
   * @param {HTMLElement} container - Container element
   */
  static update(mockSet, container) {
    this.render(mockSet, container);
  }
}

export default MockPreviewComponent;

