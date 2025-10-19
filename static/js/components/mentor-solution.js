/**
 * Mentor Solution Component
 * Displays mentor solution and comparison with user code
 */

export class MentorSolutionComponent {
  /**
   * Render mentor solution
   * @param {Object} mentorSolution - Mentor solution object
   * @param {string} userCode - User's code
   * @param {HTMLElement} container - Container element
   */
  static render(mentorSolution, userCode, container) {
    if (!mentorSolution || !container) return;

    container.innerHTML = '';
    const solutionEl = document.createElement('div');
    solutionEl.className = 'mentor-solution';

    // Header
    const header = document.createElement('div');
    header.className = 'mentor-header';
    header.innerHTML = `
      <h3 class="mentor-title">👨‍🏫 Mentor Solution</h3>
      <p class="mentor-subtitle">Learn from an expert approach</p>
    `;
    solutionEl.appendChild(header);

    // Comparison section
    const comparison = document.createElement('div');
    comparison.className = 'mentor-comparison';

    // User code section
    const userSection = document.createElement('div');
    userSection.className = 'mentor-code-section mentor-user-code';
    userSection.innerHTML = `
      <div class="mentor-code-label">Your Code</div>
      <div class="mentor-code">
        <pre><code>${this.escapeHtml(userCode || 'No code yet')}</code></pre>
      </div>
    `;
    comparison.appendChild(userSection);

    // Mentor code section
    const mentorSection = document.createElement('div');
    mentorSection.className = 'mentor-code-section mentor-mentor-code';
    mentorSection.innerHTML = `
      <div class="mentor-code-label">Mentor Solution</div>
      <div class="mentor-code">
        <pre><code>${this.escapeHtml(mentorSolution.code || '')}</code></pre>
      </div>
    `;
    comparison.appendChild(mentorSection);

    solutionEl.appendChild(comparison);

    // Differences
    const differences = this.findDifferences(userCode, mentorSolution.code);
    if (differences.length > 0) {
      const diffSection = document.createElement('div');
      diffSection.className = 'mentor-differences';
      diffSection.innerHTML = '<h4 class="mentor-diff-title">Key Differences</h4>';

      const diffList = document.createElement('ul');
      diffList.className = 'mentor-diff-list';

      differences.forEach(diff => {
        const item = document.createElement('li');
        item.className = 'mentor-diff';
        item.textContent = diff;
        diffList.appendChild(item);
      });

      diffSection.appendChild(diffList);
      solutionEl.appendChild(diffSection);
    }

    // Explanation
    if (mentorSolution.explanation) {
      const explanationEl = document.createElement('div');
      explanationEl.className = 'mentor-explanation-section';
      explanationEl.innerHTML = `
        <h4 class="mentor-explanation-title">💡 Explanation</h4>
        <div class="mentor-explanation">${mentorSolution.explanation}</div>
      `;
      solutionEl.appendChild(explanationEl);
    }

    // Metrics comparison
    if (mentorSolution.metrics) {
      const metricsEl = document.createElement('div');
      metricsEl.className = 'mentor-metrics-section';
      metricsEl.innerHTML = '<h4 class="mentor-metrics-title">📊 Metrics</h4>';

      const metricsList = document.createElement('div');
      metricsList.className = 'mentor-metrics';

      Object.entries(mentorSolution.metrics).forEach(([key, value]) => {
        const metric = document.createElement('div');
        metric.className = 'mentor-metric-item';
        metric.innerHTML = `
          <span class="mentor-metric-label">${this.formatLabel(key)}:</span>
          <span class="mentor-metric-value">${value}</span>
        `;
        metricsList.appendChild(metric);
      });

      metricsEl.appendChild(metricsList);
      solutionEl.appendChild(metricsEl);
    }

    container.appendChild(solutionEl);
  }

  /**
   * Find differences between two code snippets
   * @param {string} userCode - User's code
   * @param {string} mentorCode - Mentor's code
   * @returns {Array} Array of differences
   */
  static findDifferences(userCode, mentorCode) {
    const differences = [];

    if (!userCode || !mentorCode) {
      return differences;
    }

    const userLines = userCode.split('\n');
    const mentorLines = mentorCode.split('\n');

    // Check line count
    if (userLines.length !== mentorLines.length) {
      differences.push(
        `Line count: Your code has ${userLines.length} lines, mentor has ${mentorLines.length}`
      );
    }

    // Check for specific patterns
    if (userCode.includes('pass') && !mentorCode.includes('pass')) {
      differences.push('Mentor solution has actual implementation instead of pass');
    }

    if (userCode.length > mentorCode.length * 1.5) {
      differences.push('Your code is significantly longer - consider simplifying');
    }

    if (!userCode.includes('return') && mentorCode.includes('return')) {
      differences.push('Mentor solution uses explicit return statements');
    }

    return differences;
  }

  /**
   * Format label for display
   * @param {string} label - Label to format
   * @returns {string} Formatted label
   */
  static formatLabel(label) {
    return label
      .replace(/([A-Z])/g, ' $1')
      .replace(/^./, str => str.toUpperCase())
      .trim();
  }

  /**
   * Escape HTML special characters
   * @param {string} text - Text to escape
   * @returns {string} Escaped text
   */
  static escapeHtml(text) {
    const map = {
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      '\'': '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
  }
}

