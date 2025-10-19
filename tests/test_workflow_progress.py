"""
Unit tests for WorkflowProgress class.
"""

import pytest
from datetime import datetime
from app.services.workflow_progress import WorkflowProgress


class TestWorkflowProgress:
    """Test WorkflowProgress class."""

    def test_init(self):
        """Test WorkflowProgress initialization."""
        progress = WorkflowProgress("wf1", "user1", "ws1")
        
        assert progress.workflow_id == "wf1"
        assert progress.user_id == "user1"
        assert progress.workshop_id == "ws1"
        assert progress.current_step == 1
        assert progress.steps_completed == []
        assert len(progress.code_per_step) == 6
        assert progress.completed_at is None
        assert progress.time_spent_seconds == 0

    def test_mark_step_complete(self):
        """Test marking a step as complete."""
        progress = WorkflowProgress("wf1", "user1", "ws1")
        validation_result = {"valid": True, "message": "Test passed"}
        
        progress.mark_step_complete(1, validation_result)
        
        assert 1 in progress.steps_completed
        assert progress.validation_results[1] == validation_result
        assert progress.attempts_per_step[1] == 1

    def test_mark_multiple_steps_complete(self):
        """Test marking multiple steps as complete."""
        progress = WorkflowProgress("wf1", "user1", "ws1")
        
        for step in range(1, 7):
            progress.mark_step_complete(step, {"valid": True})
        
        assert len(progress.steps_completed) == 6
        assert progress.is_complete()

    def test_set_step_code(self):
        """Test setting code for a step."""
        progress = WorkflowProgress("wf1", "user1", "ws1")
        code = "def test_example(): pass"
        
        progress.set_step_code(1, code)
        
        assert progress.code_per_step[1] == code

    def test_increment_hint_usage(self):
        """Test incrementing hint usage."""
        progress = WorkflowProgress("wf1", "user1", "ws1")
        
        progress.increment_hint_usage(1)
        progress.increment_hint_usage(1)
        progress.increment_hint_usage(2)
        
        assert progress.hints_used[1] == 2
        assert progress.hints_used[2] == 1

    def test_mark_workflow_complete(self):
        """Test marking workflow as complete."""
        progress = WorkflowProgress("wf1", "user1", "ws1")
        
        progress.mark_workflow_complete()
        
        assert progress.completed_at is not None
        assert progress.last_updated_at == progress.completed_at

    def test_is_complete(self):
        """Test is_complete method."""
        progress = WorkflowProgress("wf1", "user1", "ws1")
        
        assert not progress.is_complete()
        
        for step in range(1, 7):
            progress.mark_step_complete(step, {"valid": True})
        
        assert progress.is_complete()

    def test_get_completion_percentage(self):
        """Test completion percentage calculation."""
        progress = WorkflowProgress("wf1", "user1", "ws1")
        
        assert progress.get_completion_percentage() == 0.0
        
        progress.mark_step_complete(1, {"valid": True})
        assert progress.get_completion_percentage() == pytest.approx(16.67, 0.1)
        
        for step in range(2, 7):
            progress.mark_step_complete(step, {"valid": True})
        
        assert progress.get_completion_percentage() == 100.0

    def test_get_total_hints_used(self):
        """Test total hints used calculation."""
        progress = WorkflowProgress("wf1", "user1", "ws1")
        
        for step in range(1, 7):
            for _ in range(step):
                progress.increment_hint_usage(step)
        
        total = progress.get_total_hints_used()
        assert total == 1 + 2 + 3 + 4 + 5 + 6  # 21

    def test_get_total_attempts(self):
        """Test total attempts calculation."""
        progress = WorkflowProgress("wf1", "user1", "ws1")
        
        for step in range(1, 7):
            for _ in range(step):
                progress.mark_step_complete(step, {"valid": True})
        
        total = progress.get_total_attempts()
        assert total == 1 + 2 + 3 + 4 + 5 + 6  # 21

    def test_to_dict(self):
        """Test serialization to dictionary."""
        progress = WorkflowProgress("wf1", "user1", "ws1")
        progress.mark_step_complete(1, {"valid": True})
        
        data = progress.to_dict()
        
        assert data["workflow_id"] == "wf1"
        assert data["user_id"] == "user1"
        assert data["workshop_id"] == "ws1"
        assert data["current_step"] == 1
        assert 1 in data["steps_completed"]
        assert data["completed_at"] is None

    def test_from_dict(self):
        """Test deserialization from dictionary."""
        original = WorkflowProgress("wf1", "user1", "ws1")
        original.mark_step_complete(1, {"valid": True})
        original.set_step_code(1, "test code")
        
        data = original.to_dict()
        restored = WorkflowProgress.from_dict(data)
        
        assert restored.workflow_id == original.workflow_id
        assert restored.user_id == original.user_id
        assert restored.workshop_id == original.workshop_id
        assert restored.steps_completed == original.steps_completed
        assert restored.code_per_step[1] == "test code"

    def test_serialization_roundtrip(self):
        """Test that serialization and deserialization preserve data."""
        progress = WorkflowProgress("wf1", "user1", "ws1")
        
        for step in range(1, 4):
            progress.set_step_code(step, f"code for step {step}")
            progress.mark_step_complete(step, {"valid": True})
            for _ in range(step):
                progress.increment_hint_usage(step)
        
        data = progress.to_dict()
        restored = WorkflowProgress.from_dict(data)
        
        assert restored.to_dict() == data

