"""
Unit tests for User Statistics system.
"""

import pytest
import os
import shutil
from app.services.user_stats import UserStats, StatsCalculator
from app.services.workflow_progress import WorkflowProgress
from app.services.workflow_storage import WorkflowStorage
from app.services.achievements import AchievementTracker


class TestUserStats:
    """Test UserStats class."""

    def test_init(self):
        """Test UserStats initialization."""
        stats = UserStats("user1")
        
        assert stats.user_id == "user1"
        assert stats.total_workflows_completed == 0
        assert stats.total_time_spent_hours == 0.0
        assert stats.current_streak == 0
        assert stats.longest_streak == 0
        assert stats.total_achievements == 0
        assert stats.total_points == 0
        assert stats.red_skill_level == 1
        assert stats.green_skill_level == 1
        assert stats.refactor_skill_level == 1

    def test_to_dict(self):
        """Test UserStats serialization."""
        stats = UserStats("user1")
        stats.total_workflows_completed = 5
        stats.total_points = 100
        
        data = stats.to_dict()
        
        assert data["user_id"] == "user1"
        assert data["total_workflows_completed"] == 5
        assert data["total_points"] == 100
        assert data["red_skill_level"] == 1


class TestStatsCalculator:
    """Test StatsCalculator class."""

    @pytest.fixture
    def calculator(self, tmp_path):
        """Create a calculator with temporary storage."""
        calculator = StatsCalculator(str(tmp_path))
        yield calculator
        # Cleanup
        if os.path.exists(str(tmp_path)):
            shutil.rmtree(str(tmp_path))

    def test_init(self, calculator):
        """Test StatsCalculator initialization."""
        assert calculator.storage is not None
        assert calculator.achievement_tracker is not None

    def test_calculate_user_stats_no_data(self, calculator):
        """Test calculating stats for user with no data."""
        stats = calculator.calculate_user_stats("user_no_data")
        
        assert stats.user_id == "user_no_data"
        assert stats.total_workflows_completed == 0
        assert stats.total_achievements == 0

    def test_calculate_user_stats_with_workflows(self, calculator):
        """Test calculating stats with workflow data."""
        # Create a workflow progress
        progress = WorkflowProgress("wf1", "user1", "ws1")
        for step in range(1, 7):
            progress.mark_step_complete(step, {"valid": True})
        progress.time_spent_seconds = 600  # 10 minutes
        
        calculator.storage.save_progress(progress)
        
        stats = calculator.calculate_user_stats("user1")
        
        assert stats.total_workflows_completed == 1
        assert stats.total_time_spent_hours == pytest.approx(600 / 3600, 0.01)

    def test_calculate_skill_level(self, calculator):
        """Test skill level calculation."""
        # Add achievements
        calculator.achievement_tracker.unlock_achievement("user1", "red_analyst")
        calculator.achievement_tracker.unlock_achievement("user1", "test_writer")
        
        level = calculator.calculate_skill_level("red", "user1")
        
        assert level >= 1
        assert level <= 5

    def test_calculate_skill_level_progression(self, calculator):
        """Test skill level increases with more achievements."""
        # Level 1: no achievements
        level1 = calculator.calculate_skill_level("red", "user1")
        assert level1 == 1
        
        # Level 2: 1-2 achievements
        calculator.achievement_tracker.unlock_achievement("user1", "red_analyst")
        level2 = calculator.calculate_skill_level("red", "user1")
        assert level2 >= level1
        
        # Level 3: 3-4 achievements
        calculator.achievement_tracker.unlock_achievement("user1", "test_writer")
        calculator.achievement_tracker.unlock_achievement("user1", "test_master")
        level3 = calculator.calculate_skill_level("red", "user1")
        assert level3 >= level2

    def test_get_leaderboard(self, calculator):
        """Test leaderboard generation."""
        leaderboard = calculator.get_leaderboard(limit=10)
        
        assert isinstance(leaderboard, list)

    def test_get_user_rank(self, calculator):
        """Test user rank retrieval."""
        rank = calculator.get_user_rank("user1")
        
        assert isinstance(rank, int)
        assert rank >= 1

    def test_get_streak_info_no_workflows(self, calculator):
        """Test streak info with no workflows."""
        streak_info = calculator.get_streak_info("user_no_workflows")
        
        assert streak_info["current_streak"] == 0
        assert streak_info["longest_streak"] == 0
        assert streak_info["total_workflows"] == 0

    def test_get_streak_info_with_completed_workflows(self, calculator):
        """Test streak info with completed workflows."""
        # Create 3 completed workflows
        for i in range(1, 4):
            progress = WorkflowProgress(f"wf{i}", "user1", f"ws{i}")
            for step in range(1, 7):
                progress.mark_step_complete(step, {"valid": True})
            calculator.storage.save_progress(progress)
        
        streak_info = calculator.get_streak_info("user1")
        
        assert streak_info["current_streak"] == 3
        assert streak_info["longest_streak"] == 3
        assert streak_info["total_workflows"] == 3

    def test_get_streak_info_with_incomplete_workflow(self, calculator):
        """Test streak info with incomplete workflow."""
        # Create 2 completed workflows
        for i in range(1, 3):
            progress = WorkflowProgress(f"wf{i}", "user1", f"ws{i}")
            for step in range(1, 7):
                progress.mark_step_complete(step, {"valid": True})
            calculator.storage.save_progress(progress)
        
        # Create 1 incomplete workflow
        progress = WorkflowProgress("wf3", "user1", "ws3")
        progress.mark_step_complete(1, {"valid": True})
        calculator.storage.save_progress(progress)
        
        streak_info = calculator.get_streak_info("user1")
        
        assert streak_info["current_streak"] == 0  # Streak broken
        assert streak_info["longest_streak"] == 2
        assert streak_info["total_workflows"] == 3

    def test_count_phase_achievements(self, calculator):
        """Test counting achievements by phase."""
        calculator.achievement_tracker.unlock_achievement("user1", "red_analyst")
        calculator.achievement_tracker.unlock_achievement("user1", "test_writer")
        calculator.achievement_tracker.unlock_achievement("user1", "green_engineer")
        
        achievements = calculator.achievement_tracker.get_user_achievements("user1")
        
        red_count = calculator._count_phase_achievements(achievements, "red")
        green_count = calculator._count_phase_achievements(achievements, "green")
        
        assert red_count == 2
        assert green_count == 1

