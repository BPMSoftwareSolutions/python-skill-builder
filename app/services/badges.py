"""
Badge System
Visual representation of achievements with rarity levels.
"""

from typing import Dict, List
from datetime import datetime


class Badge:
    """Visual representation of an achievement."""

    RARITY_LEVELS = {
        "common": {"color": "#808080", "min_points": 1, "max_points": 5},
        "uncommon": {"color": "#00AA00", "min_points": 5, "max_points": 10},
        "rare": {"color": "#0055FF", "min_points": 10, "max_points": 20},
        "epic": {"color": "#AA00FF", "min_points": 20, "max_points": 50},
        "legendary": {"color": "#FFAA00", "min_points": 50, "max_points": 999},
    }

    def __init__(
        self,
        id: str,
        achievement_id: str,
        name: str,
        emoji: str,
        rarity: str,
        unlock_date: str = None,
    ):
        """
        Initialize a badge.
        
        Args:
            id: Unique badge identifier
            achievement_id: Associated achievement ID
            name: Badge name
            emoji: Badge emoji
            rarity: Rarity level (common, uncommon, rare, epic, legendary)
            unlock_date: ISO timestamp of unlock date
        """
        self.id = id
        self.achievement_id = achievement_id
        self.name = name
        self.emoji = emoji
        self.rarity = rarity
        self.unlock_date = unlock_date or datetime.now().isoformat()

    @property
    def color(self) -> str:
        """Get color for rarity level."""
        return self.RARITY_LEVELS.get(self.rarity, {}).get("color", "#808080")

    def to_dict(self) -> Dict:
        """Serialize badge to dictionary."""
        return {
            "id": self.id,
            "achievement_id": self.achievement_id,
            "name": self.name,
            "emoji": self.emoji,
            "rarity": self.rarity,
            "color": self.color,
            "unlock_date": self.unlock_date,
        }


class BadgeDisplay:
    """Manages badge display and showcase."""

    def __init__(self):
        """Initialize badge display manager."""
        pass

    @staticmethod
    def get_rarity_for_points(points: int) -> str:
        """
        Determine rarity level based on points.
        
        Args:
            points: Achievement points
            
        Returns:
            Rarity level string
        """
        if points < 5:
            return "common"
        elif points < 10:
            return "uncommon"
        elif points < 20:
            return "rare"
        elif points < 50:
            return "epic"
        else:
            return "legendary"

    @staticmethod
    def create_badge_from_achievement(achievement: Dict) -> Badge:
        """
        Create a badge from an achievement.
        
        Args:
            achievement: Achievement dictionary
            
        Returns:
            Badge instance
        """
        rarity = BadgeDisplay.get_rarity_for_points(achievement.get("points", 0))
        
        badge = Badge(
            id=f"badge_{achievement['id']}",
            achievement_id=achievement["id"],
            name=achievement["name"],
            emoji=achievement.get("icon", "🏆"),
            rarity=rarity,
            unlock_date=achievement.get("unlocked_at"),
        )
        
        return badge

    @staticmethod
    def get_badge_showcase(badges: List[Dict]) -> Dict:
        """
        Get badge showcase data for dashboard.
        
        Args:
            badges: List of badge dictionaries
            
        Returns:
            Showcase dictionary with organized badges
        """
        showcase = {
            "total_badges": len(badges),
            "by_rarity": {
                "common": [],
                "uncommon": [],
                "rare": [],
                "epic": [],
                "legendary": [],
            },
            "by_category": {
                "red": [],
                "green": [],
                "refactor": [],
                "mastery": [],
                "streak": [],
            },
            "featured": [],  # Top 5 most recent
        }
        
        # Sort by unlock date (most recent first)
        sorted_badges = sorted(
            badges,
            key=lambda b: b.get("unlocked_at", ""),
            reverse=True
        )
        
        # Organize by rarity and category
        for badge in sorted_badges:
            rarity = badge.get("rarity", "common")
            if rarity in showcase["by_rarity"]:
                showcase["by_rarity"][rarity].append(badge)
            
            # Extract category from achievement (if available)
            # This would need to be passed in or looked up
        
        # Get featured badges (top 5 most recent)
        showcase["featured"] = sorted_badges[:5]
        
        return showcase

    @staticmethod
    def get_rarity_stats(badges: List[Dict]) -> Dict:
        """
        Get statistics about badge rarities.
        
        Args:
            badges: List of badge dictionaries
            
        Returns:
            Statistics dictionary
        """
        stats = {
            "common": 0,
            "uncommon": 0,
            "rare": 0,
            "epic": 0,
            "legendary": 0,
        }
        
        for badge in badges:
            rarity = badge.get("rarity", "common")
            if rarity in stats:
                stats[rarity] += 1
        
        return stats

