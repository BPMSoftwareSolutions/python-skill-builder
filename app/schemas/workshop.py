"""
Workshop Schema
Extended workshop data model for TDD-first learning
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from enum import Enum

from .test_suite import TestSuite
from .mock_data import MockDataSet
from .phase_guidance import PhaseGuidance
from .tdd_workflow import TDDWorkflowDefinition


class WorkshopPhase(str, Enum):
    """TDD phases"""
    RED = "red"
    GREEN = "green"
    REFACTOR = "refactor"


@dataclass
class WorkshopPhases:
    """
    TDD phases structure for a workshop
    
    Attributes:
        test_suite: Test suite for the workshop
        mock_data_sets: Dictionary of mock data sets
        guidance: Phase-specific guidance
    """
    test_suite: TestSuite
    mock_data_sets: Dict[str, MockDataSet] = field(default_factory=dict)
    guidance: Optional[PhaseGuidance] = None

    def add_mock_data_set(self, mock_set: MockDataSet) -> None:
        """Add a mock data set"""
        self.mock_data_sets[mock_set.id] = mock_set

    def get_mock_data_set(self, set_id: str) -> Optional[MockDataSet]:
        """Get a mock data set by ID"""
        return self.mock_data_sets.get(set_id)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'test_suite': self.test_suite.to_dict(),
            'mock_data_sets': {
                k: v.to_dict() for k, v in self.mock_data_sets.items()
            },
            'guidance': self.guidance.to_dict() if self.guidance else None,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WorkshopPhases':
        """Create from dictionary"""
        test_suite = TestSuite.from_dict(data['test_suite'])
        mock_data_sets = {
            k: MockDataSet.from_dict(v)
            for k, v in data.get('mock_data_sets', {}).items()
        }
        guidance = None
        if data.get('guidance'):
            guidance = PhaseGuidance.from_dict(data['guidance'])
        
        return cls(
            test_suite=test_suite,
            mock_data_sets=mock_data_sets,
            guidance=guidance,
        )


@dataclass
class Workshop:
    """
    Extended workshop model for TDD-first learning

    Attributes:
        id: Unique identifier
        title: Workshop title
        description: Workshop description
        difficulty: Difficulty level (beginner, intermediate, advanced)
        estimated_minutes: Estimated time to complete

        # TDD-specific fields
        phases: TDD phases structure
        tdd_workflow: TDD workflow definition (step-by-step guidance)

        # Backward compatibility fields
        prompt: Original prompt (for backward compatibility)
        starter_code: Original starter code (for backward compatibility)
        hints: Original hints (for backward compatibility)
        tests: Original tests (for backward compatibility)
    """
    id: str
    title: str
    description: str
    difficulty: str = "beginner"
    estimated_minutes: int = 15
    phases: Optional[WorkshopPhases] = None
    tdd_workflow: Optional[TDDWorkflowDefinition] = None

    # Backward compatibility
    prompt: Optional[str] = None
    starter_code: Optional[str] = None
    hints: List[str] = field(default_factory=list)
    tests: Optional[str] = None

    def has_tdd_structure(self) -> bool:
        """Check if workshop has TDD structure"""
        return self.phases is not None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'difficulty': self.difficulty,
            'estimated_minutes': self.estimated_minutes,
        }

        # Add TDD structure if present
        if self.phases:
            data['phases'] = self.phases.to_dict()

        # Add TDD workflow if present
        if self.tdd_workflow:
            data['tdd_workflow'] = self.tdd_workflow.to_dict()

        # Add backward compatibility fields
        if self.prompt:
            data['prompt'] = self.prompt
        if self.starter_code:
            data['starter_code'] = self.starter_code
        if self.hints:
            data['hints'] = self.hints
        if self.tests:
            data['tests'] = self.tests

        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Workshop':
        """Create from dictionary"""
        phases = None
        if data.get('phases'):
            phases = WorkshopPhases.from_dict(data['phases'])

        tdd_workflow = None
        if data.get('tdd_workflow'):
            tdd_workflow = TDDWorkflowDefinition.from_dict(data['tdd_workflow'])

        return cls(
            id=data['id'],
            title=data['title'],
            description=data['description'],
            difficulty=data.get('difficulty', 'beginner'),
            estimated_minutes=data.get('estimated_minutes', 15),
            phases=phases,
            tdd_workflow=tdd_workflow,
            prompt=data.get('prompt'),
            starter_code=data.get('starter_code'),
            hints=data.get('hints', []),
            tests=data.get('tests'),
        )

