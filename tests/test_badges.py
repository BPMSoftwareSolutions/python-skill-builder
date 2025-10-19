"""
Unit tests for Badge system.
"""

import pytest
from app.services.badges import Badge, BadgeDisplay


class TestBadge:
    """Test Badge class."""

    def test_init(self):
        """Test Badge initialization."""
        badge = Badge(
            "badge1", "achievement1", "Test Badge",
            "🏆", "rare"
        )
        
        assert badge.id == "badge1"
        assert badge.achievement_id == "achievement1"
        assert badge.name == "Test Badge"
        assert badge.emoji == "🏆"
        assert badge.rarity == "rare"

    def test_color_property(self):
        """Test color property for different rarities."""
        rarities = {
            "common": "#808080",
            "uncommon": "#00AA00",
            "rare": "#0055FF",
            "epic": "#AA00FF",
            "legendary": "#FFAA00",
        }
        
        for rarity, expected_color in rarities.items():
            badge = Badge("b1", "a1", "Test", "🏆", rarity)
            assert badge.color == expected_color

    def test_to_dict(self):
        """Test Badge serialization."""
        badge = Badge("badge1", "achievement1", "Test Badge", "🏆", "rare")
        
        data = badge.to_dict()
        
        assert data["id"] == "badge1"
        assert data["achievement_id"] == "achievement1"
        assert data["name"] == "Test Badge"
        assert data["emoji"] == "🏆"
        assert data["rarity"] == "rare"
        assert data["color"] == "#0055FF"


class TestBadgeDisplay:
    """Test BadgeDisplay class."""

    def test_get_rarity_for_points(self):
        """Test rarity determination based on points."""
        assert BadgeDisplay.get_rarity_for_points(1) == "common"
        assert BadgeDisplay.get_rarity_for_points(5) == "uncommon"
        assert BadgeDisplay.get_rarity_for_points(10) == "rare"
        assert BadgeDisplay.get_rarity_for_points(20) == "epic"
        assert BadgeDisplay.get_rarity_for_points(50) == "legendary"
        assert BadgeDisplay.get_rarity_for_points(100) == "legendary"

    def test_create_badge_from_achievement(self):
        """Test creating badge from achievement."""
        achievement = {
            "id": "test_achievement",
            "name": "Test Achievement",
            "icon": "🏆",
            "points": 15,
            "unlocked_at": "2025-10-19T12:00:00"
        }
        
        badge = BadgeDisplay.create_badge_from_achievement(achievement)
        
        assert badge.achievement_id == "test_achievement"
        assert badge.name == "Test Achievement"
        assert badge.emoji == "🏆"
        assert badge.rarity == "rare"  # 15 points = rare

    def test_create_badge_rarity_mapping(self):
        """Test that badge rarity matches points."""
        test_cases = [
            (3, "common"),
            (7, "uncommon"),
            (15, "rare"),
            (30, "epic"),
            (75, "legendary"),
        ]
        
        for points, expected_rarity in test_cases:
            achievement = {
                "id": f"ach_{points}",
                "name": f"Achievement {points}",
                "icon": "🏆",
                "points": points,
                "unlocked_at": "2025-10-19T12:00:00"
            }
            
            badge = BadgeDisplay.create_badge_from_achievement(achievement)
            assert badge.rarity == expected_rarity

    def test_get_badge_showcase(self):
        """Test badge showcase generation."""
        badges = [
            {
                "id": "badge1",
                "name": "Badge 1",
                "rarity": "common",
                "unlocked_at": "2025-10-19T12:00:00"
            },
            {
                "id": "badge2",
                "name": "Badge 2",
                "rarity": "rare",
                "unlocked_at": "2025-10-19T13:00:00"
            },
        ]
        
        showcase = BadgeDisplay.get_badge_showcase(badges)
        
        assert showcase["total_badges"] == 2
        assert len(showcase["featured"]) == 2
        assert showcase["featured"][0]["id"] == "badge2"  # Most recent first

    def test_get_rarity_stats(self):
        """Test rarity statistics."""
        badges = [
            {"id": "b1", "rarity": "common"},
            {"id": "b2", "rarity": "common"},
            {"id": "b3", "rarity": "uncommon"},
            {"id": "b4", "rarity": "rare"},
            {"id": "b5", "rarity": "epic"},
            {"id": "b6", "rarity": "legendary"},
        ]
        
        stats = BadgeDisplay.get_rarity_stats(badges)
        
        assert stats["common"] == 2
        assert stats["uncommon"] == 1
        assert stats["rare"] == 1
        assert stats["epic"] == 1
        assert stats["legendary"] == 1

    def test_get_rarity_stats_empty(self):
        """Test rarity statistics with no badges."""
        stats = BadgeDisplay.get_rarity_stats([])
        
        assert stats["common"] == 0
        assert stats["uncommon"] == 0
        assert stats["rare"] == 0
        assert stats["epic"] == 0
        assert stats["legendary"] == 0

    def test_badge_showcase_by_rarity(self):
        """Test badge showcase organization by rarity."""
        badges = [
            {"id": "b1", "name": "Common", "rarity": "common", "unlocked_at": "2025-10-19T12:00:00"},
            {"id": "b2", "name": "Rare", "rarity": "rare", "unlocked_at": "2025-10-19T13:00:00"},
        ]
        
        showcase = BadgeDisplay.get_badge_showcase(badges)
        
        assert "by_rarity" in showcase
        assert "common" in showcase["by_rarity"]
        assert "rare" in showcase["by_rarity"]

