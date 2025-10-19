/**
 * Hints Panel Component
 * Progressive hint reveals with example and solution display
 */

class HintsPanel {
  constructor(workshopId, step = 1) {
    this.workshopId = workshopId;
    this.step = step;
    this.currentHintLevel = 0;
    this.hints = [];
    this.container = null;
    this.api = new WorkflowAPI();
    this.hintsUsed = [];
  }

  /**
   * Render the hints panel
   * @param {HTMLElement} container - The container to render into
   */
  render(container) {
    this.container = container;
    container.innerHTML = '';

    const wrapper = document.createElement('div');
    wrapper.className = 'hints-panel';

    const header = document.createElement('div');
    header.className = 'hints-header';
    header.innerHTML = '<h4>💡 Hints & Help</h4>';
    wrapper.appendChild(header);

    const content = document.createElement('div');
    content.className = 'hints-content';

    // Hint buttons
    const buttonGroup = document.createElement('div');
    buttonGroup.className = 'hint-buttons';

    const getHintBtn = document.createElement('button');
    getHintBtn.className = 'btn-hint';
    getHintBtn.textContent = this.currentHintLevel === 0 ? 'Get Hint' : 'Get Next Hint';
    getHintBtn.onclick = () => this.showNextHint();
    buttonGroup.appendChild(getHintBtn);

    const showExampleBtn = document.createElement('button');
    showExampleBtn.className = 'btn-hint';
    showExampleBtn.textContent = 'Show Example';
    showExampleBtn.onclick = () => this.showExample();
    buttonGroup.appendChild(showExampleBtn);

    const showSolutionBtn = document.createElement('button');
    showSolutionBtn.className = 'btn-hint';
    showSolutionBtn.textContent = 'Show Solution';
    showSolutionBtn.onclick = () => this.showSolution();
    buttonGroup.appendChild(showSolutionBtn);

    content.appendChild(buttonGroup);

    // Hints display area
    const hintsDisplay = document.createElement('div');
    hintsDisplay.id = 'hints-display';
    hintsDisplay.className = 'hints-display';
    content.appendChild(hintsDisplay);

    wrapper.appendChild(content);
    container.appendChild(wrapper);
  }

  /**
   * Show next hint
   */
  async showNextHint() {
    try {
      this.currentHintLevel++;
      const hint = await this.api.getHint(this.workshopId, this.step, this.currentHintLevel);
      this.hintsUsed.push({ level: this.currentHintLevel, timestamp: Date.now() });
      this.displayHint(hint.hint, this.currentHintLevel);
    } catch (error) {
      console.error('Failed to get hint:', error);
      this.displayError('Failed to load hint');
    }
  }

  /**
   * Display hint
   * @private
   */
  displayHint(hint, level) {
    const display = document.getElementById('hints-display');
    if (!display) return;

    display.innerHTML = '';
    const hintEl = document.createElement('div');
    hintEl.className = 'hint-content';
    hintEl.innerHTML = `
      <div class="hint-level">Level ${level} Hint</div>
      <p>${this.escapeHtml(hint)}</p>
    `;
    display.appendChild(hintEl);
  }

  /**
   * Show example code
   */
  async showExample() {
    try {
      const example = await this.api.getExample(this.workshopId, this.step);
      this.hintsUsed.push({ type: 'example', timestamp: Date.now() });
      this.displayCode(example.code, 'Example Code', example.explanation);
    } catch (error) {
      console.error('Failed to get example:', error);
      this.displayError('Failed to load example');
    }
  }

  /**
   * Show solution code
   */
  async showSolution() {
    try {
      const solution = await this.api.getSolution(this.workshopId, this.step);
      this.hintsUsed.push({ type: 'solution', timestamp: Date.now() });
      this.displayCode(solution.code, 'Full Solution', solution.explanation);
    } catch (error) {
      console.error('Failed to get solution:', error);
      this.displayError('Failed to load solution');
    }
  }

  /**
   * Display code
   * @private
   */
  displayCode(code, title, explanation) {
    const display = document.getElementById('hints-display');
    if (!display) return;

    display.innerHTML = '';
    const codeEl = document.createElement('div');
    codeEl.className = 'code-display';
    codeEl.innerHTML = `
      <div class="code-title">${title}</div>
      <pre><code>${this.escapeHtml(code)}</code></pre>
      ${explanation ? `<p class="code-explanation">${this.escapeHtml(explanation)}</p>` : ''}
    `;
    display.appendChild(codeEl);
  }

  /**
   * Display error
   * @private
   */
  displayError(message) {
    const display = document.getElementById('hints-display');
    if (!display) return;

    display.innerHTML = '';
    const errorEl = document.createElement('div');
    errorEl.className = 'hint-error';
    errorEl.textContent = message;
    display.appendChild(errorEl);
  }

  /**
   * Get hints used
   * @returns {Array}
   */
  getHintsUsed() {
    return this.hintsUsed;
  }

  /**
   * Reset hints
   */
  reset() {
    this.currentHintLevel = 0;
    this.hintsUsed = [];
    if (this.container) {
      this.render(this.container);
    }
  }

  /**
   * Set step
   * @param {number} step - The new step number
   */
  setStep(step) {
    this.step = step;
    this.reset();
  }

  /**
   * Escape HTML
   * @private
   */
  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = HintsPanel;
}

