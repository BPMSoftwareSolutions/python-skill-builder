"""
Unit tests for WorkflowStorage class.
"""

import pytest
import os
import shutil
import tempfile
from app.services.workflow_storage import WorkflowStorage
from app.services.workflow_state import TDDWorkflowState


class TestWorkflowStorageInitialization:
    """Test workflow storage initialization."""

    def test_storage_initialization(self):
        """Test creating a workflow storage instance."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = WorkflowStorage(tmpdir)
            
            assert os.path.exists(tmpdir)

    def test_storage_creates_directory(self):
        """Test that storage creates directory if it doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage_dir = os.path.join(tmpdir, "workflows")
            storage = WorkflowStorage(storage_dir)
            
            assert os.path.exists(storage_dir)


class TestWorkflowStorageSaveLoad:
    """Test saving and loading workflows."""

    def setup_method(self):
        """Set up test fixtures."""
        self.tmpdir = tempfile.mkdtemp()
        self.storage = WorkflowStorage(self.tmpdir)

    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_save_workflow(self):
        """Test saving a workflow."""
        workflow = TDDWorkflowState("workshop_123")
        workflow.set_step_code(1, "test code")
        
        self.storage.save_workflow("workflow_1", workflow)
        
        path = os.path.join(self.tmpdir, "workflow_1.json")
        assert os.path.exists(path)

    def test_load_workflow(self):
        """Test loading a saved workflow."""
        workflow = TDDWorkflowState("workshop_123")
        workflow.set_step_code(1, "test code")
        self.storage.save_workflow("workflow_1", workflow)
        
        loaded = self.storage.load_workflow("workflow_1")
        
        assert loaded is not None
        assert loaded.workshop_id == "workshop_123"
        assert loaded.get_step_code(1) == "test code"

    def test_load_nonexistent_workflow(self):
        """Test loading a workflow that doesn't exist."""
        loaded = self.storage.load_workflow("nonexistent")
        
        assert loaded is None

    def test_save_and_load_preserves_state(self):
        """Test that save and load preserve workflow state."""
        workflow = TDDWorkflowState("workshop_123")
        workflow.current_step = 3
        workflow.set_step_code(1, "test code")
        workflow.set_step_code(3, "impl code")
        workflow.mark_step_complete(1, {"valid": True})
        
        self.storage.save_workflow("workflow_1", workflow)
        loaded = self.storage.load_workflow("workflow_1")
        
        assert loaded.get_current_step() == 3
        assert loaded.get_step_code(1) == "test code"
        assert loaded.get_step_code(3) == "impl code"
        assert loaded.get_step_status(1)["completed"] is True


class TestWorkflowStorageDelete:
    """Test deleting workflows."""

    def setup_method(self):
        """Set up test fixtures."""
        self.tmpdir = tempfile.mkdtemp()
        self.storage = WorkflowStorage(self.tmpdir)

    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_delete_workflow(self):
        """Test deleting a workflow."""
        workflow = TDDWorkflowState("workshop_123")
        self.storage.save_workflow("workflow_1", workflow)
        
        result = self.storage.delete_workflow("workflow_1")
        
        assert result is True
        path = os.path.join(self.tmpdir, "workflow_1.json")
        assert not os.path.exists(path)

    def test_delete_nonexistent_workflow(self):
        """Test deleting a workflow that doesn't exist."""
        result = self.storage.delete_workflow("nonexistent")
        
        assert result is False


class TestWorkflowStorageList:
    """Test listing workflows."""

    def setup_method(self):
        """Set up test fixtures."""
        self.tmpdir = tempfile.mkdtemp()
        self.storage = WorkflowStorage(self.tmpdir)

    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_list_empty_storage(self):
        """Test listing workflows from empty storage."""
        workflows = self.storage.list_workflows()
        
        assert workflows == []

    def test_list_workflows(self):
        """Test listing multiple workflows."""
        workflow1 = TDDWorkflowState("workshop_123")
        workflow2 = TDDWorkflowState("workshop_456")
        
        self.storage.save_workflow("workflow_1", workflow1)
        self.storage.save_workflow("workflow_2", workflow2)
        
        workflows = self.storage.list_workflows()
        
        assert len(workflows) == 2
        assert "workflow_1" in workflows
        assert "workflow_2" in workflows

    def test_list_workflows_sorted(self):
        """Test that listed workflows are sorted."""
        for i in range(5, 0, -1):
            workflow = TDDWorkflowState(f"workshop_{i}")
            self.storage.save_workflow(f"workflow_{i}", workflow)
        
        workflows = self.storage.list_workflows()
        
        assert workflows == ["workflow_1", "workflow_2", "workflow_3", "workflow_4", "workflow_5"]


class TestWorkflowStorageExists:
    """Test checking workflow existence."""

    def setup_method(self):
        """Set up test fixtures."""
        self.tmpdir = tempfile.mkdtemp()
        self.storage = WorkflowStorage(self.tmpdir)

    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_workflow_exists(self):
        """Test checking if workflow exists."""
        workflow = TDDWorkflowState("workshop_123")
        self.storage.save_workflow("workflow_1", workflow)
        
        exists = self.storage.workflow_exists("workflow_1")
        
        assert exists is True

    def test_workflow_not_exists(self):
        """Test checking if nonexistent workflow exists."""
        exists = self.storage.workflow_exists("nonexistent")
        
        assert exists is False

