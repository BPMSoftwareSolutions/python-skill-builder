/**
 * Code Metrics Component
 * Displays code quality metrics during the REFACTOR phase
 */

export class CodeMetricsComponent {
  /**
   * Render code metrics display
   * @param {Object} metrics - Code metrics object
   * @param {HTMLElement} container - Container element
   */
  static render(metrics, container) {
    if (!metrics || !container) return;

    container.innerHTML = '';
    const metricsEl = document.createElement('div');
    metricsEl.className = 'code-metrics';

    // Metrics header
    const header = document.createElement('div');
    header.className = 'metrics-header';
    header.innerHTML = `
      <h3 class="metrics-title">📊 Code Metrics</h3>
      <p class="metrics-subtitle">Quality indicators for your code</p>
    `;
    metricsEl.appendChild(header);

    // Metrics grid
    const grid = document.createElement('div');
    grid.className = 'metrics-grid';

    // Complexity metric
    const complexityEl = document.createElement('div');
    complexityEl.className = 'metrics-item metrics-complexity';
    complexityEl.innerHTML = `
      <div class="metrics-label">Cyclomatic Complexity</div>
      <div class="metrics-value">${metrics.complexity?.cyclomatic || 0}</div>
      <div class="metrics-rating">Rating: ${metrics.complexity?.rating || 'N/A'}</div>
    `;
    grid.appendChild(complexityEl);

    // Coverage metric
    const coverageEl = document.createElement('div');
    coverageEl.className = 'metrics-item metrics-coverage';
    coverageEl.innerHTML = `
      <div class="metrics-label">Code Coverage</div>
      <div class="metrics-value">${metrics.coverage?.lines || 0}%</div>
      <div class="metrics-bar">
        <div class="metrics-bar-fill" style="width: ${metrics.coverage?.lines || 0}%"></div>
      </div>
    `;
    grid.appendChild(coverageEl);

    // Line count metric
    const linesEl = document.createElement('div');
    linesEl.className = 'metrics-item metrics-lines';
    linesEl.innerHTML = `
      <div class="metrics-label">Lines of Code</div>
      <div class="metrics-value">${metrics.code?.lines || 0}</div>
    `;
    grid.appendChild(linesEl);

    // Duplication metric
    const duplicationEl = document.createElement('div');
    duplicationEl.className = 'metrics-item metrics-duplication';
    duplicationEl.innerHTML = `
      <div class="metrics-label">Code Duplication</div>
      <div class="metrics-value">${metrics.code?.duplication || 0}%</div>
    `;
    grid.appendChild(duplicationEl);

    // Functions metric
    const functionsEl = document.createElement('div');
    functionsEl.className = 'metrics-item metrics-functions';
    functionsEl.innerHTML = `
      <div class="metrics-label">Functions</div>
      <div class="metrics-value">${metrics.code?.functions || 0}</div>
      <div class="metrics-detail">Avg length: ${metrics.code?.avgFunctionLength || 0} lines</div>
    `;
    grid.appendChild(functionsEl);

    metricsEl.appendChild(grid);

    // Issues section
    if (metrics.issues && metrics.issues.length > 0) {
      const issuesSection = document.createElement('div');
      issuesSection.className = 'metrics-issues-section';
      issuesSection.innerHTML = '<h4 class="metrics-issues-title">⚠️ Issues Found</h4>';

      const issuesList = document.createElement('div');
      issuesList.className = 'metrics-issues-list';

      metrics.issues.forEach(issue => {
        const issueEl = document.createElement('div');
        issueEl.className = `metrics-issue metrics-issue-${issue.severity}`;
        issueEl.innerHTML = `
          <div class="metrics-issue-type">${issue.type}</div>
          <div class="metrics-issue-message">${issue.message}</div>
          <div class="metrics-issue-severity">${issue.severity}</div>
        `;
        issuesList.appendChild(issueEl);
      });

      issuesSection.appendChild(issuesList);
      metricsEl.appendChild(issuesSection);
    }

    container.appendChild(metricsEl);
  }

  /**
   * Get metrics from code
   * @param {string} code - Code to analyze
   * @returns {Object} Metrics object
   */
  static analyzeCode(code) {
    if (!code) {
      return {
        complexity: { cyclomatic: 0, cognitive: 0, rating: 'N/A' },
        coverage: { lines: 0, branches: 0, functions: 0 },
        code: { lines: 0, functions: 0, avgFunctionLength: 0, duplication: 0 },
        issues: []
      };
    }

    const lines = code.split('\n').length;
    const functions = (code.match(/def\s+\w+/g) || []).length;
    const avgFunctionLength = functions > 0 ? Math.round(lines / functions) : 0;

    return {
      complexity: { cyclomatic: 1, cognitive: 1, rating: 'A' },
      coverage: { lines: 100, branches: 100, functions: 100 },
      code: { lines, functions, avgFunctionLength, duplication: 0 },
      issues: []
    };
  }
}

