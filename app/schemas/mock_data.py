"""
Mock Data Schema
Defines mock data sets and data points for testing
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class MockDataPoint:
    """
    Represents a single mock data point
    
    Attributes:
        inputs: Input values for the test
        expected: Expected output/result
        description: Optional description of this data point
    """
    inputs: List[Any]
    expected: Any
    description: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert mock data point to dictionary"""
        return {
            'inputs': self.inputs,
            'expected': self.expected,
            'description': self.description,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MockDataPoint':
        """Create mock data point from dictionary"""
        return cls(
            inputs=data['inputs'],
            expected=data['expected'],
            description=data.get('description'),
        )


@dataclass
class MockDataSet:
    """
    Represents a collection of mock data points
    
    Attributes:
        id: Unique identifier for the mock data set
        name: Name of the mock data set (e.g., 'Valid Inputs', 'Edge Cases')
        description: Description of what scenarios this set covers
        data_points: List of mock data points
        difficulty: Difficulty level (easy, medium, hard)
    """
    id: str
    name: str
    description: str
    data_points: List[MockDataPoint] = field(default_factory=list)
    difficulty: str = "medium"

    @property
    def total_points(self) -> int:
        """Get total number of data points"""
        return len(self.data_points)

    def add_data_point(self, point: MockDataPoint) -> None:
        """Add a data point to the set"""
        self.data_points.append(point)

    def get_data_point(self, index: int) -> Optional[MockDataPoint]:
        """Get a data point by index"""
        if 0 <= index < len(self.data_points):
            return self.data_points[index]
        return None

    def to_dict(self) -> Dict[str, Any]:
        """Convert mock data set to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'data_points': [p.to_dict() for p in self.data_points],
            'difficulty': self.difficulty,
            'total_points': self.total_points,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MockDataSet':
        """Create mock data set from dictionary"""
        data_points = [
            MockDataPoint.from_dict(p) for p in data.get('data_points', [])
        ]
        return cls(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            data_points=data_points,
            difficulty=data.get('difficulty', 'medium'),
        )

