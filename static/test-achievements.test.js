/**
 * Achievement System Tests
 * Tests for achievement definitions, service, and state management
 */

import AchievementService from './js/services/achievement-service.js';
import { ACHIEVEMENTS, getAchievementById, getAchievementsByCategory, getAchievementsByRarity } from './js/config/achievements.js';
import ProgressState from './js/state/progress.js';

describe('Achievement Definitions', () => {
  test('should have at least 15 achievements defined', () => {
    expect(ACHIEVEMENTS.length).toBeGreaterThanOrEqual(15);
  });

  test('each achievement should have required fields', () => {
    ACHIEVEMENTS.forEach(achievement => {
      expect(achievement.id).toBeDefined();
      expect(achievement.name).toBeDefined();
      expect(achievement.description).toBeDefined();
      expect(achievement.category).toBeDefined();
      expect(achievement.rarity).toBeDefined();
      expect(achievement.icon).toBeDefined();
      expect(achievement.unlockCondition).toBeDefined();
      expect(achievement.reward).toBeDefined();
      expect(achievement.reward.points).toBeGreaterThan(0);
    });
  });

  test('achievement IDs should be unique', () => {
    const ids = ACHIEVEMENTS.map(a => a.id);
    const uniqueIds = new Set(ids);
    expect(uniqueIds.size).toBe(ids.length);
  });

  test('getAchievementById should return correct achievement', () => {
    const achievement = getAchievementById('first_green');
    expect(achievement).toBeDefined();
    expect(achievement.name).toContain('First Green');
  });

  test('getAchievementById should return null for invalid ID', () => {
    const achievement = getAchievementById('invalid_id');
    expect(achievement).toBeNull();
  });

  test('getAchievementsByCategory should filter correctly', () => {
    const redAchievements = getAchievementsByCategory('RED');
    expect(redAchievements.length).toBeGreaterThan(0);
    redAchievements.forEach(a => {
      expect(a.category).toBe('RED');
    });
  });

  test('getAchievementsByRarity should filter correctly', () => {
    const commonAchievements = getAchievementsByRarity('Common');
    expect(commonAchievements.length).toBeGreaterThan(0);
    commonAchievements.forEach(a => {
      expect(a.rarity).toBe('Common');
    });
  });
});

describe('Achievement Service', () => {
  test('shouldUnlock should return true when condition is met', () => {
    const achievement = getAchievementById('first_green');
    const stats = { testsPassed: 1 };
    expect(AchievementService.shouldUnlock(achievement, stats)).toBe(true);
  });

  test('shouldUnlock should return false when condition is not met', () => {
    const achievement = getAchievementById('first_green');
    const stats = { testsPassed: 0 };
    expect(AchievementService.shouldUnlock(achievement, stats)).toBe(false);
  });

  test('shouldUnlock should handle multiple conditions', () => {
    const achievement = {
      id: 'test',
      unlockCondition: { testsPassed: 10, redPhasesCompleted: 5 },
    };
    const stats = { testsPassed: 10, redPhasesCompleted: 5 };
    expect(AchievementService.shouldUnlock(achievement, stats)).toBe(true);
  });

  test('shouldUnlock should return false if any condition is not met', () => {
    const achievement = {
      id: 'test',
      unlockCondition: { testsPassed: 10, redPhasesCompleted: 5 },
    };
    const stats = { testsPassed: 10, redPhasesCompleted: 3 };
    expect(AchievementService.shouldUnlock(achievement, stats)).toBe(false);
  });

  test('checkAchievements should return newly unlocked achievements', () => {
    const stats = { testsPassed: 50, redPhasesCompleted: 10 };
    const unlockedIds = [];
    const newlyUnlocked = AchievementService.checkAchievements(stats, unlockedIds);
    expect(newlyUnlocked.length).toBeGreaterThan(0);
  });

  test('checkAchievements should not return already unlocked achievements', () => {
    const stats = { testsPassed: 50 };
    const unlockedIds = ['green_achiever'];
    const newlyUnlocked = AchievementService.checkAchievements(stats, unlockedIds);
    expect(newlyUnlocked.map(a => a.id)).not.toContain('green_achiever');
  });

  test('calculateTotalPoints should sum achievement points', () => {
    const unlockedIds = ['first_green', 'test_reader'];
    const totalPoints = AchievementService.calculateTotalPoints(unlockedIds);
    expect(totalPoints).toBeGreaterThan(0);
  });

  test('getAchievementProgress should return progress object', () => {
    const stats = { testsPassed: 25 };
    const progress = AchievementService.getAchievementProgress('green_achiever', stats);
    expect(progress).toBeDefined();
    expect(progress.testsPassed).toBeDefined();
    expect(progress.testsPassed.current).toBe(25);
    expect(progress.testsPassed.target).toBe(50);
    expect(progress.testsPassed.percentage).toBe(50);
  });

  test('getAllAchievementsWithStatus should include unlock status', () => {
    const stats = { testsPassed: 1 };
    const unlockedIds = ['first_green'];
    const achievements = AchievementService.getAllAchievementsWithStatus(stats, unlockedIds);
    const firstGreen = achievements.find(a => a.id === 'first_green');
    expect(firstGreen.unlocked).toBe(true);
  });

  test('getAchievementsByCategory should group achievements', () => {
    const stats = { testsPassed: 50 };
    const grouped = AchievementService.getAchievementsByCategory(stats);
    expect(Object.keys(grouped).length).toBeGreaterThan(0);
    Object.values(grouped).forEach(categoryAchievements => {
      expect(Array.isArray(categoryAchievements)).toBe(true);
    });
  });

  test('getAchievementsByRarity should group achievements', () => {
    const stats = { testsPassed: 50 };
    const grouped = AchievementService.getAchievementsByRarity(stats);
    expect(Object.keys(grouped).length).toBeGreaterThan(0);
    Object.values(grouped).forEach(rarityAchievements => {
      expect(Array.isArray(rarityAchievements)).toBe(true);
    });
  });
});

describe('Progress State - Achievements', () => {
  let progressState;

  beforeEach(() => {
    progressState = new ProgressState();
    progressState.resetAll();
  });

  test('should initialize module with achievement fields', () => {
    progressState.initializeModule('test-module', 5);
    const progress = progressState.getModuleProgress('test-module');
    expect(progress.achievements).toBeDefined();
    expect(Array.isArray(progress.achievements)).toBe(true);
    expect(progress.stats).toBeDefined();
  });

  test('should unlock achievement', () => {
    progressState.initializeModule('test-module', 5);
    progressState.unlockAchievement('test-module', 'first_green');
    const achievements = progressState.getUnlockedAchievements('test-module');
    expect(achievements).toContain('first_green');
  });

  test('should not duplicate achievement unlock', () => {
    progressState.initializeModule('test-module', 5);
    progressState.unlockAchievement('test-module', 'first_green');
    progressState.unlockAchievement('test-module', 'first_green');
    const achievements = progressState.getUnlockedAchievements('test-module');
    expect(achievements.filter(a => a === 'first_green').length).toBe(1);
  });

  test('should record achievement unlock timestamp', () => {
    progressState.initializeModule('test-module', 5);
    progressState.unlockAchievement('test-module', 'first_green');
    const progress = progressState.getModuleProgress('test-module');
    expect(progress.achievementUnlockedAt['first_green']).toBeDefined();
  });

  test('should update statistics', () => {
    progressState.initializeModule('test-module', 5);
    progressState.updateStats('test-module', { testsPassed: 10, redPhasesCompleted: 2 });
    const stats = progressState.getStats('test-module');
    expect(stats.testsPassed).toBe(10);
    expect(stats.redPhasesCompleted).toBe(2);
  });

  test('should update streak', () => {
    progressState.initializeModule('test-module', 5);
    progressState.updateStreak('test-module', 5);
    const streakInfo = progressState.getStreakInfo('test-module');
    expect(streakInfo.current).toBe(5);
  });

  test('should track longest streak', () => {
    progressState.initializeModule('test-module', 5);
    progressState.updateStreak('test-module', 5);
    progressState.updateStreak('test-module', 3);
    progressState.updateStreak('test-module', 10);
    const streakInfo = progressState.getStreakInfo('test-module');
    expect(streakInfo.longest).toBe(10);
  });

  test('should maintain backward compatibility', () => {
    progressState.initializeModule('test-module', 5);
    progressState.updateWorkshopScore('test-module', 'workshop-1', 85);
    const progress = progressState.getModuleProgress('test-module');
    expect(progress.scores['workshop-1']).toBe(85);
    expect(progress.completed).toBe(1);
  });
});

describe('Achievement Integration', () => {
  test('should unlock achievement when stats meet condition', () => {
    const stats = { testsPassed: 1 };
    const newlyUnlocked = AchievementService.checkAchievements(stats, []);
    const firstGreen = newlyUnlocked.find(a => a.id === 'first_green');
    expect(firstGreen).toBeDefined();
  });

  test('should calculate correct total points', () => {
    const stats = { testsPassed: 50, redPhasesCompleted: 10 };
    const newlyUnlocked = AchievementService.checkAchievements(stats, []);
    const totalPoints = AchievementService.calculateTotalPoints(newlyUnlocked.map(a => a.id));
    expect(totalPoints).toBeGreaterThan(0);
  });

  test('should handle multiple achievement unlocks', () => {
    const stats = {
      testsPassed: 200,
      redPhasesCompleted: 10,
      refactorPhases: 5,
      streak: 20,
    };
    const newlyUnlocked = AchievementService.checkAchievements(stats, []);
    expect(newlyUnlocked.length).toBeGreaterThan(1);
  });
});

