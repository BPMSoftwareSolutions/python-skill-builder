/**
 * Test Progress Component
 * Renders progress bar and calculates pass/fail counts
 */

export class TestProgressComponent {
  /**
   * Calculate test statistics
   * @param {Array} tests - Array of test objects
   * @returns {Object} Statistics object with counts and percentages
   */
  static calculateStats(tests) {
    if (!tests || tests.length === 0) {
      return {
        total: 0,
        passed: 0,
        failed: 0,
        notRun: 0,
        passPercentage: 0,
        failPercentage: 0,
        notRunPercentage: 100
      };
    }

    const total = tests.length;
    const passed = tests.filter(t => t.status === 'pass').length;
    const failed = tests.filter(t => t.status === 'fail').length;
    const notRun = tests.filter(t => t.status === 'not_run' || !t.status).length;

    const passPercentage = total > 0 ? Math.round((passed / total) * 100) : 0;
    const failPercentage = total > 0 ? Math.round((failed / total) * 100) : 0;
    const notRunPercentage = total > 0 ? Math.round((notRun / total) * 100) : 0;

    return {
      total,
      passed,
      failed,
      notRun,
      passPercentage,
      failPercentage,
      notRunPercentage
    };
  }

  /**
   * Render progress bar
   * @param {Array} tests - Array of test objects
   * @param {HTMLElement} container - Container element
   * @returns {void}
   */
  static renderProgressBar(tests, container) {
    if (!container) return;

    const stats = this.calculateStats(tests);
    
    container.innerHTML = `
      <div class="progress-container">
        <div class="progress-header">
          <span class="progress-label">Test Progress</span>
          <span class="progress-count">${stats.passed}/${stats.total}</span>
        </div>
        <div class="progress-bar-wrapper">
          <div class="progress-bar">
            ${stats.passed > 0 ? `<div class="progress-segment progress-pass" style="width: ${stats.passPercentage}%"></div>` : ''}
            ${stats.failed > 0 ? `<div class="progress-segment progress-fail" style="width: ${stats.failPercentage}%"></div>` : ''}
            ${stats.notRun > 0 ? `<div class="progress-segment progress-not-run" style="width: ${stats.notRunPercentage}%"></div>` : ''}
          </div>
        </div>
        <div class="progress-stats">
          <div class="stat-item stat-pass">
            <span class="stat-icon">✓</span>
            <span class="stat-label">Passed:</span>
            <span class="stat-value">${stats.passed}</span>
          </div>
          <div class="stat-item stat-fail">
            <span class="stat-icon">✗</span>
            <span class="stat-label">Failed:</span>
            <span class="stat-value">${stats.failed}</span>
          </div>
          <div class="stat-item stat-not-run">
            <span class="stat-icon">○</span>
            <span class="stat-label">Not Run:</span>
            <span class="stat-value">${stats.notRun}</span>
          </div>
        </div>
      </div>
    `;
  }

  /**
   * Update progress bar
   * @param {Array} tests - Array of test objects
   * @returns {void}
   */
  static updateProgressBar(tests) {
    const container = document.getElementById('test-progress');
    if (container) {
      this.renderProgressBar(tests, container);
    }
  }

  /**
   * Render progress summary
   * @param {Array} tests - Array of test objects
   * @returns {string} HTML summary
   */
  static renderSummary(tests) {
    const stats = this.calculateStats(tests);
    
    let summary = `${stats.passed}/${stats.total} tests passing`;
    
    if (stats.passPercentage === 100) {
      summary += ' ✓ All tests passing!';
    } else if (stats.passPercentage > 0) {
      summary += ` (${stats.passPercentage}%)`;
    }
    
    return summary;
  }

  /**
   * Get progress status
   * @param {Array} tests - Array of test objects
   * @returns {string} Status: 'all_pass', 'partial', 'all_fail', 'not_run'
   */
  static getProgressStatus(tests) {
    const stats = this.calculateStats(tests);
    
    if (stats.total === 0) return 'not_run';
    if (stats.passed === stats.total) return 'all_pass';
    if (stats.passed === 0) return 'all_fail';
    return 'partial';
  }

  /**
   * Get progress color
   * @param {Array} tests - Array of test objects
   * @returns {string} CSS color class
   */
  static getProgressColor(tests) {
    const status = this.getProgressStatus(tests);
    
    switch (status) {
    case 'all_pass':
      return 'progress-success';
    case 'all_fail':
      return 'progress-error';
    case 'partial':
      return 'progress-warning';
    default:
      return 'progress-neutral';
    }
  }

  /**
   * Render progress indicator
   * @param {Array} tests - Array of test objects
   * @returns {HTMLElement} Progress indicator element
   */
  static createProgressIndicator(tests) {
    const div = document.createElement('div');
    const stats = this.calculateStats(tests);
    const status = this.getProgressStatus(tests);
    const color = this.getProgressColor(tests);
    
    div.className = `progress-indicator ${color}`;
    div.innerHTML = `
      <div class="indicator-content">
        <span class="indicator-text">${stats.passed}/${stats.total}</span>
        <span class="indicator-status">${status}</span>
      </div>
    `;
    
    return div;
  }
}

export default TestProgressComponent;

