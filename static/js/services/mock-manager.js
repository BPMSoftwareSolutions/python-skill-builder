/**
 * Mock Manager Service
 * Manages mock data sets, switching between sets, validation, and persistence
 */

export class MockManager {
  constructor() {
    this.mockSets = {};
    this.currentMockSetId = 'valid';
    this.customMockSets = {};
    this.loadCustomMockSets();
  }

  /**
   * Initialize mock data from workshop configuration
   * @param {Object} workshop - Workshop object containing mock data
   */
  initializeMockData(workshop) {
    if (!workshop || !workshop.mockData) {
      this.mockSets = this.getDefaultMockSets();
      return;
    }

    this.mockSets = workshop.mockData;
    this.currentMockSetId = 'valid'; // Default to valid inputs
  }

  /**
   * Get default mock sets if none provided
   * @returns {Object} Default mock sets
   */
  getDefaultMockSets() {
    return {
      valid: {
        id: 'valid',
        name: 'Valid Inputs',
        description: 'Basic positive numbers and standard cases',
        dataPoints: [
          { inputs: [2, 3], expected: 5 },
          { inputs: [5, 10], expected: 15 },
          { inputs: [0, 0], expected: 0 }
        ]
      },
      edge: {
        id: 'edge',
        name: 'Edge Cases',
        description: 'Boundary conditions and special cases',
        dataPoints: [
          { inputs: [-1, 1], expected: 0 },
          { inputs: [0, -5], expected: -5 },
          { inputs: [Number.MAX_SAFE_INTEGER, 1], expected: Number.MAX_SAFE_INTEGER + 1 }
        ]
      },
      stress: {
        id: 'stress',
        name: 'Stress Tests',
        description: 'Large numbers and performance tests',
        dataPoints: [
          { inputs: [1000000, 2000000], expected: 3000000 },
          { inputs: [999999, 1], expected: 1000000 },
          { inputs: [500000, 500000], expected: 1000000 }
        ]
      }
    };
  }

  /**
   * Get all available mock sets
   * @returns {Object} All mock sets
   */
  getAllMockSets() {
    return { ...this.mockSets, ...this.customMockSets };
  }

  /**
   * Get a specific mock set by ID
   * @param {string} mockSetId - Mock set ID
   * @returns {Object|null} Mock set or null if not found
   */
  getMockSet(mockSetId) {
    return this.mockSets[mockSetId] || this.customMockSets[mockSetId] || null;
  }

  /**
   * Get current mock set
   * @returns {Object|null} Current mock set
   */
  getCurrentMockSet() {
    return this.getMockSet(this.currentMockSetId);
  }

  /**
   * Switch to a different mock set
   * @param {string} mockSetId - Mock set ID to switch to
   * @returns {boolean} True if switch successful
   */
  switchMockSet(mockSetId) {
    if (!this.getMockSet(mockSetId)) {
      console.warn(`Mock set ${mockSetId} not found`);
      return false;
    }
    this.currentMockSetId = mockSetId;
    return true;
  }

  /**
   * Get current mock set ID
   * @returns {string} Current mock set ID
   */
  getCurrentMockSetId() {
    return this.currentMockSetId;
  }

  /**
   * Validate mock data structure
   * @param {Object} mockSet - Mock set to validate
   * @returns {Object} Validation result { valid: boolean, errors: Array }
   */
  validateMockSet(mockSet) {
    const errors = [];

    if (!mockSet) {
      errors.push('Mock set is null or undefined');
      return { valid: false, errors };
    }

    if (!mockSet.id || typeof mockSet.id !== 'string') {
      errors.push('Mock set must have a valid id');
    }

    if (!mockSet.name || typeof mockSet.name !== 'string') {
      errors.push('Mock set must have a valid name');
    }

    if (!Array.isArray(mockSet.dataPoints)) {
      errors.push('Mock set must have dataPoints array');
    } else if (mockSet.dataPoints.length === 0) {
      errors.push('Mock set must have at least one data point');
    } else {
      mockSet.dataPoints.forEach((point, index) => {
        if (!Array.isArray(point.inputs)) {
          errors.push(`Data point ${index} must have inputs array`);
        }
        if (point.expected === undefined) {
          errors.push(`Data point ${index} must have expected value`);
        }
      });
    }

    return { valid: errors.length === 0, errors };
  }

  /**
   * Create a custom mock set
   * @param {Object} mockSet - Mock set to create
   * @returns {Object} Result { success: boolean, error?: string }
   */
  createCustomMockSet(mockSet) {
    const validation = this.validateMockSet(mockSet);
    if (!validation.valid) {
      return { success: false, error: validation.errors.join('; ') };
    }

    this.customMockSets[mockSet.id] = mockSet;
    this.saveCustomMockSets();
    return { success: true };
  }

  /**
   * Delete a custom mock set
   * @param {string} mockSetId - Mock set ID to delete
   * @returns {boolean} True if deleted successfully
   */
  deleteCustomMockSet(mockSetId) {
    if (this.customMockSets[mockSetId]) {
      delete this.customMockSets[mockSetId];
      this.saveCustomMockSets();
      return true;
    }
    return false;
  }

  /**
   * Save custom mock sets to localStorage
   */
  saveCustomMockSets() {
    try {
      localStorage.setItem('customMockSets', JSON.stringify(this.customMockSets));
    } catch (error) {
      console.error('Failed to save custom mock sets:', error);
    }
  }

  /**
   * Load custom mock sets from localStorage
   */
  loadCustomMockSets() {
    try {
      const stored = localStorage.getItem('customMockSets');
      this.customMockSets = stored ? JSON.parse(stored) : {};
    } catch (error) {
      console.error('Failed to load custom mock sets:', error);
      this.customMockSets = {};
    }
  }

  /**
   * Export mock data
   * @param {string} mockSetId - Mock set ID to export
   * @returns {string} JSON string of mock set
   */
  exportMockSet(mockSetId) {
    const mockSet = this.getMockSet(mockSetId);
    if (!mockSet) return null;
    return JSON.stringify(mockSet, null, 2);
  }

  /**
   * Import mock data
   * @param {string} jsonString - JSON string of mock set
   * @returns {Object} Result { success: boolean, error?: string }
   */
  importMockSet(jsonString) {
    try {
      const mockSet = JSON.parse(jsonString);
      return this.createCustomMockSet(mockSet);
    } catch (error) {
      return { success: false, error: `Invalid JSON: ${error.message}` };
    }
  }

  /**
   * Get mock set statistics
   * @param {string} mockSetId - Mock set ID
   * @returns {Object} Statistics object
   */
  getMockSetStats(mockSetId) {
    const mockSet = this.getMockSet(mockSetId);
    if (!mockSet) return null;

    return {
      id: mockSet.id,
      name: mockSet.name,
      dataPointCount: mockSet.dataPoints.length,
      isCustom: !!this.customMockSets[mockSetId]
    };
  }
}

export default new MockManager();

