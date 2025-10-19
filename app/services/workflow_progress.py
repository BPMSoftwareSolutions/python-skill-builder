"""
Workflow Progress Tracking
Tracks user progress through TDD workflows with persistence.
"""

from typing import Dict, List, Optional
from datetime import datetime


class WorkflowProgress:
    """
    Tracks user progress through a TDD workflow.
    Persists completion status, code, validation results, and metrics.
    """

    def __init__(
        self,
        workflow_id: str,
        user_id: str,
        workshop_id: str,
    ):
        """
        Initialize workflow progress tracking.
        
        Args:
            workflow_id: Unique workflow identifier
            user_id: User identifier
            workshop_id: Workshop identifier
        """
        self.workflow_id = workflow_id
        self.user_id = user_id
        self.workshop_id = workshop_id
        self.current_step = 1
        self.steps_completed: List[int] = []
        self.code_per_step: Dict[int, str] = {i: "" for i in range(1, 7)}
        self.validation_results: Dict[int, Dict] = {}
        self.started_at = datetime.now().isoformat()
        self.last_updated_at = datetime.now().isoformat()
        self.completed_at: Optional[str] = None
        self.time_spent_seconds = 0
        self.hints_used: Dict[int, int] = {i: 0 for i in range(1, 7)}
        self.attempts_per_step: Dict[int, int] = {i: 0 for i in range(1, 7)}

    def mark_step_complete(self, step_num: int, validation_result: Dict) -> None:
        """
        Mark a step as complete.
        
        Args:
            step_num: Step number (1-6)
            validation_result: Validation result dictionary
        """
        if step_num not in self.steps_completed:
            self.steps_completed.append(step_num)
        
        self.validation_results[step_num] = validation_result
        self.attempts_per_step[step_num] += 1
        self.last_updated_at = datetime.now().isoformat()

    def set_step_code(self, step_num: int, code: str) -> None:
        """
        Store code for a step.
        
        Args:
            step_num: Step number (1-6)
            code: Code content
        """
        if 1 <= step_num <= 6:
            self.code_per_step[step_num] = code
            self.last_updated_at = datetime.now().isoformat()

    def increment_hint_usage(self, step_num: int) -> None:
        """
        Increment hint usage count for a step.
        
        Args:
            step_num: Step number (1-6)
        """
        if 1 <= step_num <= 6:
            self.hints_used[step_num] += 1
            self.last_updated_at = datetime.now().isoformat()

    def mark_workflow_complete(self) -> None:
        """Mark the entire workflow as complete."""
        self.completed_at = datetime.now().isoformat()
        self.last_updated_at = self.completed_at

    def is_complete(self) -> bool:
        """Check if workflow is complete (all 6 steps done)."""
        return len(self.steps_completed) == 6

    def get_completion_percentage(self) -> float:
        """Get workflow completion percentage (0-100)."""
        return (len(self.steps_completed) / 6) * 100

    def get_total_hints_used(self) -> int:
        """Get total hints used across all steps."""
        return sum(self.hints_used.values())

    def get_total_attempts(self) -> int:
        """Get total attempts across all steps."""
        return sum(self.attempts_per_step.values())

    def to_dict(self) -> Dict:
        """Serialize progress to dictionary."""
        return {
            "workflow_id": self.workflow_id,
            "user_id": self.user_id,
            "workshop_id": self.workshop_id,
            "current_step": self.current_step,
            "steps_completed": self.steps_completed,
            "code_per_step": self.code_per_step,
            "validation_results": self.validation_results,
            "started_at": self.started_at,
            "last_updated_at": self.last_updated_at,
            "completed_at": self.completed_at,
            "time_spent_seconds": self.time_spent_seconds,
            "hints_used": self.hints_used,
            "attempts_per_step": self.attempts_per_step,
        }

    @staticmethod
    def from_dict(data: Dict) -> "WorkflowProgress":
        """Deserialize progress from dictionary."""
        progress = WorkflowProgress(
            data["workflow_id"],
            data["user_id"],
            data["workshop_id"],
        )
        progress.current_step = data.get("current_step", 1)
        progress.steps_completed = data.get("steps_completed", [])
        progress.code_per_step = data.get("code_per_step", {i: "" for i in range(1, 7)})
        progress.validation_results = data.get("validation_results", {})
        progress.started_at = data.get("started_at", datetime.now().isoformat())
        progress.last_updated_at = data.get("last_updated_at", datetime.now().isoformat())
        progress.completed_at = data.get("completed_at")
        progress.time_spent_seconds = data.get("time_spent_seconds", 0)
        progress.hints_used = data.get("hints_used", {i: 0 for i in range(1, 7)})
        progress.attempts_per_step = data.get("attempts_per_step", {i: 0 for i in range(1, 7)})
        
        return progress

