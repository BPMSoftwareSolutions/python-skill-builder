/**
 * Assertion Display Component
 * Parses and formats assertion statements with expected vs actual values
 */

export class AssertionDisplayComponent {
  /**
   * Parse assertion statement
   * @param {string} assertion - Assertion statement (e.g., "assertEqual(add(2, 3), 5)")
   * @returns {Object} Parsed assertion object
   */
  static parseAssertion(assertion) {
    if (!assertion) {
      return { type: 'unknown', raw: assertion };
    }

    // Match common assertion patterns
    const patterns = {
      assertEqual: /assertEqual\s*\(\s*(.+?)\s*,\s*(.+?)\s*\)/,
      assertNotEqual: /assertNotEqual\s*\(\s*(.+?)\s*,\s*(.+?)\s*\)/,
      assertTrue: /assertTrue\s*\(\s*(.+?)\s*\)/,
      assertFalse: /assertFalse\s*\(\s*(.+?)\s*\)/,
      assertAlmostEqual: /assertAlmostEqual\s*\(\s*(.+?)\s*,\s*(.+?)\s*(?:,\s*(.+?))?\s*\)/,
      assertRaises: /assertRaises\s*\(\s*(.+?)\s*,\s*(.+?)\s*\)/,
      assertIn: /assertIn\s*\(\s*(.+?)\s*,\s*(.+?)\s*\)/,
      assertIsNone: /assertIsNone\s*\(\s*(.+?)\s*\)/,
      assertIsNotNone: /assertIsNotNone\s*\(\s*(.+?)\s*\)/
    };

    for (const [type, pattern] of Object.entries(patterns)) {
      const match = assertion.match(pattern);
      if (match) {
        return {
          type,
          raw: assertion,
          groups: match.slice(1)
        };
      }
    }

    return { type: 'unknown', raw: assertion };
  }

  /**
   * Format assertion for display
   * @param {string} assertion - Assertion statement
   * @param {*} expected - Expected value
   * @param {*} actual - Actual value
   * @returns {string} Formatted HTML
   */
  static formatAssertion(assertion, expected, actual) {
    const parsed = this.parseAssertion(assertion);
    
    let html = '<div class="assertion-display">';
    html += `<div class="assertion-type">${parsed.type}</div>`;
    html += `<div class="assertion-raw">${this.escapeHtml(assertion)}</div>`;
    
    if (expected !== undefined) {
      html += '<div class="assertion-comparison">';
      html += '<div class="comparison-item">';
      html += '<span class="comparison-label">Expected:</span>';
      html += `<span class="comparison-value">${this.formatValue(expected)}</span>`;
      html += '</div>';
      
      if (actual !== undefined) {
        html += '<div class="comparison-item">';
        html += '<span class="comparison-label">Actual:</span>';
        html += `<span class="comparison-value">${this.formatValue(actual)}</span>`;
        html += '</div>';
      }
      html += '</div>';
    }
    
    html += '</div>';
    return html;
  }

  /**
   * Format value for display
   * @param {*} value - Value to format
   * @returns {string} Formatted value
   */
  static formatValue(value) {
    if (value === null) return '<em>null</em>';
    if (value === undefined) return '<em>undefined</em>';
    if (typeof value === 'string') return `"${this.escapeHtml(value)}"`;
    if (typeof value === 'boolean') return `<strong>${value}</strong>`;
    if (typeof value === 'number') return `<strong>${value}</strong>`;
    if (Array.isArray(value)) {
      return `[${value.map(v => this.formatValue(v)).join(', ')}]`;
    }
    if (typeof value === 'object') {
      return this.escapeHtml(JSON.stringify(value));
    }
    return this.escapeHtml(String(value));
  }

  /**
   * Highlight differences between expected and actual
   * @param {*} expected - Expected value
   * @param {*} actual - Actual value
   * @returns {string} HTML with highlighted differences
   */
  static highlightDifferences(expected, actual) {
    if (typeof expected !== typeof actual) {
      return `
        <div class="difference-highlight">
          <div class="diff-item">
            <span class="diff-label">Type mismatch:</span>
            <span class="diff-expected">Expected ${typeof expected}</span>
            <span class="diff-actual">Got ${typeof actual}</span>
          </div>
        </div>
      `;
    }

    if (typeof expected === 'string' || typeof expected === 'number') {
      if (expected !== actual) {
        return `
          <div class="difference-highlight">
            <div class="diff-item">
              <span class="diff-label">Value mismatch:</span>
              <span class="diff-expected">${this.formatValue(expected)}</span>
              <span class="diff-actual">${this.formatValue(actual)}</span>
            </div>
          </div>
        `;
      }
    }

    if (Array.isArray(expected) && Array.isArray(actual)) {
      if (expected.length !== actual.length) {
        return `
          <div class="difference-highlight">
            <div class="diff-item">
              <span class="diff-label">Length mismatch:</span>
              <span class="diff-expected">Expected length ${expected.length}</span>
              <span class="diff-actual">Got length ${actual.length}</span>
            </div>
          </div>
        `;
      }
    }

    return '';
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
   * Create assertion display element
   * @param {Object} test - Test object
   * @returns {HTMLElement} Assertion display element
   */
  static createAssertionElement(test) {
    const div = document.createElement('div');
    div.className = 'assertion-display-element';
    
    div.innerHTML = `
      <div class="assertion-header">
        <span class="assertion-type-badge">${test.assertion ? 'Assertion' : 'N/A'}</span>
      </div>
      <div class="assertion-content">
        ${this.formatAssertion(test.assertion, test.expected, test.actual)}
        ${test.actual !== undefined && test.expected !== undefined ? this.highlightDifferences(test.expected, test.actual) : ''}
      </div>
    `;
    
    return div;
  }
}

export default AssertionDisplayComponent;

