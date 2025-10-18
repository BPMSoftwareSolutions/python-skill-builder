/**
 * Achievement Notification Component
 * Manages achievement unlock notifications and animations
 */

import AchievementBadgeComponent from './achievement-badge.js';

export class AchievementNotificationComponent {
  constructor() {
    this.notificationQueue = [];
    this.isShowing = false;
    this.notificationContainer = this.createContainer();
  }

  /**
   * Create notification container
   * @returns {HTMLElement} Container element
   */
  createContainer() {
    const container = document.createElement('div');
    container.id = 'achievement-notification-container';
    container.className = 'achievement-notification-container';
    document.body.appendChild(container);
    return container;
  }

  /**
   * Show a single achievement notification
   * @param {Object} achievement - Achievement object
   * @param {number} duration - Duration to show in milliseconds
   * @returns {Promise} Resolves when notification is done
   */
  showNotification(achievement, duration = 5000) {
    return new Promise((resolve) => {
      this.notificationQueue.push({ achievement, duration, resolve });
      this.processQueue();
    });
  }

  /**
   * Show multiple achievement notifications
   * @param {Array} achievements - Array of achievement objects
   * @param {number} duration - Duration for each notification
   * @returns {Promise} Resolves when all notifications are done
   */
  async showNotifications(achievements, duration = 5000) {
    for (const achievement of achievements) {
      await this.showNotification(achievement, duration);
    }
  }

  /**
   * Process notification queue
   */
  processQueue() {
    if (this.isShowing || this.notificationQueue.length === 0) {
      return;
    }

    this.isShowing = true;
    const { achievement, duration, resolve } = this.notificationQueue.shift();

    const notification = AchievementBadgeComponent.createNotification(achievement);
    this.notificationContainer.appendChild(notification);

    // Trigger animation
    setTimeout(() => {
      notification.classList.add('show');
    }, 10);

    // Remove after duration
    setTimeout(() => {
      notification.classList.remove('show');
      setTimeout(() => {
        notification.remove();
        this.isShowing = false;
        resolve();
        this.processQueue();
      }, 300);
    }, duration);
  }

  /**
   * Clear all notifications
   */
  clearAll() {
    this.notificationQueue = [];
    this.notificationContainer.innerHTML = '';
    this.isShowing = false;
  }
}

export default AchievementNotificationComponent;

