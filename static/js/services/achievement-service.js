/**
 * Achievement Service
 * Handles achievement checking, unlocking, and tracking
 */

import { ACHIEVEMENTS, getAchievementById } from '../config/achievements.js';

export class AchievementService {
  /**
   * Check if an achievement should be unlocked based on progress
   * @param {Object} achievement - Achievement definition
   * @param {Object} stats - Current statistics object
   * @returns {boolean} True if achievement should be unlocked
   */
  static shouldUnlock(achievement, stats) {
    const condition = achievement.unlockCondition;

    // Check each condition in the unlock condition object
    for (const [key, value] of Object.entries(condition)) {
      const statValue = stats[key];

      if (statValue === undefined) {
        return false;
      }

      // Handle different condition types
      if (typeof value === 'number') {
        // For numeric conditions, check if stat meets or exceeds the value
        if (statValue < value) {
          return false;
        }
      } else if (typeof value === 'boolean') {
        // For boolean conditions, check exact match
        if (statValue !== value) {
          return false;
        }
      }
    }

    return true;
  }

  /**
   * Check all achievements and return newly unlocked ones
   * @param {Object} stats - Current statistics object
   * @param {Array} unlockedAchievements - Array of already unlocked achievement IDs
   * @returns {Array} Array of newly unlocked achievement objects
   */
  static checkAchievements(stats, unlockedAchievements = []) {
    const newlyUnlocked = [];

    for (const achievement of ACHIEVEMENTS) {
      // Skip if already unlocked
      if (unlockedAchievements.includes(achievement.id)) {
        continue;
      }

      // Check if achievement should be unlocked
      if (this.shouldUnlock(achievement, stats)) {
        newlyUnlocked.push(achievement);
      }
    }

    return newlyUnlocked;
  }

  /**
   * Calculate total points from achievements
   * @param {Array} unlockedAchievementIds - Array of unlocked achievement IDs
   * @returns {number} Total points
   */
  static calculateTotalPoints(unlockedAchievementIds) {
    return unlockedAchievementIds.reduce((total, id) => {
      const achievement = getAchievementById(id);
      return total + (achievement?.reward?.points || 0);
    }, 0);
  }

  /**
   * Get achievement progress for a specific achievement
   * @param {string} achievementId - Achievement ID
   * @param {Object} stats - Current statistics object
   * @returns {Object} Progress object with current and target values
   */
  static getAchievementProgress(achievementId, stats) {
    const achievement = getAchievementById(achievementId);
    if (!achievement) {
      return null;
    }

    const condition = achievement.unlockCondition;
    const progress = {};

    for (const [key, targetValue] of Object.entries(condition)) {
      const currentValue = stats[key] || 0;
      progress[key] = {
        current: currentValue,
        target: targetValue,
        percentage: Math.min(100, Math.round((currentValue / targetValue) * 100)),
      };
    }

    return progress;
  }

  /**
   * Get all achievements with their unlock status
   * @param {Object} stats - Current statistics object
   * @param {Array} unlockedAchievementIds - Array of unlocked achievement IDs
   * @returns {Array} Array of achievements with unlock status
   */
  static getAllAchievementsWithStatus(stats, unlockedAchievementIds = []) {
    return ACHIEVEMENTS.map(achievement => ({
      ...achievement,
      unlocked: unlockedAchievementIds.includes(achievement.id),
      progress: this.getAchievementProgress(achievement.id, stats),
    }));
  }

  /**
   * Get achievements grouped by category
   * @param {Object} stats - Current statistics object
   * @param {Array} unlockedAchievementIds - Array of unlocked achievement IDs
   * @returns {Object} Achievements grouped by category
   */
  static getAchievementsByCategory(stats, unlockedAchievementIds = []) {
    const grouped = {};

    for (const achievement of ACHIEVEMENTS) {
      const category = achievement.category;
      if (!grouped[category]) {
        grouped[category] = [];
      }

      grouped[category].push({
        ...achievement,
        unlocked: unlockedAchievementIds.includes(achievement.id),
        progress: this.getAchievementProgress(achievement.id, stats),
      });
    }

    return grouped;
  }

  /**
   * Get achievements grouped by rarity
   * @param {Object} stats - Current statistics object
   * @param {Array} unlockedAchievementIds - Array of unlocked achievement IDs
   * @returns {Object} Achievements grouped by rarity
   */
  static getAchievementsByRarity(stats, unlockedAchievementIds = []) {
    const grouped = {};

    for (const achievement of ACHIEVEMENTS) {
      const rarity = achievement.rarity;
      if (!grouped[rarity]) {
        grouped[rarity] = [];
      }

      grouped[rarity].push({
        ...achievement,
        unlocked: unlockedAchievementIds.includes(achievement.id),
        progress: this.getAchievementProgress(achievement.id, stats),
      });
    }

    return grouped;
  }
}

export default AchievementService;

