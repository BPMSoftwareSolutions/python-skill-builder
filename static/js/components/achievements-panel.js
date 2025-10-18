/**
 * Achievements Panel Component
 * Displays all achievements with progress and filtering options
 */

import AchievementBadgeComponent from './achievement-badge.js';
import { ACHIEVEMENT_CATEGORIES, ACHIEVEMENT_RARITY } from '../config/achievements.js';

export class AchievementsPanelComponent {
  constructor() {
    this.currentFilter = 'all'; // all, category, rarity
    this.currentFilterValue = null;
    this.achievements = [];
  }

  /**
   * Create the achievements panel
   * @param {Array} achievements - Array of achievements with unlock status
   * @returns {HTMLElement} Panel element
   */
  createPanel(achievements) {
    this.achievements = achievements;

    const panel = document.createElement('div');
    panel.className = 'achievements-panel';

    // Header
    const header = this.createHeader();
    panel.appendChild(header);

    // Filter controls
    const filterControls = this.createFilterControls();
    panel.appendChild(filterControls);

    // Statistics
    const stats = this.createStatistics(achievements);
    panel.appendChild(stats);

    // Achievement grid
    const grid = this.createAchievementGrid(achievements);
    panel.appendChild(grid);

    return panel;
  }

  /**
   * Create panel header
   * @returns {HTMLElement} Header element
   */
  createHeader() {
    const header = document.createElement('div');
    header.className = 'achievements-panel-header';

    header.innerHTML = `
      <h2>Achievements</h2>
      <p>Unlock achievements by mastering TDD phases and reaching milestones</p>
    `;

    return header;
  }

  /**
   * Create filter controls
   * @returns {HTMLElement} Filter controls element
   */
  createFilterControls() {
    const controls = document.createElement('div');
    controls.className = 'achievements-filter-controls';

    // Category filter
    const categoryFilter = document.createElement('div');
    categoryFilter.className = 'filter-group';
    categoryFilter.innerHTML = '<label>Category:</label>';

    const categorySelect = document.createElement('select');
    categorySelect.className = 'category-filter';
    categorySelect.innerHTML = '<option value="all">All Categories</option>';

    Object.values(ACHIEVEMENT_CATEGORIES).forEach(category => {
      const option = document.createElement('option');
      option.value = category;
      option.textContent = category;
      categorySelect.appendChild(option);
    });

    categorySelect.addEventListener('change', (e) => {
      this.currentFilter = e.target.value === 'all' ? 'all' : 'category';
      this.currentFilterValue = e.target.value === 'all' ? null : e.target.value;
      this.updateGrid();
    });

    categoryFilter.appendChild(categorySelect);
    controls.appendChild(categoryFilter);

    // Rarity filter
    const rarityFilter = document.createElement('div');
    rarityFilter.className = 'filter-group';
    rarityFilter.innerHTML = '<label>Rarity:</label>';

    const raritySelect = document.createElement('select');
    raritySelect.className = 'rarity-filter';
    raritySelect.innerHTML = '<option value="all">All Rarities</option>';

    Object.values(ACHIEVEMENT_RARITY).forEach(rarity => {
      const option = document.createElement('option');
      option.value = rarity;
      option.textContent = rarity;
      raritySelect.appendChild(option);
    });

    raritySelect.addEventListener('change', (e) => {
      this.currentFilter = e.target.value === 'all' ? 'all' : 'rarity';
      this.currentFilterValue = e.target.value === 'all' ? null : e.target.value;
      this.updateGrid();
    });

    rarityFilter.appendChild(raritySelect);
    controls.appendChild(rarityFilter);

    return controls;
  }

  /**
   * Create statistics section
   * @param {Array} achievements - Array of achievements
   * @returns {HTMLElement} Statistics element
   */
  createStatistics(achievements) {
    const stats = document.createElement('div');
    stats.className = 'achievements-statistics';

    const unlockedCount = achievements.filter(a => a.unlocked).length;
    const totalCount = achievements.length;
    const completionPercentage = Math.round((unlockedCount / totalCount) * 100);

    const totalPoints = achievements
      .filter(a => a.unlocked)
      .reduce((sum, a) => sum + (a.reward?.points || 0), 0);

    stats.innerHTML = `
      <div class="stat-item">
        <div class="stat-label">Achievements Unlocked</div>
        <div class="stat-value">${unlockedCount}/${totalCount}</div>
      </div>
      <div class="stat-item">
        <div class="stat-label">Completion</div>
        <div class="stat-value">${completionPercentage}%</div>
      </div>
      <div class="stat-item">
        <div class="stat-label">Total Points</div>
        <div class="stat-value">${totalPoints}</div>
      </div>
    `;

    return stats;
  }

  /**
   * Create achievement grid
   * @param {Array} achievements - Array of achievements
   * @returns {HTMLElement} Grid element
   */
  createAchievementGrid(achievements) {
    const grid = document.createElement('div');
    grid.className = 'achievements-grid';
    grid.id = 'achievements-grid';

    const filtered = this.filterAchievements(achievements);

    if (filtered.length === 0) {
      grid.innerHTML = '<p class="no-achievements">No achievements match your filters</p>';
      return grid;
    }

    filtered.forEach(achievement => {
      const badge = AchievementBadgeComponent.createBadgeWithProgress(
        achievement,
        achievement.progress,
        achievement.unlocked
      );
      grid.appendChild(badge);
    });

    return grid;
  }

  /**
   * Filter achievements based on current filter
   * @param {Array} achievements - Array of achievements
   * @returns {Array} Filtered achievements
   */
  filterAchievements(achievements) {
    if (this.currentFilter === 'all') {
      return achievements;
    }

    if (this.currentFilter === 'category') {
      return achievements.filter(a => a.category === this.currentFilterValue);
    }

    if (this.currentFilter === 'rarity') {
      return achievements.filter(a => a.rarity === this.currentFilterValue);
    }

    return achievements;
  }

  /**
   * Update the achievement grid
   */
  updateGrid() {
    const gridContainer = document.getElementById('achievements-grid');
    if (!gridContainer) return;

    const filtered = this.filterAchievements(this.achievements);
    gridContainer.innerHTML = '';

    if (filtered.length === 0) {
      gridContainer.innerHTML = '<p class="no-achievements">No achievements match your filters</p>';
      return;
    }

    filtered.forEach(achievement => {
      const badge = AchievementBadgeComponent.createBadgeWithProgress(
        achievement,
        achievement.progress,
        achievement.unlocked
      );
      gridContainer.appendChild(badge);
    });
  }
}

export default AchievementsPanelComponent;

