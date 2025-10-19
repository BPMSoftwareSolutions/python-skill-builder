"""
Achievement System
Tracks and manages TDD-specific achievements and gamification.
"""

import json
import os
from typing import Dict, List, Optional, Callable
from datetime import datetime


class Achievement:
    """Represents a learner achievement."""

    def __init__(
        self,
        id: str,
        name: str,
        description: str,
        icon: str,
        category: str,
        points: int,
    ):
        """
        Initialize an achievement.
        
        Args:
            id: Unique achievement identifier
            name: Achievement name
            description: Achievement description
            icon: Emoji or icon name
            category: Category (red, green, refactor, mastery, streak)
            points: Points awarded
        """
        self.id = id
        self.name = name
        self.description = description
        self.icon = icon
        self.category = category
        self.points = points

    def to_dict(self) -> Dict:
        """Serialize achievement to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "icon": self.icon,
            "category": self.category,
            "points": self.points,
        }


class UnlockedAchievement:
    """Represents an unlocked achievement for a user."""

    def __init__(self, achievement: Achievement):
        """
        Initialize an unlocked achievement.
        
        Args:
            achievement: Achievement instance
        """
        self.achievement = achievement
        self.unlocked_at = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        """Serialize to dictionary."""
        return {
            **self.achievement.to_dict(),
            "unlocked_at": self.unlocked_at,
        }


class AchievementTracker:
    """Tracks user achievements."""

    # Define all achievements
    ACHIEVEMENTS = {
        # RED Phase Achievements
        "red_analyst": Achievement(
            "red_analyst", "🔴 Red Analyst", "Complete 1 RED phase",
            "🔴", "red", 5
        ),
        "test_writer": Achievement(
            "test_writer", "🔴 Test Writer", "Write 5 tests",
            "🔴", "red", 10
        ),
        "test_master": Achievement(
            "test_master", "🔴 Test Master", "Write 25 tests",
            "🔴", "red", 25
        ),
        "edge_case_hunter": Achievement(
            "edge_case_hunter", "🔴 Edge Case Hunter", "Write test with edge cases",
            "🔴", "red", 15
        ),
        "assertion_expert": Achievement(
            "assertion_expert", "🔴 Assertion Expert", "Use 3+ different assertion types",
            "🔴", "red", 20
        ),
        # GREEN Phase Achievements
        "green_engineer": Achievement(
            "green_engineer", "🟢 Green Engineer", "Complete 1 GREEN phase",
            "🟢", "green", 5
        ),
        "code_implementer": Achievement(
            "code_implementer", "🟢 Code Implementer", "Implement 5 functions",
            "🟢", "green", 10
        ),
        "code_master": Achievement(
            "code_master", "🟢 Code Master", "Implement 25 functions",
            "🟢", "green", 25
        ),
        "minimal_coder": Achievement(
            "minimal_coder", "🟢 Minimal Coder", "Pass test with <5 lines of code",
            "🟢", "green", 15
        ),
        "first_try": Achievement(
            "first_try", "🟢 First Try", "Pass test on first attempt",
            "🟢", "green", 20
        ),
        # REFACTOR Phase Achievements
        "refactor_master": Achievement(
            "refactor_master", "🔵 Refactor Master", "Complete 1 REFACTOR phase",
            "🔵", "refactor", 5
        ),
        "code_polisher": Achievement(
            "code_polisher", "🔵 Code Polisher", "Refactor 5 functions",
            "🔵", "refactor", 10
        ),
        "type_hint_pro": Achievement(
            "type_hint_pro", "🔵 Type Hint Pro", "Add type hints to 10 functions",
            "🔵", "refactor", 15
        ),
        "documentation_expert": Achievement(
            "documentation_expert", "🔵 Documentation Expert", "Add docstrings to 10 functions",
            "🔵", "refactor", 15
        ),
        "code_quality_champion": Achievement(
            "code_quality_champion", "🔵 Code Quality Champion", "Improve code metrics in 5 refactors",
            "🔵", "refactor", 20
        ),
        # Mastery Achievements
        "tdd_novice": Achievement(
            "tdd_novice", "🏆 TDD Novice", "Complete 1 full TDD workflow",
            "🏆", "mastery", 10
        ),
        "tdd_practitioner": Achievement(
            "tdd_practitioner", "🏆 TDD Practitioner", "Complete 5 full TDD workflows",
            "🏆", "mastery", 25
        ),
        "tdd_expert": Achievement(
            "tdd_expert", "🏆 TDD Expert", "Complete 25 full TDD workflows",
            "🏆", "mastery", 50
        ),
        "perfect_workflow": Achievement(
            "perfect_workflow", "🏆 Perfect Workflow", "Complete workflow without hints",
            "🏆", "mastery", 30
        ),
        "speed_runner": Achievement(
            "speed_runner", "🏆 Speed Runner", "Complete workflow in <10 minutes",
            "🏆", "mastery", 20
        ),
        # Streak Achievements
        "on_fire": Achievement(
            "on_fire", "🔥 On Fire", "Complete 3 workflows in a row",
            "🔥", "streak", 15
        ),
        "unstoppable": Achievement(
            "unstoppable", "🔥 Unstoppable", "Complete 7 workflows in a row",
            "🔥", "streak", 30
        ),
        "legend": Achievement(
            "legend", "🔥 Legend", "Complete 30 workflows in a row",
            "🔥", "streak", 50
        ),
    }

    def __init__(self, storage_dir: str = "workflows"):
        """
        Initialize achievement tracker.
        
        Args:
            storage_dir: Directory to store achievement data
        """
        self.storage_dir = storage_dir
        self._ensure_storage_dir()

    def _ensure_storage_dir(self) -> None:
        """Create storage directory if it doesn't exist."""
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir, exist_ok=True)

    def _get_achievements_path(self, user_id: str) -> str:
        """Get file path for user achievements."""
        user_dir = os.path.join(self.storage_dir, user_id)
        if not os.path.exists(user_dir):
            os.makedirs(user_dir, exist_ok=True)
        return os.path.join(user_dir, "achievements.json")

    def unlock_achievement(self, user_id: str, achievement_id: str) -> bool:
        """
        Unlock an achievement for a user.
        
        Args:
            user_id: User identifier
            achievement_id: Achievement identifier
            
        Returns:
            True if unlocked, False if already unlocked or invalid
        """
        if achievement_id not in self.ACHIEVEMENTS:
            return False
        
        achievements = self._load_achievements(user_id)
        
        if achievement_id in achievements:
            return False  # Already unlocked
        
        achievement = self.ACHIEVEMENTS[achievement_id]
        achievements[achievement_id] = UnlockedAchievement(achievement).to_dict()
        self._save_achievements(user_id, achievements)
        return True

    def get_user_achievements(self, user_id: str) -> List[Dict]:
        """
        Get all achievements for a user.
        
        Args:
            user_id: User identifier
            
        Returns:
            List of achievement dictionaries
        """
        achievements = self._load_achievements(user_id)
        return list(achievements.values())

    def get_total_points(self, user_id: str) -> int:
        """
        Get total points for a user.
        
        Args:
            user_id: User identifier
            
        Returns:
            Total points
        """
        achievements = self._load_achievements(user_id)
        total = 0
        for achievement_id in achievements:
            if achievement_id in self.ACHIEVEMENTS:
                total += self.ACHIEVEMENTS[achievement_id].points
        return total

    def _load_achievements(self, user_id: str) -> Dict:
        """Load achievements from file."""
        path = self._get_achievements_path(user_id)
        
        if not os.path.exists(path):
            return {}
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def _save_achievements(self, user_id: str, achievements: Dict) -> None:
        """Save achievements to file."""
        path = self._get_achievements_path(user_id)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(achievements, f, indent=2)

