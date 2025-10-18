/**
 * Achievement Badge Component
 * Displays achievement badges with rarity colors and icons
 */

import { ACHIEVEMENT_RARITY } from '../config/achievements.js';

export class AchievementBadgeComponent {
  /**
   * Create an achievement badge element
   * @param {Object} achievement - Achievement object
   * @param {boolean} unlocked - Whether the achievement is unlocked
   * @returns {HTMLElement} Badge element
   */
  static createBadge(achievement, unlocked = false) {
    const badge = document.createElement('div');
    badge.className = `achievement-badge ${unlocked ? 'unlocked' : 'locked'} rarity-${this.getRarityClass(achievement.rarity)}`;
    badge.title = achievement.description;
    badge.setAttribute('data-achievement-id', achievement.id);

    // Badge content
    badge.innerHTML = `
      <div class="badge-icon">${achievement.icon}</div>
      <div class="badge-name">${achievement.name}</div>
      <div class="badge-rarity">${achievement.rarity}</div>
      ${unlocked ? '<div class="badge-unlocked-indicator">✓</div>' : '<div class="badge-locked-indicator">🔒</div>'}
    `;

    return badge;
  }

  /**
   * Create a badge with progress indicator
   * @param {Object} achievement - Achievement object
   * @param {Object} progress - Progress object with current, target, percentage
   * @param {boolean} unlocked - Whether the achievement is unlocked
   * @returns {HTMLElement} Badge element with progress
   */
  static createBadgeWithProgress(achievement, progress, unlocked = false) {
    const badge = this.createBadge(achievement, unlocked);
    badge.classList.add('with-progress');

    // Add progress bar
    const progressBar = document.createElement('div');
    progressBar.className = 'badge-progress-bar';

    const progressFill = document.createElement('div');
    progressFill.className = 'badge-progress-fill';
    progressFill.style.width = `${progress.percentage || 0}%`;

    const progressText = document.createElement('div');
    progressText.className = 'badge-progress-text';

    // Get the first condition key and display progress
    const firstKey = Object.keys(progress)[0];
    if (firstKey && progress[firstKey]) {
      const { current, target } = progress[firstKey];
      progressText.textContent = `${current}/${target}`;
    }

    progressBar.appendChild(progressFill);
    progressBar.appendChild(progressText);
    badge.appendChild(progressBar);

    return badge;
  }

  /**
   * Create a small badge for display on module cards
   * @param {Object} achievement - Achievement object
   * @returns {HTMLElement} Small badge element
   */
  static createSmallBadge(achievement) {
    const badge = document.createElement('div');
    badge.className = `achievement-badge-small rarity-${this.getRarityClass(achievement.rarity)}`;
    badge.title = achievement.name;
    badge.setAttribute('data-achievement-id', achievement.id);
    badge.innerHTML = `<span class="badge-icon-small">${achievement.icon}</span>`;

    return badge;
  }

  /**
   * Create an achievement notification
   * @param {Object} achievement - Achievement object
   * @returns {HTMLElement} Notification element
   */
  static createNotification(achievement) {
    const notification = document.createElement('div');
    notification.className = `achievement-notification rarity-${this.getRarityClass(achievement.rarity)}`;

    notification.innerHTML = `
      <div class="notification-content">
        <div class="notification-icon">${achievement.icon}</div>
        <div class="notification-text">
          <div class="notification-title">Achievement Unlocked!</div>
          <div class="notification-name">${achievement.name}</div>
          <div class="notification-description">${achievement.description}</div>
          <div class="notification-reward">+${achievement.reward.points} points</div>
        </div>
      </div>
    `;

    return notification;
  }

  /**
   * Show achievement notification
   * @param {Object} achievement - Achievement object
   * @param {number} duration - Duration to show notification in milliseconds
   */
  static showNotification(achievement, duration = 5000) {
    const notification = this.createNotification(achievement);
    document.body.appendChild(notification);

    // Trigger animation
    setTimeout(() => {
      notification.classList.add('show');
    }, 10);

    // Remove after duration
    setTimeout(() => {
      notification.classList.remove('show');
      setTimeout(() => {
        notification.remove();
      }, 300);
    }, duration);
  }

  /**
   * Get CSS class for rarity level
   * @param {string} rarity - Rarity level
   * @returns {string} CSS class name
   */
  static getRarityClass(rarity) {
    return rarity.toLowerCase().replace(/\s+/g, '-');
  }

  /**
   * Create a full achievement panel
   * @param {Array} achievements - Array of achievements with unlock status
   * @returns {HTMLElement} Panel element
   */
  static createAchievementPanel(achievements) {
    const panel = document.createElement('div');
    panel.className = 'achievement-panel';

    // Group by category
    const byCategory = {};
    achievements.forEach(achievement => {
      if (!byCategory[achievement.category]) {
        byCategory[achievement.category] = [];
      }
      byCategory[achievement.category].push(achievement);
    });

    // Create sections for each category
    Object.entries(byCategory).forEach(([category, categoryAchievements]) => {
      const section = document.createElement('div');
      section.className = 'achievement-category-section';

      const title = document.createElement('h3');
      title.className = 'achievement-category-title';
      title.textContent = category;
      section.appendChild(title);

      const grid = document.createElement('div');
      grid.className = 'achievement-grid';

      categoryAchievements.forEach(achievement => {
        const badge = this.createBadgeWithProgress(
          achievement,
          achievement.progress,
          achievement.unlocked
        );
        grid.appendChild(badge);
      });

      section.appendChild(grid);
      panel.appendChild(section);
    });

    return panel;
  }
}

export default AchievementBadgeComponent;

