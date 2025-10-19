"""
Unit tests for Achievement system.
"""

import pytest
import os
import shutil
from app.services.achievements import Achievement, AchievementTracker


class TestAchievement:
    """Test Achievement class."""

    def test_init(self):
        """Test Achievement initialization."""
        achievement = Achievement(
            "test_id", "Test Achievement", "Test description",
            "🏆", "mastery", 10
        )
        
        assert achievement.id == "test_id"
        assert achievement.name == "Test Achievement"
        assert achievement.description == "Test description"
        assert achievement.icon == "🏆"
        assert achievement.category == "mastery"
        assert achievement.points == 10

    def test_to_dict(self):
        """Test Achievement serialization."""
        achievement = Achievement(
            "test_id", "Test Achievement", "Test description",
            "🏆", "mastery", 10
        )
        
        data = achievement.to_dict()
        
        assert data["id"] == "test_id"
        assert data["name"] == "Test Achievement"
        assert data["points"] == 10


class TestAchievementTracker:
    """Test AchievementTracker class."""

    @pytest.fixture
    def tracker(self, tmp_path):
        """Create a tracker with temporary storage."""
        tracker = AchievementTracker(str(tmp_path))
        yield tracker
        # Cleanup
        if os.path.exists(str(tmp_path)):
            shutil.rmtree(str(tmp_path))

    def test_init(self, tracker):
        """Test AchievementTracker initialization."""
        assert tracker.storage_dir is not None
        assert len(tracker.ACHIEVEMENTS) > 0

    def test_unlock_achievement(self, tracker):
        """Test unlocking an achievement."""
        result = tracker.unlock_achievement("user1", "tdd_novice")
        
        assert result is True

    def test_unlock_same_achievement_twice(self, tracker):
        """Test that same achievement can't be unlocked twice."""
        tracker.unlock_achievement("user1", "tdd_novice")
        result = tracker.unlock_achievement("user1", "tdd_novice")
        
        assert result is False

    def test_unlock_invalid_achievement(self, tracker):
        """Test unlocking invalid achievement."""
        result = tracker.unlock_achievement("user1", "invalid_id")
        
        assert result is False

    def test_get_user_achievements(self, tracker):
        """Test getting user achievements."""
        tracker.unlock_achievement("user1", "tdd_novice")
        tracker.unlock_achievement("user1", "red_analyst")
        
        achievements = tracker.get_user_achievements("user1")
        
        assert len(achievements) == 2
        assert any(a["id"] == "tdd_novice" for a in achievements)
        assert any(a["id"] == "red_analyst" for a in achievements)

    def test_get_total_points(self, tracker):
        """Test total points calculation."""
        tracker.unlock_achievement("user1", "tdd_novice")  # 10 points
        tracker.unlock_achievement("user1", "red_analyst")  # 5 points
        
        total = tracker.get_total_points("user1")
        
        assert total == 15

    def test_get_user_achievements_empty(self, tracker):
        """Test getting achievements for user with none."""
        achievements = tracker.get_user_achievements("user_no_achievements")
        
        assert achievements == []

    def test_get_total_points_empty(self, tracker):
        """Test total points for user with no achievements."""
        total = tracker.get_total_points("user_no_achievements")
        
        assert total == 0

    def test_all_achievements_defined(self, tracker):
        """Test that all achievement types are defined."""
        # RED Phase
        assert "red_analyst" in tracker.ACHIEVEMENTS
        assert "test_writer" in tracker.ACHIEVEMENTS
        assert "test_master" in tracker.ACHIEVEMENTS
        assert "edge_case_hunter" in tracker.ACHIEVEMENTS
        assert "assertion_expert" in tracker.ACHIEVEMENTS
        
        # GREEN Phase
        assert "green_engineer" in tracker.ACHIEVEMENTS
        assert "code_implementer" in tracker.ACHIEVEMENTS
        assert "code_master" in tracker.ACHIEVEMENTS
        assert "minimal_coder" in tracker.ACHIEVEMENTS
        assert "first_try" in tracker.ACHIEVEMENTS
        
        # REFACTOR Phase
        assert "refactor_master" in tracker.ACHIEVEMENTS
        assert "code_polisher" in tracker.ACHIEVEMENTS
        assert "type_hint_pro" in tracker.ACHIEVEMENTS
        assert "documentation_expert" in tracker.ACHIEVEMENTS
        assert "code_quality_champion" in tracker.ACHIEVEMENTS
        
        # Mastery
        assert "tdd_novice" in tracker.ACHIEVEMENTS
        assert "tdd_practitioner" in tracker.ACHIEVEMENTS
        assert "tdd_expert" in tracker.ACHIEVEMENTS
        assert "perfect_workflow" in tracker.ACHIEVEMENTS
        assert "speed_runner" in tracker.ACHIEVEMENTS
        
        # Streak
        assert "on_fire" in tracker.ACHIEVEMENTS
        assert "unstoppable" in tracker.ACHIEVEMENTS
        assert "legend" in tracker.ACHIEVEMENTS

    def test_achievement_categories(self, tracker):
        """Test that achievements have correct categories."""
        red_achievements = [
            a for a in tracker.ACHIEVEMENTS.values()
            if a.category == "red"
        ]
        
        assert len(red_achievements) == 5
        
        green_achievements = [
            a for a in tracker.ACHIEVEMENTS.values()
            if a.category == "green"
        ]
        
        assert len(green_achievements) == 5

    def test_achievement_points(self, tracker):
        """Test that achievements have valid points."""
        for achievement in tracker.ACHIEVEMENTS.values():
            assert achievement.points > 0
            assert achievement.points <= 50

    def test_persistence(self, tracker):
        """Test that achievements persist to disk."""
        tracker.unlock_achievement("user1", "tdd_novice")
        
        # Create new tracker instance
        tracker2 = AchievementTracker(tracker.storage_dir)
        achievements = tracker2.get_user_achievements("user1")
        
        assert len(achievements) == 1
        assert achievements[0]["id"] == "tdd_novice"

