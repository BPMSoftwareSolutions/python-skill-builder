/**
 * Achievement Definitions
 * Defines all TDD-specific achievements with metadata, categories, rarity levels, and unlock conditions
 */

export const ACHIEVEMENT_CATEGORIES = {
  RED: 'RED',
  GREEN: 'GREEN',
  REFACTOR: 'REFACTOR',
  COVERAGE: 'Coverage',
  CONSISTENCY: 'Consistency',
};

export const ACHIEVEMENT_RARITY = {
  COMMON: 'Common',
  UNCOMMON: 'Uncommon',
  RARE: 'Rare',
  EPIC: 'Epic',
  LEGENDARY: 'Legendary',
};

export const ACHIEVEMENTS = [
  // RED Phase Achievements
  {
    id: 'red_phase_master',
    name: '🔴 Red Phase Master',
    description: 'Analyzed 10 test suites in RED phase',
    category: ACHIEVEMENT_CATEGORIES.RED,
    rarity: ACHIEVEMENT_RARITY.UNCOMMON,
    icon: 'target',
    unlockCondition: { redPhasesCompleted: 10 },
    reward: { points: 50 },
  },
  {
    id: 'test_reader',
    name: '📖 Test Reader',
    description: 'Expanded all test details in a single workshop',
    category: ACHIEVEMENT_CATEGORIES.RED,
    rarity: ACHIEVEMENT_RARITY.COMMON,
    icon: 'book-open',
    unlockCondition: { allTestsExpanded: true },
    reward: { points: 10 },
  },
  {
    id: 'requirement_analyst',
    name: '🔍 Requirement Analyst',
    description: 'Analyzed 50 test cases across all workshops',
    category: ACHIEVEMENT_CATEGORIES.RED,
    rarity: ACHIEVEMENT_RARITY.RARE,
    icon: 'search',
    unlockCondition: { totalTestsAnalyzed: 50 },
    reward: { points: 100 },
  },

  // GREEN Phase Achievements
  {
    id: 'green_achiever',
    name: '🟢 Green Achiever',
    description: 'Passed 50 tests across all workshops',
    category: ACHIEVEMENT_CATEGORIES.GREEN,
    rarity: ACHIEVEMENT_RARITY.UNCOMMON,
    icon: 'check-circle',
    unlockCondition: { testsPassed: 50 },
    reward: { points: 50 },
  },
  {
    id: 'first_green',
    name: '✨ First Green',
    description: 'Passed your first test',
    category: ACHIEVEMENT_CATEGORIES.GREEN,
    rarity: ACHIEVEMENT_RARITY.COMMON,
    icon: 'star',
    unlockCondition: { testsPassed: 1 },
    reward: { points: 5 },
  },
  {
    id: 'perfect_score',
    name: '💯 Perfect Score',
    description: 'Passed all tests on first try (no failures)',
    category: ACHIEVEMENT_CATEGORIES.GREEN,
    rarity: ACHIEVEMENT_RARITY.RARE,
    icon: 'award',
    unlockCondition: { perfectScores: 5 },
    reward: { points: 100 },
  },
  {
    id: 'test_master',
    name: '🏆 Test Master',
    description: 'Passed 200 tests across all workshops',
    category: ACHIEVEMENT_CATEGORIES.GREEN,
    rarity: ACHIEVEMENT_RARITY.EPIC,
    icon: 'crown',
    unlockCondition: { testsPassed: 200 },
    reward: { points: 250 },
  },

  // REFACTOR Phase Achievements
  {
    id: 'refactor_wizard',
    name: '🧙 Refactor Wizard',
    description: 'Improved code quality in 5 workshops',
    category: ACHIEVEMENT_CATEGORIES.REFACTOR,
    rarity: ACHIEVEMENT_RARITY.UNCOMMON,
    icon: 'wand2',
    unlockCondition: { refactorPhases: 5 },
    reward: { points: 50 },
  },
  {
    id: 'complexity_slayer',
    name: '⚔️ Complexity Slayer',
    description: 'Reduced cyclomatic complexity by 50% in a workshop',
    category: ACHIEVEMENT_CATEGORIES.REFACTOR,
    rarity: ACHIEVEMENT_RARITY.RARE,
    icon: 'zap',
    unlockCondition: { complexityReduced: 0.5 },
    reward: { points: 100 },
  },
  {
    id: 'code_artist',
    name: '🎨 Code Artist',
    description: 'Achieved perfect code metrics (complexity, coverage, duplication)',
    category: ACHIEVEMENT_CATEGORIES.REFACTOR,
    rarity: ACHIEVEMENT_RARITY.EPIC,
    icon: 'palette',
    unlockCondition: { perfectMetrics: true },
    reward: { points: 200 },
  },

  // Coverage Achievements
  {
    id: 'coverage_champion',
    name: '🎯 Coverage Champion',
    description: 'Achieved 95%+ test coverage',
    category: ACHIEVEMENT_CATEGORIES.COVERAGE,
    rarity: ACHIEVEMENT_RARITY.RARE,
    icon: 'target',
    unlockCondition: { coverage: 0.95 },
    reward: { points: 100 },
  },
  {
    id: 'full_coverage',
    name: '✅ Full Coverage',
    description: 'Achieved 100% test coverage in a workshop',
    category: ACHIEVEMENT_CATEGORIES.COVERAGE,
    rarity: ACHIEVEMENT_RARITY.EPIC,
    icon: 'check-square',
    unlockCondition: { coverage: 1.0 },
    reward: { points: 150 },
  },

  // Consistency Achievements
  {
    id: 'streak_starter',
    name: '🔥 Streak Starter',
    description: 'Completed 5 workshops in a row',
    category: ACHIEVEMENT_CATEGORIES.CONSISTENCY,
    rarity: ACHIEVEMENT_RARITY.COMMON,
    icon: 'flame',
    unlockCondition: { streak: 5 },
    reward: { points: 25 },
  },
  {
    id: 'unstoppable',
    name: '⚡ Unstoppable',
    description: 'Completed 20 workshops in a row',
    category: ACHIEVEMENT_CATEGORIES.CONSISTENCY,
    rarity: ACHIEVEMENT_RARITY.EPIC,
    icon: 'zap',
    unlockCondition: { streak: 20 },
    reward: { points: 200 },
  },
  {
    id: 'tdd_devotee',
    name: '🙏 TDD Devotee',
    description: 'Completed 100 workshops total',
    category: ACHIEVEMENT_CATEGORIES.CONSISTENCY,
    rarity: ACHIEVEMENT_RARITY.LEGENDARY,
    icon: 'heart',
    unlockCondition: { totalWorkshops: 100 },
    reward: { points: 500 },
  },
];

/**
 * Get achievement by ID
 * @param {string} achievementId - Achievement ID
 * @returns {Object|null} Achievement object or null if not found
 */
export function getAchievementById(achievementId) {
  return ACHIEVEMENTS.find(a => a.id === achievementId) || null;
}

/**
 * Get achievements by category
 * @param {string} category - Achievement category
 * @returns {Array} Array of achievements in the category
 */
export function getAchievementsByCategory(category) {
  return ACHIEVEMENTS.filter(a => a.category === category);
}

/**
 * Get achievements by rarity
 * @param {string} rarity - Achievement rarity level
 * @returns {Array} Array of achievements with the rarity level
 */
export function getAchievementsByRarity(rarity) {
  return ACHIEVEMENTS.filter(a => a.rarity === rarity);
}

/**
 * Get all achievements
 * @returns {Array} Array of all achievements
 */
export function getAllAchievements() {
  return ACHIEVEMENTS;
}

export default ACHIEVEMENTS;

