"""
User Statistics Service
Tracks and calculates user statistics and skill levels.
"""

from typing import Dict, List, Optional
from .workflow_storage import WorkflowStorage
from .achievements import AchievementTracker


class UserStats:
    """User statistics and progress."""

    def __init__(self, user_id: str):
        """
        Initialize user stats.
        
        Args:
            user_id: User identifier
        """
        self.user_id = user_id
        self.total_workflows_completed = 0
        self.total_time_spent_hours = 0.0
        self.current_streak = 0
        self.longest_streak = 0
        self.total_achievements = 0
        self.total_points = 0
        self.average_time_per_workflow = 0.0
        self.average_hints_per_workflow = 0.0
        self.average_attempts_per_step = 0.0
        
        # Per-phase stats
        self.red_phase_completions = 0
        self.green_phase_completions = 0
        self.refactor_phase_completions = 0
        
        # Skill levels (1-5)
        self.red_skill_level = 1
        self.green_skill_level = 1
        self.refactor_skill_level = 1

    def to_dict(self) -> Dict:
        """Serialize stats to dictionary."""
        return {
            "user_id": self.user_id,
            "total_workflows_completed": self.total_workflows_completed,
            "total_time_spent_hours": self.total_time_spent_hours,
            "current_streak": self.current_streak,
            "longest_streak": self.longest_streak,
            "total_achievements": self.total_achievements,
            "total_points": self.total_points,
            "average_time_per_workflow": self.average_time_per_workflow,
            "average_hints_per_workflow": self.average_hints_per_workflow,
            "average_attempts_per_step": self.average_attempts_per_step,
            "red_phase_completions": self.red_phase_completions,
            "green_phase_completions": self.green_phase_completions,
            "refactor_phase_completions": self.refactor_phase_completions,
            "red_skill_level": self.red_skill_level,
            "green_skill_level": self.green_skill_level,
            "refactor_skill_level": self.refactor_skill_level,
        }


class StatsCalculator:
    """Calculates user statistics."""

    def __init__(self, storage_dir: str = "workflows"):
        """
        Initialize stats calculator.
        
        Args:
            storage_dir: Directory for workflow storage
        """
        self.storage = WorkflowStorage(storage_dir)
        self.achievement_tracker = AchievementTracker(storage_dir)

    def calculate_user_stats(self, user_id: str) -> UserStats:
        """
        Calculate comprehensive user statistics.
        
        Args:
            user_id: User identifier
            
        Returns:
            UserStats instance
        """
        stats = UserStats(user_id)
        
        # Get progress stats
        progress_stats = self.storage.get_progress_stats(user_id)
        
        stats.total_workflows_completed = progress_stats["completed_workflows"]
        stats.total_time_spent_hours = progress_stats["total_time_seconds"] / 3600
        stats.average_time_per_workflow = progress_stats["average_time_per_workflow"] / 60  # Convert to minutes
        stats.average_hints_per_workflow = progress_stats["average_hints_per_workflow"]
        stats.average_attempts_per_step = progress_stats["average_attempts_per_workflow"]
        
        # Get achievements
        achievements = self.achievement_tracker.get_user_achievements(user_id)
        stats.total_achievements = len(achievements)
        stats.total_points = self.achievement_tracker.get_total_points(user_id)
        
        # Calculate skill levels
        stats.red_skill_level = self._calculate_skill_level("red", achievements)
        stats.green_skill_level = self._calculate_skill_level("green", achievements)
        stats.refactor_skill_level = self._calculate_skill_level("refactor", achievements)
        
        # Count phase completions
        stats.red_phase_completions = self._count_phase_achievements(achievements, "red")
        stats.green_phase_completions = self._count_phase_achievements(achievements, "green")
        stats.refactor_phase_completions = self._count_phase_achievements(achievements, "refactor")
        
        return stats

    def calculate_skill_level(self, phase: str, user_id: str) -> int:
        """
        Calculate skill level for a phase.
        
        Args:
            phase: Phase name (red, green, refactor)
            user_id: User identifier
            
        Returns:
            Skill level (1-5)
        """
        achievements = self.achievement_tracker.get_user_achievements(user_id)
        return self._calculate_skill_level(phase, achievements)

    def _calculate_skill_level(self, phase: str, achievements: List[Dict]) -> int:
        """
        Calculate skill level based on achievements.
        
        Args:
            phase: Phase name
            achievements: List of achievement dictionaries
            
        Returns:
            Skill level (1-5)
        """
        phase_achievements = [a for a in achievements if a.get("category") == phase]
        count = len(phase_achievements)
        
        if count == 0:
            return 1
        elif count < 3:
            return 2
        elif count < 5:
            return 3
        elif count < 8:
            return 4
        else:
            return 5

    def _count_phase_achievements(self, achievements: List[Dict], phase: str) -> int:
        """Count achievements for a phase."""
        return len([a for a in achievements if a.get("category") == phase])

    def get_leaderboard(self, limit: int = 10, offset: int = 0) -> List[Dict]:
        """
        Get global leaderboard.
        
        Args:
            limit: Number of entries to return
            offset: Offset for pagination
            
        Returns:
            List of leaderboard entries
        """
        # This is a placeholder - in production, would query database
        # For now, return empty list
        return []

    def get_user_rank(self, user_id: str) -> int:
        """
        Get user's rank on leaderboard.
        
        Args:
            user_id: User identifier
            
        Returns:
            User's rank (1-based)
        """
        # This is a placeholder - in production, would query database
        return 1

    def get_streak_info(self, user_id: str) -> Dict:
        """
        Get streak information for user.
        
        Args:
            user_id: User identifier
            
        Returns:
            Dictionary with streak info
        """
        workflow_ids = self.storage.list_user_workflows(user_id)
        
        if not workflow_ids:
            return {
                "current_streak": 0,
                "longest_streak": 0,
                "total_workflows": 0,
            }
        
        # Count consecutive completed workflows
        current_streak = 0
        longest_streak = 0
        
        for workflow_id in sorted(workflow_ids):
            progress = self.storage.load_progress(user_id, workflow_id)
            if progress and progress.is_complete():
                current_streak += 1
                longest_streak = max(longest_streak, current_streak)
            else:
                current_streak = 0
        
        return {
            "current_streak": current_streak,
            "longest_streak": longest_streak,
            "total_workflows": len(workflow_ids),
        }

