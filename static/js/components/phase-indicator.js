/**
 * Phase Indicator Component
 * Manages TDD phase state (RED, GREEN, REFACTOR) and UI updates
 */

export class PhaseIndicatorComponent {
  constructor() {
    this.currentPhase = 'RED'; // RED, GREEN, or REFACTOR
    this.phases = ['RED', 'GREEN', 'REFACTOR'];
    this.phaseButtons = {};
    this.onPhaseChange = null;
    this.initializeButtons();
  }

  /**
   * Initialize phase buttons from DOM
   */
  initializeButtons() {
    this.phaseButtons = {
      RED: document.getElementById('phase-red-btn'),
      GREEN: document.getElementById('phase-green-btn'),
      REFACTOR: document.getElementById('phase-refactor-btn'),
    };

    // Add click handlers
    Object.entries(this.phaseButtons).forEach(([phase, btn]) => {
      if (btn) {
        btn.addEventListener('click', () => this.setPhase(phase));
      }
    });

    // Set initial phase
    this.setPhase('RED');
  }

  /**
   * Set the current phase
   * @param {string} phase - Phase name (RED, GREEN, REFACTOR)
   */
  setPhase(phase) {
    if (!this.phases.includes(phase)) {
      console.warn(`Invalid phase: ${phase}`);
      return;
    }

    this.currentPhase = phase;
    this.updateUI();

    if (this.onPhaseChange) {
      this.onPhaseChange(phase);
    }
  }

  /**
   * Get the current phase
   * @returns {string} Current phase
   */
  getPhase() {
    return this.currentPhase;
  }

  /**
   * Update UI to reflect current phase
   */
  updateUI() {
    Object.entries(this.phaseButtons).forEach(([phase, btn]) => {
      if (btn) {
        if (phase === this.currentPhase) {
          btn.classList.add('active');
        } else {
          btn.classList.remove('active');
        }
      }
    });
  }

  /**
   * Get phase description
   * @returns {string} Description of current phase
   */
  getPhaseDescription() {
    const descriptions = {
      RED: 'Tests are failing - write code to make them pass',
      GREEN: 'Tests are passing - code is working correctly',
      REFACTOR: 'Improve code quality while keeping tests passing',
    };
    return descriptions[this.currentPhase] || '';
  }

  /**
   * Get phase color
   * @returns {string} CSS color for current phase
   */
  getPhaseColor() {
    const colors = {
      RED: '#ef4444',      /* red-500 */
      GREEN: '#22c55e',    /* green-500 */
      REFACTOR: '#3b82f6', /* blue-500 */
    };
    return colors[this.currentPhase] || '#3b82f6';
  }

  /**
   * Get phase emoji
   * @returns {string} Emoji for current phase
   */
  getPhaseEmoji() {
    const emojis = {
      RED: '🔴',
      GREEN: '🟢',
      REFACTOR: '🔵',
    };
    return emojis[this.currentPhase] || '🔴';
  }

  /**
   * Check if in RED phase
   * @returns {boolean} True if in RED phase
   */
  isRed() {
    return this.currentPhase === 'RED';
  }

  /**
   * Check if in GREEN phase
   * @returns {boolean} True if in GREEN phase
   */
  isGreen() {
    return this.currentPhase === 'GREEN';
  }

  /**
   * Check if in REFACTOR phase
   * @returns {boolean} True if in REFACTOR phase
   */
  isRefactor() {
    return this.currentPhase === 'REFACTOR';
  }

  /**
   * Register callback for phase changes
   * @param {Function} callback - Function to call when phase changes
   */
  onPhaseChangeCallback(callback) {
    this.onPhaseChange = callback;
  }

  /**
   * Get all phases
   * @returns {Array} Array of phase names
   */
  getPhases() {
    return [...this.phases];
  }

  /**
   * Get next phase in sequence
   * @returns {string} Next phase
   */
  getNextPhase() {
    const currentIndex = this.phases.indexOf(this.currentPhase);
    const nextIndex = (currentIndex + 1) % this.phases.length;
    return this.phases[nextIndex];
  }

  /**
   * Get previous phase in sequence
   * @returns {string} Previous phase
   */
  getPreviousPhase() {
    const currentIndex = this.phases.indexOf(this.currentPhase);
    const prevIndex = (currentIndex - 1 + this.phases.length) % this.phases.length;
    return this.phases[prevIndex];
  }

  /**
   * Advance to next phase
   */
  nextPhase() {
    this.setPhase(this.getNextPhase());
  }

  /**
   * Go to previous phase
   */
  previousPhase() {
    this.setPhase(this.getPreviousPhase());
  }

  /**
   * Get phase-specific guidance
   * @param {string} phase - Phase name
   * @returns {string} Guidance text for the phase
   */
  getPhaseGuidance(phase) {
    const guidance = {
      RED: '🔴 RED Phase: Understand the requirements by reading the failing tests. What do they expect?',
      GREEN: '🟢 GREEN Phase: Write the simplest code to make all tests pass. Focus on functionality, not perfection.',
      REFACTOR: '🔵 REFACTOR Phase: Improve your code while keeping all tests green. Focus on clarity and efficiency.'
    };
    return guidance[phase] || '';
  }

  /**
   * Get phase progression
   * @returns {Array} Array of phases in order
   */
  getPhaseProgression() {
    return [...this.phases];
  }
}

export default PhaseIndicatorComponent;

