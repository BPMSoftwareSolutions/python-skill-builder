"""
TDD Workflow Schema
Defines the structure for step-by-step TDD workflow definitions
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class StepContent:
    """
    Content for a single TDD step
    
    Attributes:
        objective: Learning goal for this step
        instruction: What the user should do
        requirements: Checklist items for success
        starter_code: Initial code template
        example_code: Example solution
        hints: Progressive hints (general → specific → example → solution)
        success_criteria: How to know you succeeded
        error_messages: Common errors and explanations
    """
    objective: str
    instruction: str
    requirements: List[str] = field(default_factory=list)
    starter_code: str = ""
    example_code: str = ""
    hints: List[str] = field(default_factory=list)
    success_criteria: List[str] = field(default_factory=list)
    error_messages: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'objective': self.objective,
            'instruction': self.instruction,
            'requirements': self.requirements,
            'starter_code': self.starter_code,
            'example_code': self.example_code,
            'hints': self.hints,
            'success_criteria': self.success_criteria,
            'error_messages': self.error_messages,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StepContent':
        """Create from dictionary"""
        return cls(
            objective=data.get('objective', ''),
            instruction=data.get('instruction', ''),
            requirements=data.get('requirements', []),
            starter_code=data.get('starter_code', ''),
            example_code=data.get('example_code', ''),
            hints=data.get('hints', []),
            success_criteria=data.get('success_criteria', []),
            error_messages=data.get('error_messages', {}),
        )


@dataclass
class TDDWorkflowDefinition:
    """
    Complete TDD workflow for a workshop
    
    Attributes:
        feature_description: Description of the feature to build (e.g., "add(a, b) - Add two numbers")
        step_1_red_write_test: RED phase - Write a failing test
        step_2_red_validation: RED phase - Validate test syntax and failure
        step_3_green_write_code: GREEN phase - Write minimal code
        step_4_green_validation: GREEN phase - Validate code passes test
        step_5_refactor_improve: REFACTOR phase - Improve code quality
        step_6_refactor_validation: REFACTOR phase - Validate refactoring
    """
    feature_description: str
    step_1_red_write_test: StepContent
    step_2_red_validation: Optional[StepContent] = None
    step_3_green_write_code: Optional[StepContent] = None
    step_4_green_validation: Optional[StepContent] = None
    step_5_refactor_improve: Optional[StepContent] = None
    step_6_refactor_validation: Optional[StepContent] = None

    def get_step(self, step_number: int) -> Optional[StepContent]:
        """Get step content by step number (1-6)"""
        steps = {
            1: self.step_1_red_write_test,
            2: self.step_2_red_validation,
            3: self.step_3_green_write_code,
            4: self.step_4_green_validation,
            5: self.step_5_refactor_improve,
            6: self.step_6_refactor_validation,
        }
        return steps.get(step_number)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = {
            'feature_description': self.feature_description,
            'step_1_red_write_test': self.step_1_red_write_test.to_dict(),
        }
        
        # Add optional steps
        if self.step_2_red_validation:
            data['step_2_red_validation'] = self.step_2_red_validation.to_dict()
        if self.step_3_green_write_code:
            data['step_3_green_write_code'] = self.step_3_green_write_code.to_dict()
        if self.step_4_green_validation:
            data['step_4_green_validation'] = self.step_4_green_validation.to_dict()
        if self.step_5_refactor_improve:
            data['step_5_refactor_improve'] = self.step_5_refactor_improve.to_dict()
        if self.step_6_refactor_validation:
            data['step_6_refactor_validation'] = self.step_6_refactor_validation.to_dict()
        
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TDDWorkflowDefinition':
        """Create from dictionary"""
        return cls(
            feature_description=data.get('feature_description', ''),
            step_1_red_write_test=StepContent.from_dict(data.get('step_1_red_write_test', {})),
            step_2_red_validation=StepContent.from_dict(data['step_2_red_validation']) if data.get('step_2_red_validation') else None,
            step_3_green_write_code=StepContent.from_dict(data['step_3_green_write_code']) if data.get('step_3_green_write_code') else None,
            step_4_green_validation=StepContent.from_dict(data['step_4_green_validation']) if data.get('step_4_green_validation') else None,
            step_5_refactor_improve=StepContent.from_dict(data['step_5_refactor_improve']) if data.get('step_5_refactor_improve') else None,
            step_6_refactor_validation=StepContent.from_dict(data['step_6_refactor_validation']) if data.get('step_6_refactor_validation') else None,
        )

