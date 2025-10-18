"""
Phase Guidance Schema
Defines guidance for RED, GREEN, and REFACTOR phases
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class RedPhaseGuidance:
    """
    RED Phase Guidance - Understanding Requirements
    
    Attributes:
        objective: Learning objective for RED phase
        guidance: Main guidance text
        hints: List of hints to help understand tests
        learning_objectives: Key concepts to learn
    """
    objective: str
    guidance: str
    hints: List[str] = field(default_factory=list)
    learning_objectives: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'objective': self.objective,
            'guidance': self.guidance,
            'hints': self.hints,
            'learning_objectives': self.learning_objectives,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RedPhaseGuidance':
        """Create from dictionary"""
        return cls(
            objective=data['objective'],
            guidance=data['guidance'],
            hints=data.get('hints', []),
            learning_objectives=data.get('learning_objectives', []),
        )


@dataclass
class GreenPhaseGuidance:
    """
    GREEN Phase Guidance - Making Tests Pass
    
    Attributes:
        objective: Learning objective for GREEN phase
        guidance: Main guidance text
        minimum_requirements: What must be satisfied
        hints: List of hints for implementation
        success_criteria: Criteria for success
    """
    objective: str
    guidance: str
    minimum_requirements: str
    hints: List[str] = field(default_factory=list)
    success_criteria: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'objective': self.objective,
            'guidance': self.guidance,
            'minimum_requirements': self.minimum_requirements,
            'hints': self.hints,
            'success_criteria': self.success_criteria,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GreenPhaseGuidance':
        """Create from dictionary"""
        return cls(
            objective=data['objective'],
            guidance=data['guidance'],
            minimum_requirements=data['minimum_requirements'],
            hints=data.get('hints', []),
            success_criteria=data.get('success_criteria', []),
        )


@dataclass
class RefactorPhaseGuidance:
    """
    REFACTOR Phase Guidance - Improving Code Quality
    
    Attributes:
        objective: Learning objective for REFACTOR phase
        guidance: Main guidance text
        guidelines: Code quality guidelines
        code_metrics: Target metrics for code quality
        mentor_solution: Reference implementation
        patterns: Design patterns to consider
    """
    objective: str
    guidance: str
    guidelines: List[str] = field(default_factory=list)
    code_metrics: Dict[str, Any] = field(default_factory=dict)
    mentor_solution: Optional[str] = None
    patterns: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'objective': self.objective,
            'guidance': self.guidance,
            'guidelines': self.guidelines,
            'code_metrics': self.code_metrics,
            'mentor_solution': self.mentor_solution,
            'patterns': self.patterns,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RefactorPhaseGuidance':
        """Create from dictionary"""
        return cls(
            objective=data['objective'],
            guidance=data['guidance'],
            guidelines=data.get('guidelines', []),
            code_metrics=data.get('code_metrics', {}),
            mentor_solution=data.get('mentor_solution'),
            patterns=data.get('patterns', []),
        )


@dataclass
class PhaseGuidance:
    """
    Complete phase guidance for all three TDD phases
    
    Attributes:
        red: RED phase guidance
        green: GREEN phase guidance
        refactor: REFACTOR phase guidance
    """
    red: RedPhaseGuidance
    green: GreenPhaseGuidance
    refactor: RefactorPhaseGuidance

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'red': self.red.to_dict(),
            'green': self.green.to_dict(),
            'refactor': self.refactor.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PhaseGuidance':
        """Create from dictionary"""
        return cls(
            red=RedPhaseGuidance.from_dict(data['red']),
            green=GreenPhaseGuidance.from_dict(data['green']),
            refactor=RefactorPhaseGuidance.from_dict(data['refactor']),
        )

