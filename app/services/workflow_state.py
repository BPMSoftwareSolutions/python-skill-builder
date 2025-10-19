"""
TDD Workflow State Machine
Manages the 6-step TDD workflow progression for workshops.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime


class TDDWorkflowState:
    """
    Manages workflow progression through 6 steps of the TDD cycle:
    1. RED: Write a Test
    2. RED Validation: System validates test
    3. GREEN: Write Code
    4. GREEN Validation: System validates code
    5. REFACTOR: Improve Code
    6. REFACTOR Validation: System validates refactoring
    """

    # Step definitions
    STEPS = {
        1: {"name": "RED: Write a Test", "phase": "RED"},
        2: {"name": "RED Validation", "phase": "RED"},
        3: {"name": "GREEN: Write Code", "phase": "GREEN"},
        4: {"name": "GREEN Validation", "phase": "GREEN"},
        5: {"name": "REFACTOR: Improve Code", "phase": "REFACTOR"},
        6: {"name": "REFACTOR Validation", "phase": "REFACTOR"},
    }

    def __init__(self, workshop_id: str):
        """
        Initialize workflow state for a workshop.
        
        Args:
            workshop_id: Unique identifier for the workshop
        """
        self.workshop_id = workshop_id
        self.current_step = 1
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        
        # Track completion status per step
        self.step_status = {
            i: {
                "completed": False,
                "locked": i > 1,  # Only step 1 is unlocked initially
                "code": "",
                "validation_result": None,
                "attempts": 0,
                "completed_at": None
            }
            for i in range(1, 7)
        }

    def get_current_step(self) -> int:
        """Get the current step number (1-6)."""
        return self.current_step

    def can_advance_to_next_step(self) -> bool:
        """
        Check if user can advance to the next step.
        Requirements:
        - Current step must be completed
        - Current step must have valid validation result
        """
        if self.current_step >= 6:
            return False
        
        current_status = self.step_status[self.current_step]
        return current_status["completed"] and current_status["validation_result"] is not None

    def advance_to_next_step(self) -> bool:
        """
        Advance to the next step if requirements are met.
        
        Returns:
            True if advanced, False if requirements not met
        """
        if not self.can_advance_to_next_step():
            return False
        
        self.current_step += 1
        self.step_status[self.current_step]["locked"] = False
        self.updated_at = datetime.now().isoformat()
        return True

    def go_back_to_step(self, step_num: int) -> bool:
        """
        Go back to a previous step for editing.
        
        Args:
            step_num: Target step number (must be <= current step)
            
        Returns:
            True if successful, False if invalid step
        """
        if step_num < 1 or step_num > self.current_step:
            return False
        
        self.current_step = step_num
        self.updated_at = datetime.now().isoformat()
        return True

    def mark_step_complete(self, step_num: int, validation_result: Dict) -> None:
        """
        Mark a step as complete with validation results.
        
        Args:
            step_num: Step number to mark complete
            validation_result: Validation result dictionary
        """
        if step_num not in self.step_status:
            return
        
        self.step_status[step_num]["completed"] = True
        self.step_status[step_num]["validation_result"] = validation_result
        self.step_status[step_num]["completed_at"] = datetime.now().isoformat()
        self.step_status[step_num]["attempts"] += 1
        self.updated_at = datetime.now().isoformat()

    def set_step_code(self, step_num: int, code: str) -> None:
        """
        Store code for a specific step.
        
        Args:
            step_num: Step number
            code: Code content
        """
        if step_num in self.step_status:
            self.step_status[step_num]["code"] = code
            self.updated_at = datetime.now().isoformat()

    def get_step_code(self, step_num: int) -> str:
        """Get code for a specific step."""
        if step_num in self.step_status:
            return self.step_status[step_num]["code"]
        return ""

    def get_step_status(self, step_num: int) -> Dict:
        """Get status of a specific step."""
        if step_num in self.step_status:
            return self.step_status[step_num].copy()
        return {}

    def get_all_steps_status(self) -> List[Dict]:
        """Get status of all steps."""
        result = []
        for i in range(1, 7):
            status = self.step_status[i].copy()
            status["step"] = i
            status["name"] = self.STEPS[i]["name"]
            status["phase"] = self.STEPS[i]["phase"]
            result.append(status)
        return result

    def to_dict(self) -> Dict:
        """Serialize workflow state to dictionary."""
        return {
            "workshop_id": self.workshop_id,
            "current_step": self.current_step,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "step_status": self.step_status
        }

    @staticmethod
    def from_dict(data: Dict) -> "TDDWorkflowState":
        """Deserialize workflow state from dictionary."""
        workflow = TDDWorkflowState(data["workshop_id"])
        workflow.current_step = data["current_step"]
        workflow.created_at = data["created_at"]
        workflow.updated_at = data["updated_at"]

        # Convert string keys back to integers (JSON serialization converts keys to strings)
        step_status_data = data["step_status"]
        workflow.step_status = {
            int(k): v for k, v in step_status_data.items()
        }

        return workflow

