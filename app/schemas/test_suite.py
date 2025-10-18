"""
Test Suite Schema
Defines test case structure with assertions and metadata
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from enum import Enum


class AssertionType(str, Enum):
    """Types of assertions supported in tests"""
    EQUAL = "assertEqual"
    NOT_EQUAL = "assertNotEqual"
    TRUE = "assertTrue"
    FALSE = "assertFalse"
    IN = "assertIn"
    NOT_IN = "assertNotIn"
    RAISES = "assertRaises"
    ALMOST_EQUAL = "assertAlmostEqual"
    GREATER_THAN = "assertGreater"
    LESS_THAN = "assertLess"
    GREATER_EQUAL = "assertGreaterEqual"
    LESS_EQUAL = "assertLessEqual"


@dataclass
class TestCase:
    """
    Represents a single test case
    
    Attributes:
        id: Unique identifier for the test
        name: Test name (e.g., 'test_add_positive_numbers')
        description: Human-readable description of what the test validates
        assertion: The assertion statement (e.g., 'assertEqual(add(2, 3), 5)')
        assertion_type: Type of assertion being used
        expected: Expected output/result
        inputs: Input parameters for the test (mock data)
        difficulty: Difficulty level (easy, medium, hard)
        error_message: Optional custom error message
    """
    id: str
    name: str
    description: str
    assertion: str
    assertion_type: AssertionType
    expected: Any
    inputs: List[Any] = field(default_factory=list)
    difficulty: str = "medium"
    error_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert test case to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'assertion': self.assertion,
            'assertion_type': self.assertion_type.value,
            'expected': self.expected,
            'inputs': self.inputs,
            'difficulty': self.difficulty,
            'error_message': self.error_message,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TestCase':
        """Create test case from dictionary"""
        return cls(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            assertion=data['assertion'],
            assertion_type=AssertionType(data['assertion_type']),
            expected=data['expected'],
            inputs=data.get('inputs', []),
            difficulty=data.get('difficulty', 'medium'),
            error_message=data.get('error_message'),
        )


@dataclass
class TestSuite:
    """
    Represents a collection of test cases for a workshop
    
    Attributes:
        id: Unique identifier for the test suite
        name: Name of the test suite
        description: Description of what the test suite validates
        tests: List of test cases
        total_tests: Total number of tests in the suite
    """
    id: str
    name: str
    description: str
    tests: List[TestCase] = field(default_factory=list)

    @property
    def total_tests(self) -> int:
        """Get total number of tests"""
        return len(self.tests)

    def add_test(self, test: TestCase) -> None:
        """Add a test case to the suite"""
        self.tests.append(test)

    def get_test(self, test_id: str) -> Optional[TestCase]:
        """Get a test case by ID"""
        return next((t for t in self.tests if t.id == test_id), None)

    def to_dict(self) -> Dict[str, Any]:
        """Convert test suite to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'tests': [t.to_dict() for t in self.tests],
            'total_tests': self.total_tests,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TestSuite':
        """Create test suite from dictionary"""
        tests = [TestCase.from_dict(t) for t in data.get('tests', [])]
        return cls(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            tests=tests,
        )

