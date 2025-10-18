/**
 * Coverage Analyzer Service
 * Analyzes code coverage from test results
 */

export class CoverageAnalyzer {
  static coverageTrend = [];

  /**
   * Calculate coverage percentage
   * @param {Object} data - Coverage data with totalLines and coveredLines
   * @returns {number} Coverage percentage
   */
  static calculateCoverage(data) {
    if (!data || !data.totalLines || data.totalLines === 0) {
      return 0;
    }
    return Math.round((data.coveredLines / data.totalLines) * 100);
  }

  /**
   * Get uncovered lines
   * @param {Object} data - Coverage data
   * @returns {Array} Array of uncovered line numbers
   */
  static getUncoveredLines(data) {
    if (!data || !data.uncoveredLineNumbers) {
      return [];
    }
    return data.uncoveredLineNumbers;
  }

  /**
   * Suggest coverage improvements
   * @param {Object} data - Coverage data with coverage percentage and uncovered lines
   * @returns {Array} Array of improvement suggestions
   */
  static suggestImprovements(data) {
    const suggestions = [];

    if (!data) {
      return suggestions;
    }

    if (data.coverage < 80) {
      suggestions.push({
        id: 'increase-coverage',
        title: 'Increase Test Coverage',
        description: 'Your code coverage is below 80%. Consider adding more tests.',
        severity: 'high',
        suggestion: 'Write tests for uncovered lines'
      });
    }

    if (data.coverage < 90) {
      suggestions.push({
        id: 'improve-coverage',
        title: 'Improve Test Coverage',
        description: 'Your code coverage is below 90%. Add tests for edge cases.',
        severity: 'medium',
        suggestion: 'Focus on edge cases and error conditions'
      });
    }

    if (data.uncoveredLines && data.uncoveredLines.length > 0) {
      suggestions.push({
        id: 'test-uncovered',
        title: 'Test Uncovered Lines',
        description: `You have ${data.uncoveredLines.length} uncovered lines.`,
        severity: 'medium',
        suggestion: 'Add tests for these specific lines'
      });
    }

    return suggestions;
  }

  /**
   * Record coverage for trend tracking
   * @param {number} coverage - Coverage percentage
   */
  static recordCoverage(coverage) {
    this.coverageTrend.push(coverage);
  }

  /**
   * Get coverage trend
   * @returns {Array} Array of coverage percentages over time
   */
  static getTrend() {
    return this.coverageTrend;
  }

  /**
   * Clear coverage trend
   */
  static clearTrend() {
    this.coverageTrend = [];
  }

  /**
   * Get coverage trend direction
   * @returns {string} 'improving', 'declining', or 'stable'
   */
  static getTrendDirection() {
    if (this.coverageTrend.length < 2) {
      return 'stable';
    }

    const recent = this.coverageTrend.slice(-3);
    const first = recent[0];
    const last = recent[recent.length - 1];

    if (last > first) {
      return 'improving';
    } else if (last < first) {
      return 'declining';
    }
    return 'stable';
  }

  /**
   * Get coverage metrics summary
   * @param {Object} data - Coverage data
   * @returns {Object} Summary object
   */
  static getSummary(data) {
    if (!data) {
      return {
        coverage: 0,
        uncoveredLines: 0,
        trend: 'stable'
      };
    }

    return {
      coverage: this.calculateCoverage(data),
      uncoveredLines: data.uncoveredLineNumbers ? data.uncoveredLineNumbers.length : 0,
      trend: this.getTrendDirection()
    };
  }
}

