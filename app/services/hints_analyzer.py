"""
Hints Analyzer Service
Provides context-aware hints based on current step and errors
"""

from typing import List, Dict, Optional, Any
from app.schemas.tdd_workflow import TDDWorkflowDefinition, StepContent


class HintsAnalyzer:
    """Analyzes errors and provides progressive hints"""

    def __init__(self, workflow: Optional[TDDWorkflowDefinition] = None):
        """
        Initialize hints analyzer
        
        Args:
            workflow: TDD workflow definition
        """
        self.workflow = workflow

    def get_hints_for_step(self, step: int) -> List[str]:
        """
        Get all hints for a specific step
        
        Args:
            step: Step number (1-6)
            
        Returns:
            List of hints for the step
        """
        if not self.workflow:
            return []
        
        step_content = self.workflow.get_step(step)
        if not step_content:
            return []
        
        return step_content.hints

    def get_progressive_hints(self, step: int, hint_level: int) -> List[str]:
        """
        Get progressive hints at a specific level
        
        Args:
            step: Step number (1-6)
            hint_level: Hint level (1-4)
                - Level 1: General guidance
                - Level 2: Specific hint
                - Level 3: Example code
                - Level 4: Full solution
                
        Returns:
            List of hints up to the specified level
        """
        if not self.workflow:
            return []
        
        step_content = self.workflow.get_step(step)
        if not step_content:
            return []
        
        hints = []
        
        # Level 1: General hints
        if hint_level >= 1:
            hints.extend(step_content.hints[:1] if step_content.hints else [])
        
        # Level 2: More specific hints
        if hint_level >= 2:
            hints.extend(step_content.hints[1:2] if len(step_content.hints) > 1 else [])
        
        # Level 3: Example code
        if hint_level >= 3 and step_content.example_code:
            hints.append(f"Example:\n{step_content.example_code}")
        
        # Level 4: Full solution
        if hint_level >= 4 and step_content.example_code:
            hints.append(f"Solution:\n{step_content.example_code}")
        
        return hints

    def analyze_error_and_suggest_hints(self, step: int, error: str) -> List[str]:
        """
        Analyze an error and suggest relevant hints
        
        Args:
            step: Step number (1-6)
            error: Error message or code
            
        Returns:
            List of suggested hints
        """
        if not self.workflow:
            return []
        
        step_content = self.workflow.get_step(step)
        if not step_content:
            return []
        
        suggestions = []
        
        # Check error messages mapping
        for error_code, error_message in step_content.error_messages.items():
            if error_code.lower() in error.lower() or error.lower() in error_code.lower():
                suggestions.append(error_message)
        
        # If no specific error match, return general hints
        if not suggestions:
            suggestions = step_content.hints[:2] if step_content.hints else []
        
        return suggestions

    def get_example_code(self, step: int) -> Optional[str]:
        """
        Get example code for a step
        
        Args:
            step: Step number (1-6)
            
        Returns:
            Example code or None
        """
        if not self.workflow:
            return None
        
        step_content = self.workflow.get_step(step)
        if not step_content:
            return None
        
        return step_content.example_code if step_content.example_code else None

    def get_solution_code(self, step: int) -> Optional[str]:
        """
        Get solution code for a step (same as example code)
        
        Args:
            step: Step number (1-6)
            
        Returns:
            Solution code or None
        """
        return self.get_example_code(step)

    def get_starter_code(self, step: int) -> Optional[str]:
        """
        Get starter code for a step
        
        Args:
            step: Step number (1-6)
            
        Returns:
            Starter code or None
        """
        if not self.workflow:
            return None
        
        step_content = self.workflow.get_step(step)
        if not step_content:
            return None
        
        return step_content.starter_code if step_content.starter_code else None

    def get_step_requirements(self, step: int) -> List[str]:
        """
        Get requirements checklist for a step
        
        Args:
            step: Step number (1-6)
            
        Returns:
            List of requirements
        """
        if not self.workflow:
            return []
        
        step_content = self.workflow.get_step(step)
        if not step_content:
            return []
        
        return step_content.requirements

    def get_success_criteria(self, step: int) -> List[str]:
        """
        Get success criteria for a step
        
        Args:
            step: Step number (1-6)
            
        Returns:
            List of success criteria
        """
        if not self.workflow:
            return []
        
        step_content = self.workflow.get_step(step)
        if not step_content:
            return []
        
        return step_content.success_criteria

    def get_step_objective(self, step: int) -> Optional[str]:
        """
        Get objective for a step
        
        Args:
            step: Step number (1-6)
            
        Returns:
            Step objective or None
        """
        if not self.workflow:
            return None
        
        step_content = self.workflow.get_step(step)
        if not step_content:
            return None
        
        return step_content.objective

    def get_step_instruction(self, step: int) -> Optional[str]:
        """
        Get instruction for a step
        
        Args:
            step: Step number (1-6)
            
        Returns:
            Step instruction or None
        """
        if not self.workflow:
            return None
        
        step_content = self.workflow.get_step(step)
        if not step_content:
            return None
        
        return step_content.instruction

