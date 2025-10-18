/**
 * Mock Selector Component
 * Displays available mock sets and allows selection
 */

export class MockSelectorComponent {
  /**
   * Render mock selector with available mock sets
   * @param {Object} mockManager - Mock manager instance
   * @param {HTMLElement} container - Container element
   * @param {Function} onMockSetChange - Callback when mock set changes
   */
  static render(mockManager, container, onMockSetChange) {
    if (!container) return;

    container.innerHTML = '';

    const allMockSets = mockManager.getAllMockSets();
    const mockSetIds = Object.keys(allMockSets);

    if (mockSetIds.length === 0) {
      container.innerHTML = '<p class="no-mock-sets">No mock sets available</p>';
      return;
    }

    // Create selector wrapper
    const selectorWrapper = document.createElement('div');
    selectorWrapper.className = 'mock-selector-wrapper';

    // Create radio buttons for each mock set
    mockSetIds.forEach((mockSetId) => {
      const mockSet = allMockSets[mockSetId];
      const isSelected = mockSetId === mockManager.getCurrentMockSetId();

      const radioGroup = document.createElement('div');
      radioGroup.className = 'mock-selector-group';

      const radioInput = document.createElement('input');
      radioInput.type = 'radio';
      radioInput.id = `mock-${mockSetId}`;
      radioInput.name = 'mock-set';
      radioInput.value = mockSetId;
      radioInput.checked = isSelected;
      radioInput.className = 'mock-selector-input';

      radioInput.addEventListener('change', () => {
        if (mockManager.switchMockSet(mockSetId)) {
          this.updateSelection(container, mockSetId);
          if (onMockSetChange) {
            onMockSetChange(mockSetId, mockSet);
          }
        }
      });

      const label = document.createElement('label');
      label.htmlFor = `mock-${mockSetId}`;
      label.className = 'mock-selector-label';

      const labelContent = document.createElement('div');
      labelContent.className = 'mock-selector-label-content';

      const labelName = document.createElement('div');
      labelName.className = 'mock-selector-name';
      labelName.textContent = mockSet.name;

      const labelDescription = document.createElement('div');
      labelDescription.className = 'mock-selector-description';
      labelDescription.textContent = mockSet.description || '';

      const labelCount = document.createElement('div');
      labelCount.className = 'mock-selector-count';
      labelCount.textContent = `${mockSet.dataPoints.length} data points`;

      labelContent.appendChild(labelName);
      labelContent.appendChild(labelDescription);
      labelContent.appendChild(labelCount);

      label.appendChild(labelContent);

      radioGroup.appendChild(radioInput);
      radioGroup.appendChild(label);

      selectorWrapper.appendChild(radioGroup);
    });

    container.appendChild(selectorWrapper);
  }

  /**
   * Update selection state
   * @param {HTMLElement} container - Container element
   * @param {string} selectedMockSetId - Selected mock set ID
   */
  static updateSelection(container, selectedMockSetId) {
    const radioInputs = container.querySelectorAll('.mock-selector-input');
    radioInputs.forEach((input) => {
      input.checked = input.value === selectedMockSetId;
    });
  }

  /**
   * Get selected mock set ID
   * @param {HTMLElement} container - Container element
   * @returns {string|null} Selected mock set ID or null
   */
  static getSelectedMockSetId(container) {
    const selectedInput = container.querySelector('.mock-selector-input:checked');
    return selectedInput ? selectedInput.value : null;
  }
}

export default MockSelectorComponent;

