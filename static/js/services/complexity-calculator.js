/**
 * Complexity Calculator Service
 * Calculates code complexity metrics
 */

export class ComplexityCalculator {
  /**
   * Calculate cyclomatic complexity
   * @param {string} code - Code to analyze
   * @returns {number} Cyclomatic complexity score
   */
  static calculateCyclomaticComplexity(code) {
    if (!code) return 0;

    let complexity = 1;

    // Count decision points
    const ifMatches = (code.match(/\bif\b/g) || []).length;
    const elifMatches = (code.match(/\belif\b/g) || []).length;
    const forMatches = (code.match(/\bfor\b/g) || []).length;
    const whileMatches = (code.match(/\bwhile\b/g) || []).length;
    const exceptMatches = (code.match(/\bexcept\b/g) || []).length;
    const andMatches = (code.match(/\band\b/g) || []).length;
    const orMatches = (code.match(/\bor\b/g) || []).length;

    complexity += ifMatches + elifMatches + forMatches + whileMatches + exceptMatches;
    complexity += Math.floor((andMatches + orMatches) / 2);

    return complexity;
  }

  /**
   * Get complex functions
   * @param {string} code - Code to analyze
   * @returns {Array} Array of complex functions
   */
  static getComplexFunctions(code) {
    if (!code) return [];

    const functions = [];
    const functionRegex = /def\s+(\w+)\s*\([^)]*\):/g;
    let match;

    while ((match = functionRegex.exec(code)) !== null) {
      const functionName = match[1];
      const startIndex = match.index;
      const endIndex = code.indexOf('\ndef ', startIndex + 1);
      const functionCode = endIndex === -1 
        ? code.substring(startIndex) 
        : code.substring(startIndex, endIndex);

      const complexity = this.calculateCyclomaticComplexity(functionCode);

      if (complexity > 3) {
        functions.push({
          name: functionName,
          complexity,
          startLine: code.substring(0, startIndex).split('\n').length,
          severity: complexity > 10 ? 'high' : complexity > 5 ? 'medium' : 'low'
        });
      }
    }

    return functions;
  }

  /**
   * Suggest simplification strategies
   * @param {Object} data - Data with complexity and function name
   * @returns {Array} Array of suggestions
   */
  static suggestSimplification(data) {
    const suggestions = [];

    if (!data || !data.complexity) {
      return suggestions;
    }

    if (data.complexity > 10) {
      suggestions.push({
        id: 'extract-methods',
        title: 'Extract Methods',
        description: 'Break this function into smaller, focused functions',
        severity: 'high'
      });
    }

    if (data.complexity > 5) {
      suggestions.push({
        id: 'reduce-nesting',
        title: 'Reduce Nesting',
        description: 'Reduce nested if/else statements',
        severity: 'medium'
      });
    }

    if (data.complexity > 3) {
      suggestions.push({
        id: 'use-early-return',
        title: 'Use Early Return',
        description: 'Use early returns to reduce nesting',
        severity: 'low'
      });
    }

    return suggestions;
  }

  /**
   * Get complexity benchmarks
   * @returns {Object} Benchmarks for complexity levels
   */
  static getBenchmarks() {
    return {
      low: { min: 1, max: 3, description: 'Simple and easy to understand' },
      medium: { min: 4, max: 7, description: 'Moderate complexity' },
      high: { min: 8, max: 15, description: 'Complex, consider refactoring' },
      veryHigh: { min: 16, max: Infinity, description: 'Very complex, needs refactoring' }
    };
  }

  /**
   * Get complexity rating
   * @param {number} complexity - Complexity score
   * @returns {string} Rating (A, B, C, D, F)
   */
  static getComplexityRating(complexity) {
    if (complexity <= 3) return 'A';
    if (complexity <= 7) return 'B';
    if (complexity <= 10) return 'C';
    if (complexity <= 15) return 'D';
    return 'F';
  }

  /**
   * Analyze code complexity
   * @param {string} code - Code to analyze
   * @returns {Object} Complexity analysis
   */
  static analyzeComplexity(code) {
    if (!code) {
      return {
        cyclomatic: 0,
        cognitive: 0,
        rating: 'A',
        complexFunctions: [],
        suggestions: []
      };
    }

    const cyclomatic = this.calculateCyclomaticComplexity(code);
    const complexFunctions = this.getComplexFunctions(code);

    return {
      cyclomatic,
      cognitive: Math.ceil(cyclomatic / 2),
      rating: this.getComplexityRating(cyclomatic),
      complexFunctions,
      suggestions: this.suggestSimplification({ complexity: cyclomatic })
    };
  }
}

