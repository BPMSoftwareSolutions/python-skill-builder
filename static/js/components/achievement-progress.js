/**
 * Achievement Progress Component
 * Displays progress indicators for achievement unlock conditions
 */

export class AchievementProgressComponent {
  /**
   * Create a progress bar for an achievement
   * @param {Object} achievement - Achievement object
   * @param {Object} progress - Progress object with current, target, percentage
   * @returns {HTMLElement} Progress bar element
   */
  static createProgressBar(achievement, progress) {
    const container = document.createElement('div');
    container.className = 'achievement-progress-container';

    const title = document.createElement('h4');
    title.className = 'achievement-progress-title';
    title.textContent = achievement.name;
    container.appendChild(title);

    const description = document.createElement('p');
    description.className = 'achievement-progress-description';
    description.textContent = achievement.description;
    container.appendChild(description);

    // Create progress bars for each condition
    Object.entries(progress).forEach(([key, progressData]) => {
      const progressItem = document.createElement('div');
      progressItem.className = 'progress-item';

      const label = document.createElement('div');
      label.className = 'progress-label';
      label.innerHTML = `
        <span class="progress-name">${this.formatConditionName(key)}</span>
        <span class="progress-value">${progressData.current}/${progressData.target}</span>
      `;
      progressItem.appendChild(label);

      const barContainer = document.createElement('div');
      barContainer.className = 'progress-bar-container';

      const bar = document.createElement('div');
      bar.className = 'progress-bar';
      bar.style.width = `${progressData.percentage}%`;
      barContainer.appendChild(bar);

      const percentage = document.createElement('span');
      percentage.className = 'progress-percentage';
      percentage.textContent = `${progressData.percentage}%`;
      barContainer.appendChild(percentage);

      progressItem.appendChild(barContainer);
      container.appendChild(progressItem);
    });

    return container;
  }

  /**
   * Create a progress card showing multiple achievements
   * @param {Array} achievements - Array of achievements with progress
   * @returns {HTMLElement} Progress card element
   */
  static createProgressCard(achievements) {
    const card = document.createElement('div');
    card.className = 'achievement-progress-card';

    const title = document.createElement('h3');
    title.className = 'card-title';
    title.textContent = 'Achievement Progress';
    card.appendChild(title);

    // Show only achievements with progress (not yet unlocked)
    const inProgress = achievements.filter(a => !a.unlocked && a.progress);

    if (inProgress.length === 0) {
      const message = document.createElement('p');
      message.className = 'no-progress';
      message.textContent = 'All achievements unlocked!';
      card.appendChild(message);
      return card;
    }

    // Show top 3 closest to unlocking
    const sorted = inProgress.sort((a, b) => {
      const aPercentage = Object.values(a.progress)[0]?.percentage || 0;
      const bPercentage = Object.values(b.progress)[0]?.percentage || 0;
      return bPercentage - aPercentage;
    });

    sorted.slice(0, 3).forEach(achievement => {
      const progressBar = this.createProgressBar(achievement, achievement.progress);
      card.appendChild(progressBar);
    });

    return card;
  }

  /**
   * Create a mini progress indicator for dashboard
   * @param {Array} achievements - Array of achievements
   * @returns {HTMLElement} Mini indicator element
   */
  static createMiniIndicator(achievements) {
    const indicator = document.createElement('div');
    indicator.className = 'achievement-mini-indicator';

    const unlockedCount = achievements.filter(a => a.unlocked).length;
    const totalCount = achievements.length;
    const percentage = Math.round((unlockedCount / totalCount) * 100);

    indicator.innerHTML = `
      <div class="mini-stat">
        <span class="mini-label">Achievements</span>
        <span class="mini-value">${unlockedCount}/${totalCount}</span>
      </div>
      <div class="mini-progress-bar">
        <div class="mini-progress-fill" style="width: ${percentage}%"></div>
      </div>
      <div class="mini-percentage">${percentage}%</div>
    `;

    return indicator;
  }

  /**
   * Create a streak indicator
   * @param {Object} streakInfo - Streak information object
   * @returns {HTMLElement} Streak indicator element
   */
  static createStreakIndicator(streakInfo) {
    const indicator = document.createElement('div');
    indicator.className = 'streak-indicator';

    const current = streakInfo.current || 0;
    const longest = streakInfo.longest || 0;

    indicator.innerHTML = `
      <div class="streak-item">
        <span class="streak-icon">🔥</span>
        <div class="streak-info">
          <span class="streak-label">Current Streak</span>
          <span class="streak-value">${current}</span>
        </div>
      </div>
      <div class="streak-item">
        <span class="streak-icon">🏆</span>
        <div class="streak-info">
          <span class="streak-label">Longest Streak</span>
          <span class="streak-value">${longest}</span>
        </div>
      </div>
    `;

    return indicator;
  }

  /**
   * Format condition name for display
   * @param {string} conditionKey - Condition key
   * @returns {string} Formatted name
   */
  static formatConditionName(conditionKey) {
    return conditionKey
      .replace(/([A-Z])/g, ' $1')
      .replace(/^./, str => str.toUpperCase())
      .trim();
  }

  /**
   * Create a statistics summary
   * @param {Object} stats - Statistics object
   * @returns {HTMLElement} Statistics element
   */
  static createStatisticsSummary(stats) {
    const summary = document.createElement('div');
    summary.className = 'statistics-summary';

    const items = [
      { label: 'RED Phases', value: stats.redPhasesCompleted || 0 },
      { label: 'GREEN Phases', value: stats.greenPhasesCompleted || 0 },
      { label: 'REFACTOR Phases', value: stats.refactorPhasesCompleted || 0 },
      { label: 'Tests Passed', value: stats.testsPassed || 0 },
      { label: 'Perfect Scores', value: stats.perfectScores || 0 },
      { label: 'Total Points', value: stats.totalPoints || 0 },
    ];

    items.forEach(item => {
      const statItem = document.createElement('div');
      statItem.className = 'stat-item';
      statItem.innerHTML = `
        <span class="stat-label">${item.label}</span>
        <span class="stat-value">${item.value}</span>
      `;
      summary.appendChild(statItem);
    });

    return summary;
  }
}

export default AchievementProgressComponent;

