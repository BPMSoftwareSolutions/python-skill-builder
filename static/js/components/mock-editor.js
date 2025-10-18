/**
 * Mock Editor Component
 * Allows creation and editing of custom mock data
 */

export class MockEditorComponent {
  /**
   * Render mock editor form
   * @param {Object} mockManager - Mock manager instance
   * @param {HTMLElement} container - Container element
   * @param {Function} onSave - Callback when mock set is saved
   */
  static render(mockManager, container, onSave) {
    if (!container) return;

    container.innerHTML = '';

    const editorWrapper = document.createElement('div');
    editorWrapper.className = 'mock-editor-wrapper';

    // Create form
    const form = document.createElement('form');
    form.className = 'mock-editor-form';

    // Mock Set ID field
    const idGroup = this.createFormGroup('Mock Set ID', 'mock-id', 'text', 'e.g., custom_1', true);
    form.appendChild(idGroup);

    // Mock Set Name field
    const nameGroup = this.createFormGroup('Mock Set Name', 'mock-name', 'text', 'e.g., My Custom Tests', true);
    form.appendChild(nameGroup);

    // Mock Set Description field
    const descGroup = this.createFormGroup('Description', 'mock-description', 'text', 'Optional description', false);
    form.appendChild(descGroup);

    // Data Points JSON field
    const dataPointsGroup = document.createElement('div');
    dataPointsGroup.className = 'form-group';

    const dataPointsLabel = document.createElement('label');
    dataPointsLabel.htmlFor = 'mock-data-points';
    dataPointsLabel.textContent = 'Data Points (JSON)';
    dataPointsLabel.className = 'form-label';

    const dataPointsTextarea = document.createElement('textarea');
    dataPointsTextarea.id = 'mock-data-points';
    dataPointsTextarea.className = 'form-textarea';
    dataPointsTextarea.placeholder = `[
  { "inputs": [2, 3], "expected": 5 },
  { "inputs": [5, 10], "expected": 15 }
]`;
    dataPointsTextarea.rows = 6;

    dataPointsGroup.appendChild(dataPointsLabel);
    dataPointsGroup.appendChild(dataPointsTextarea);
    form.appendChild(dataPointsGroup);

    // Buttons
    const buttonGroup = document.createElement('div');
    buttonGroup.className = 'form-button-group';

    const saveBtn = document.createElement('button');
    saveBtn.type = 'button';
    saveBtn.className = 'btn-primary btn-sm';
    saveBtn.textContent = '💾 Save Mock Set';

    const resetBtn = document.createElement('button');
    resetBtn.type = 'button';
    resetBtn.className = 'btn-secondary btn-sm';
    resetBtn.textContent = '🔄 Clear Form';

    saveBtn.addEventListener('click', () => {
      this.handleSave(form, mockManager, onSave);
    });

    resetBtn.addEventListener('click', () => {
      form.reset();
    });

    buttonGroup.appendChild(saveBtn);
    buttonGroup.appendChild(resetBtn);
    form.appendChild(buttonGroup);

    editorWrapper.appendChild(form);
    container.appendChild(editorWrapper);
  }

  /**
   * Create a form group
   * @param {string} label - Label text
   * @param {string} id - Input ID
   * @param {string} type - Input type
   * @param {string} placeholder - Placeholder text
   * @param {boolean} required - Is required
   * @returns {HTMLElement} Form group element
   */
  static createFormGroup(label, id, type, placeholder, required) {
    const group = document.createElement('div');
    group.className = 'form-group';

    const labelEl = document.createElement('label');
    labelEl.htmlFor = id;
    labelEl.className = 'form-label';
    labelEl.textContent = label;
    if (required) {
      labelEl.innerHTML += ' <span class="required">*</span>';
    }

    const input = document.createElement('input');
    input.id = id;
    input.type = type;
    input.className = 'form-input';
    input.placeholder = placeholder;
    input.required = required;

    group.appendChild(labelEl);
    group.appendChild(input);

    return group;
  }

  /**
   * Handle save button click
   * @param {HTMLElement} form - Form element
   * @param {Object} mockManager - Mock manager instance
   * @param {Function} onSave - Callback when saved
   */
  static handleSave(form, mockManager, onSave) {
    const id = form.querySelector('#mock-id').value.trim();
    const name = form.querySelector('#mock-name').value.trim();
    const description = form.querySelector('#mock-description').value.trim();
    const dataPointsJson = form.querySelector('#mock-data-points').value.trim();

    // Validate inputs
    if (!id || !name || !dataPointsJson) {
      alert('Please fill in all required fields');
      return;
    }

    // Parse data points
    let dataPoints;
    try {
      dataPoints = JSON.parse(dataPointsJson);
      if (!Array.isArray(dataPoints)) {
        throw new Error('Data points must be an array');
      }
    } catch (error) {
      alert(`Invalid JSON: ${error.message}`);
      return;
    }

    // Create mock set
    const mockSet = {
      id,
      name,
      description: description || 'Custom mock set',
      dataPoints
    };

    // Validate and save
    const result = mockManager.createCustomMockSet(mockSet);
    if (result.success) {
      alert(`Mock set "${name}" created successfully!`);
      form.reset();
      if (onSave) {
        onSave(mockSet);
      }
    } else {
      alert(`Failed to create mock set: ${result.error}`);
    }
  }
}

export default MockEditorComponent;

