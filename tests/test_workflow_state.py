"""
Unit tests for TDDWorkflowState class.
"""

import pytest
from app.services.workflow_state import TDDWorkflowState


class TestTDDWorkflowStateInitialization:
    """Test workflow state initialization."""

    def test_workflow_state_initialization(self):
        """Test creating a new workflow state."""
        workflow = TDDWorkflowState("workshop_123")
        
        assert workflow.workshop_id == "workshop_123"
        assert workflow.get_current_step() == 1
        assert workflow.step_status[1]["locked"] is False
        assert workflow.step_status[2]["locked"] is True

    def test_workflow_state_all_steps_initialized(self):
        """Test that all 6 steps are initialized."""
        workflow = TDDWorkflowState("workshop_123")
        
        for i in range(1, 7):
            assert i in workflow.step_status
            assert workflow.step_status[i]["completed"] is False
            assert workflow.step_status[i]["code"] == ""
            assert workflow.step_status[i]["validation_result"] is None


class TestWorkflowStepProgression:
    """Test step progression logic."""

    def test_can_advance_when_step_complete(self):
        """Test that we can advance when current step is complete."""
        workflow = TDDWorkflowState("workshop_123")
        
        # Mark step 1 as complete
        workflow.mark_step_complete(1, {"valid": True})
        
        assert workflow.can_advance_to_next_step() is True

    def test_cannot_advance_when_step_incomplete(self):
        """Test that we cannot advance when current step is incomplete."""
        workflow = TDDWorkflowState("workshop_123")
        
        assert workflow.can_advance_to_next_step() is False

    def test_advance_to_next_step(self):
        """Test advancing to the next step."""
        workflow = TDDWorkflowState("workshop_123")
        
        # Mark step 1 as complete
        workflow.mark_step_complete(1, {"valid": True})
        
        # Advance
        result = workflow.advance_to_next_step()
        
        assert result is True
        assert workflow.get_current_step() == 2
        assert workflow.step_status[2]["locked"] is False

    def test_cannot_advance_past_step_6(self):
        """Test that we cannot advance past step 6."""
        workflow = TDDWorkflowState("workshop_123")
        workflow.current_step = 6
        
        assert workflow.can_advance_to_next_step() is False

    def test_advance_all_steps(self):
        """Test advancing through all 6 steps."""
        workflow = TDDWorkflowState("workshop_123")
        
        for step in range(1, 6):
            workflow.mark_step_complete(step, {"valid": True})
            assert workflow.advance_to_next_step() is True
            assert workflow.get_current_step() == step + 1


class TestWorkflowGoBack:
    """Test going back to previous steps."""

    def test_go_back_to_previous_step(self):
        """Test going back to a previous step."""
        workflow = TDDWorkflowState("workshop_123")
        workflow.current_step = 3
        
        result = workflow.go_back_to_step(1)
        
        assert result is True
        assert workflow.get_current_step() == 1

    def test_cannot_go_back_beyond_step_1(self):
        """Test that we cannot go back before step 1."""
        workflow = TDDWorkflowState("workshop_123")
        
        result = workflow.go_back_to_step(0)
        
        assert result is False
        assert workflow.get_current_step() == 1

    def test_cannot_go_forward_with_go_back(self):
        """Test that go_back cannot advance beyond current step."""
        workflow = TDDWorkflowState("workshop_123")
        workflow.current_step = 2
        
        result = workflow.go_back_to_step(5)
        
        assert result is False
        assert workflow.get_current_step() == 2


class TestWorkflowStepCompletion:
    """Test step completion tracking."""

    def test_mark_step_complete(self):
        """Test marking a step as complete."""
        workflow = TDDWorkflowState("workshop_123")
        validation_result = {"valid": True, "errors": []}
        
        workflow.mark_step_complete(1, validation_result)
        
        status = workflow.get_step_status(1)
        assert status["completed"] is True
        assert status["validation_result"] == validation_result
        assert status["attempts"] == 1

    def test_mark_step_complete_increments_attempts(self):
        """Test that marking complete increments attempts."""
        workflow = TDDWorkflowState("workshop_123")
        
        workflow.mark_step_complete(1, {"valid": False})
        workflow.mark_step_complete(1, {"valid": True})
        
        status = workflow.get_step_status(1)
        assert status["attempts"] == 2


class TestWorkflowCodeStorage:
    """Test code storage per step."""

    def test_set_and_get_step_code(self):
        """Test storing and retrieving code for a step."""
        workflow = TDDWorkflowState("workshop_123")
        code = "def test_example():\n    assert True"
        
        workflow.set_step_code(1, code)
        
        assert workflow.get_step_code(1) == code

    def test_get_empty_code_for_unset_step(self):
        """Test that unset steps return empty code."""
        workflow = TDDWorkflowState("workshop_123")
        
        assert workflow.get_step_code(1) == ""

    def test_code_per_step_independent(self):
        """Test that code is independent per step."""
        workflow = TDDWorkflowState("workshop_123")
        
        workflow.set_step_code(1, "test code")
        workflow.set_step_code(3, "implementation code")
        
        assert workflow.get_step_code(1) == "test code"
        assert workflow.get_step_code(3) == "implementation code"


class TestWorkflowSerialization:
    """Test serialization and deserialization."""

    def test_to_dict(self):
        """Test converting workflow to dictionary."""
        workflow = TDDWorkflowState("workshop_123")
        workflow.set_step_code(1, "test code")
        workflow.mark_step_complete(1, {"valid": True})
        
        data = workflow.to_dict()
        
        assert data["workshop_id"] == "workshop_123"
        assert data["current_step"] == 1
        assert "created_at" in data
        assert "updated_at" in data
        assert "step_status" in data

    def test_from_dict(self):
        """Test creating workflow from dictionary."""
        original = TDDWorkflowState("workshop_123")
        original.set_step_code(1, "test code")
        original.mark_step_complete(1, {"valid": True})
        
        data = original.to_dict()
        restored = TDDWorkflowState.from_dict(data)
        
        assert restored.workshop_id == original.workshop_id
        assert restored.get_current_step() == original.get_current_step()
        assert restored.get_step_code(1) == original.get_step_code(1)

    def test_round_trip_serialization(self):
        """Test that serialization round-trip preserves state."""
        workflow = TDDWorkflowState("workshop_123")
        workflow.current_step = 3
        workflow.set_step_code(1, "test code")
        workflow.set_step_code(3, "impl code")
        workflow.mark_step_complete(1, {"valid": True})
        
        data = workflow.to_dict()
        restored = TDDWorkflowState.from_dict(data)
        
        assert restored.get_current_step() == 3
        assert restored.get_step_code(1) == "test code"
        assert restored.get_step_code(3) == "impl code"
        assert restored.get_step_status(1)["completed"] is True


class TestWorkflowStatusReporting:
    """Test status reporting methods."""

    def test_get_step_status(self):
        """Test getting status of a specific step."""
        workflow = TDDWorkflowState("workshop_123")
        
        status = workflow.get_step_status(1)
        
        assert "completed" in status
        assert "locked" in status
        assert "code" in status
        assert "validation_result" in status
        assert "attempts" in status

    def test_get_all_steps_status(self):
        """Test getting status of all steps."""
        workflow = TDDWorkflowState("workshop_123")
        
        all_status = workflow.get_all_steps_status()
        
        assert len(all_status) == 6
        for i, status in enumerate(all_status, 1):
            assert status["step"] == i
            assert "name" in status
            assert "phase" in status

    def test_all_steps_status_includes_metadata(self):
        """Test that all steps status includes step metadata."""
        workflow = TDDWorkflowState("workshop_123")
        
        all_status = workflow.get_all_steps_status()
        
        # Check first step
        assert all_status[0]["name"] == "RED: Write a Test"
        assert all_status[0]["phase"] == "RED"
        
        # Check third step
        assert all_status[2]["name"] == "GREEN: Write Code"
        assert all_status[2]["phase"] == "GREEN"
        
        # Check fifth step
        assert all_status[4]["name"] == "REFACTOR: Improve Code"
        assert all_status[4]["phase"] == "REFACTOR"

