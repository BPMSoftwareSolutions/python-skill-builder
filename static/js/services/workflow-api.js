/**
 * Workflow API Client
 * Handles all communication with the TDD workflow backend API
 */

class WorkflowAPI {
  constructor(baseUrl = '/api') {
    this.baseUrl = baseUrl;
  }

  /**
   * Start a new TDD workflow for a workshop
   * @param {string} workshopId - The workshop ID
   * @returns {Promise<Object>} - { workflow_id, current_step, steps_status }
   */
  async startWorkflow(workshopId) {
    const response = await fetch(
      `${this.baseUrl}/workshops/${workshopId}/workflow/start`,
      { method: 'POST' }
    );
    const data = await response.json();
    if (!data.ok) throw new Error(data.error);
    return data;
  }

  /**
   * Get current workflow state
   * @param {string} workshopId - The workshop ID
   * @param {string} workflowId - The workflow ID
   * @returns {Promise<Object>} - { current_step, steps_status, code_per_step }
   */
  async getWorkflow(workshopId, workflowId) {
    const response = await fetch(
      `${this.baseUrl}/workshops/${workshopId}/workflow/${workflowId}`
    );
    const data = await response.json();
    if (!data.ok) throw new Error(data.error);
    return data;
  }

  /**
   * Validate current step
   * @param {string} workshopId - The workshop ID
   * @param {string} workflowId - The workflow ID
   * @param {number} step - The step number (1-6)
   * @param {string} code - The code to validate
   * @param {string} testCode - Optional test code for steps 3 and 5
   * @returns {Promise<Object>} - { valid, errors, warnings, can_advance, validation_result }
   */
  async validateStep(workshopId, workflowId, step, code, testCode = '') {
    const response = await fetch(
      `${this.baseUrl}/workshops/${workshopId}/workflow/${workflowId}/validate-step`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ step, code, test_code: testCode })
      }
    );
    const data = await response.json();
    if (!data.ok) throw new Error(data.error);
    return data;
  }

  /**
   * Advance to next step
   * @param {string} workshopId - The workshop ID
   * @param {string} workflowId - The workflow ID
   * @returns {Promise<Object>} - { current_step, step_status }
   */
  async advanceStep(workshopId, workflowId) {
    const response = await fetch(
      `${this.baseUrl}/workshops/${workshopId}/workflow/${workflowId}/advance`,
      { method: 'POST' }
    );
    const data = await response.json();
    if (!data.ok) throw new Error(data.error);
    return data;
  }

  /**
   * Go back to a previous step
   * @param {string} workshopId - The workshop ID
   * @param {string} workflowId - The workflow ID
   * @param {number} targetStep - The target step number
   * @returns {Promise<Object>} - { current_step, step_status }
   */
  async goBackStep(workshopId, workflowId, targetStep) {
    const response = await fetch(
      `${this.baseUrl}/workshops/${workshopId}/workflow/${workflowId}/go-back`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ target_step: targetStep })
      }
    );
    const data = await response.json();
    if (!data.ok) throw new Error(data.error);
    return data;
  }

  /**
   * Get code metrics for current step
   * @param {string} workshopId - The workshop ID
   * @param {string} workflowId - The workflow ID
   * @returns {Promise<Object>} - { complexity, coverage, duplication, has_type_hints, has_docstring }
   */
  async getMetrics(workshopId, workflowId) {
    const response = await fetch(
      `${this.baseUrl}/workshops/${workshopId}/workflow/${workflowId}/metrics`
    );
    const data = await response.json();
    if (!data.ok) throw new Error(data.error);
    return data;
  }

  /**
   * Get hint for a specific step
   * @param {string} workshopId - The workshop ID
   * @param {number} step - The step number
   * @param {number} level - The hint level (1-4)
   * @returns {Promise<Object>} - { hint, level }
   */
  async getHint(workshopId, step, level = 1) {
    const response = await fetch(
      `${this.baseUrl}/workshops/${workshopId}/hints?step=${step}&level=${level}`
    );
    const data = await response.json();
    if (!data.ok) throw new Error(data.error);
    return data;
  }

  /**
   * Get example code for a step
   * @param {string} workshopId - The workshop ID
   * @param {number} step - The step number
   * @returns {Promise<Object>} - { code, explanation }
   */
  async getExample(workshopId, step) {
    const response = await fetch(
      `${this.baseUrl}/workshops/${workshopId}/example?step=${step}`
    );
    const data = await response.json();
    if (!data.ok) throw new Error(data.error);
    return data;
  }

  /**
   * Get solution code for a step
   * @param {string} workshopId - The workshop ID
   * @param {number} step - The step number
   * @returns {Promise<Object>} - { code, explanation }
   */
  async getSolution(workshopId, step) {
    const response = await fetch(
      `${this.baseUrl}/workshops/${workshopId}/solution?step=${step}`
    );
    const data = await response.json();
    if (!data.ok) throw new Error(data.error);
    return data;
  }

  /**
   * Get user achievements
   * @param {string} userId - The user ID
   * @returns {Promise<Object>} - { achievements, total_points }
   */
  async getAchievements(userId) {
    const response = await fetch(`${this.baseUrl}/users/${userId}/achievements`);
    const data = await response.json();
    if (!data.ok) throw new Error(data.error);
    return data;
  }

  /**
   * Get user badges
   * @param {string} userId - The user ID
   * @returns {Promise<Object>} - { badges, showcase }
   */
  async getBadges(userId) {
    const response = await fetch(`${this.baseUrl}/users/${userId}/badges`);
    const data = await response.json();
    if (!data.ok) throw new Error(data.error);
    return data;
  }

  /**
   * Get user statistics
   * @param {string} userId - The user ID
   * @returns {Promise<Object>} - { stats, rank }
   */
  async getStats(userId) {
    const response = await fetch(`${this.baseUrl}/users/${userId}/stats`);
    const data = await response.json();
    if (!data.ok) throw new Error(data.error);
    return data;
  }

  /**
   * Mark workflow as complete
   * @param {string} workflowId - The workflow ID
   * @param {string} userId - The user ID
   * @returns {Promise<Object>} - { achievements_unlocked, updated_stats }
   */
  async completeWorkflow(workflowId, userId) {
    const response = await fetch(
      `${this.baseUrl}/workflows/${workflowId}/complete`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId })
      }
    );
    const data = await response.json();
    if (!data.ok) throw new Error(data.error);
    return data;
  }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = WorkflowAPI;
}

