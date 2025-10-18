/**
 * Test Panel Component
 * Displays test cases with pass/fail indicators, expandable details, and progress tracking
 */

export class TestPanelComponent {
  /**
   * Render test panel with test cases
   * @param {Array} tests - Array of test case objects
   * @param {Object} container - DOM element to render into
   * @returns {void}
   */
  static render(tests, container) {
    if (!container) return;
    
    container.innerHTML = '';
    
    if (!tests || tests.length === 0) {
      container.innerHTML = '<p class="no-tests">No tests available</p>';
      return;
    }

    tests.forEach((test, index) => {
      const testElement = this.createTestElement(test, index);
      container.appendChild(testElement);
    });
  }

  /**
   * Create a single test element
   * @param {Object} test - Test case object
   * @param {number} index - Test index
   * @returns {HTMLElement} Test element
   */
  static createTestElement(test, index) {
    const testDiv = document.createElement('div');
    testDiv.className = `test-case test-${test.status || 'not_run'}`;
    testDiv.dataset.testId = test.id;
    testDiv.dataset.testIndex = index;

    // Test header (clickable to expand)
    const header = document.createElement('div');
    header.className = 'test-header';
    header.innerHTML = `
      <div class="test-status-icon">
        ${this.getStatusIcon(test.status)}
      </div>
      <div class="test-name">${test.name}</div>
      <div class="test-toggle">▼</div>
    `;

    // Test details (initially hidden)
    const details = document.createElement('div');
    details.className = 'test-details hidden';
    details.innerHTML = `
      <div class="test-detail-section">
        <div class="detail-label">Assertion:</div>
        <div class="detail-value assertion-value">${this.escapeHtml(test.assertion || 'N/A')}</div>
      </div>
      <div class="test-detail-section">
        <div class="detail-label">Mock Data:</div>
        <div class="detail-value mock-value">${this.formatMockData(test.mocks)}</div>
      </div>
      <div class="test-detail-section">
        <div class="detail-label">Expected:</div>
        <div class="detail-value expected-value">${this.escapeHtml(JSON.stringify(test.expected))}</div>
      </div>
      <div class="test-detail-section">
        <div class="detail-label">Actual:</div>
        <div class="detail-value actual-value">${test.actual !== null ? this.escapeHtml(JSON.stringify(test.actual)) : '<em>Not run</em>'}</div>
      </div>
      ${test.error ? `
        <div class="test-detail-section error-section">
          <div class="detail-label">Error:</div>
          <div class="detail-value error-value">${this.escapeHtml(test.error)}</div>
        </div>
      ` : ''}
    `;

    // Add click handler to toggle details
    header.addEventListener('click', () => {
      details.classList.toggle('hidden');
      const toggle = header.querySelector('.test-toggle');
      toggle.textContent = details.classList.contains('hidden') ? '▼' : '▲';
    });

    testDiv.appendChild(header);
    testDiv.appendChild(details);

    return testDiv;
  }

  /**
   * Get status icon based on test status
   * @param {string} status - Test status (pass, fail, not_run)
   * @returns {string} HTML icon
   */
  static getStatusIcon(status) {
    switch (status) {
    case 'pass':
      return '<span class="icon-pass">✓</span>';
    case 'fail':
      return '<span class="icon-fail">✗</span>';
    default:
      return '<span class="icon-not-run">○</span>';
    }
  }

  /**
   * Format mock data for display
   * @param {Object} mocks - Mock data object
   * @returns {string} Formatted mock data HTML
   */
  static formatMockData(mocks) {
    if (!mocks) return 'N/A';
    
    if (mocks.inputs) {
      return `inputs: [${mocks.inputs.map(i => JSON.stringify(i)).join(', ')}]`;
    }
    
    return JSON.stringify(mocks);
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
   * Update test status
   * @param {string} testId - Test ID
   * @param {string} status - New status (pass, fail, not_run)
   * @param {Object} result - Test result object
   * @returns {void}
   */
  static updateTestStatus(testId, status, result = {}) {
    const testElement = document.querySelector(`[data-test-id="${testId}"]`);
    if (!testElement) return;

    // Update status class
    testElement.className = `test-case test-${status}`;

    // Update status icon
    const statusIcon = testElement.querySelector('.test-status-icon');
    if (statusIcon) {
      statusIcon.innerHTML = this.getStatusIcon(status);
    }

    // Update actual value if provided
    if (result.actual !== undefined) {
      const actualValue = testElement.querySelector('.actual-value');
      if (actualValue) {
        actualValue.innerHTML = this.escapeHtml(JSON.stringify(result.actual));
      }
    }

    // Update error if provided
    if (result.error) {
      const errorSection = testElement.querySelector('.error-section');
      if (errorSection) {
        errorSection.innerHTML = `
          <div class="detail-label">Error:</div>
          <div class="detail-value error-value">${this.escapeHtml(result.error)}</div>
        `;
      } else {
        const details = testElement.querySelector('.test-details');
        if (details) {
          const newErrorSection = document.createElement('div');
          newErrorSection.className = 'test-detail-section error-section';
          newErrorSection.innerHTML = `
            <div class="detail-label">Error:</div>
            <div class="detail-value error-value">${this.escapeHtml(result.error)}</div>
          `;
          details.appendChild(newErrorSection);
        }
      }
    }
  }

  /**
   * Clear all test statuses
   * @returns {void}
   */
  static clearAllStatuses() {
    const testElements = document.querySelectorAll('.test-case');
    testElements.forEach(element => {
      element.className = 'test-case test-not_run';
      const statusIcon = element.querySelector('.test-status-icon');
      if (statusIcon) {
        statusIcon.innerHTML = this.getStatusIcon('not_run');
      }
      const actualValue = element.querySelector('.actual-value');
      if (actualValue) {
        actualValue.innerHTML = '<em>Not run</em>';
      }
    });
  }
}

export default TestPanelComponent;

