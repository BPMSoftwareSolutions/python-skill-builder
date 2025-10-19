/**
 * Refactor Guide Component
 * Displays refactoring suggestions and code quality issues
 */

export class RefactorGuideComponent {
  /**
   * Render refactor guide
   * @param {Array} suggestions - Array of refactor suggestions
   * @param {HTMLElement} container - Container element
   */
  static render(suggestions, container) {
    if (!suggestions || !container) return;

    container.innerHTML = '';
    const guideEl = document.createElement('div');
    guideEl.className = 'refactor-guide';

    // Header
    const header = document.createElement('div');
    header.className = 'refactor-header';
    header.innerHTML = `
      <h3 class="refactor-title">🔧 Refactor Guide</h3>
      <p class="refactor-subtitle">Suggestions to improve your code</p>
    `;
    guideEl.appendChild(header);

    // Suggestions list
    const list = document.createElement('div');
    list.className = 'refactor-suggestions-list';

    suggestions.forEach((suggestion, index) => {
      const item = document.createElement('div');
      item.className = `refactor-suggestion refactor-suggestion-${suggestion.severity}`;
      item.id = `refactor-${index}`;

      const header = document.createElement('div');
      header.className = 'refactor-suggestion-header';
      header.innerHTML = `
        <div class="refactor-suggestion-title">${suggestion.title}</div>
        <div class="refactor-severity refactor-severity-${suggestion.severity}">
          ${suggestion.severity}
        </div>
      `;
      item.appendChild(header);

      const content = document.createElement('div');
      content.className = 'refactor-suggestion-content';

      // Description
      const desc = document.createElement('div');
      desc.className = 'refactor-issue';
      desc.innerHTML = `<p>${suggestion.description}</p>`;
      content.appendChild(desc);

      // Suggestion
      const sug = document.createElement('div');
      sug.className = 'refactor-recommendation';
      sug.innerHTML = `
        <strong>Suggestion:</strong>
        <p>${suggestion.suggestion}</p>
      `;
      content.appendChild(sug);

      // Example
      if (suggestion.example) {
        const example = document.createElement('div');
        example.className = 'refactor-example';
        example.innerHTML = `
          <strong>Example:</strong>
          <pre><code>${this.escapeHtml(suggestion.example)}</code></pre>
        `;
        content.appendChild(example);
      }

      item.appendChild(content);
      list.appendChild(item);
    });

    guideEl.appendChild(list);
    container.appendChild(guideEl);
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

  /**
   * Generate refactor suggestions from code
   * @param {string} code - Code to analyze
   * @returns {Array} Array of suggestions
   */
  static generateSuggestions(code) {
    if (!code) return [];

    const suggestions = [];

    // Check for long functions
    const functions = code.match(/def\s+\w+\s*\([^)]*\):[^]*?(?=\ndef|\Z)/g) || [];
    functions.forEach(func => {
      const lines = func.split('\n').length;
      if (lines > 20) {
        suggestions.push({
          id: 'long-function',
          title: 'Extract Function',
          description: 'This function is too long and should be broken into smaller functions',
          severity: 'medium',
          suggestion: 'Extract related logic into separate functions',
          example: 'def helper_function():\n    # extracted logic'
        });
      }
    });

    // Check for nested if statements
    const nestedIfs = (code.match(/if.*:\s*if/g) || []).length;
    if (nestedIfs > 0) {
      suggestions.push({
        id: 'nested-conditions',
        title: 'Reduce Nesting',
        description: 'Nested if statements reduce readability',
        severity: 'low',
        suggestion: 'Use early returns or combine conditions',
        example: 'if not condition:\n    return\n# rest of logic'
      });
    }

    // Check for code duplication
    const lines = code.split('\n');
    const lineMap = {};
    lines.forEach(line => {
      if (line.trim().length > 10) {
        lineMap[line] = (lineMap[line] || 0) + 1;
      }
    });

    const duplicates = Object.values(lineMap).filter(count => count > 1).length;
    if (duplicates > 0) {
      suggestions.push({
        id: 'duplication',
        title: 'Remove Duplication',
        description: 'You have repeated code that should be extracted',
        severity: 'low',
        suggestion: 'Create a helper function for repeated logic',
        example: 'def process_data(data):\n    # shared logic'
      });
    }

    return suggestions;
  }

  /**
   * Get severity color
   * @param {string} severity - Severity level
   * @returns {string} Color code
   */
  static getSeverityColor(severity) {
    const colors = {
      high: '#ef4444',
      medium: '#f59e0b',
      low: '#3b82f6'
    };
    return colors[severity] || '#6b7280';
  }
}

