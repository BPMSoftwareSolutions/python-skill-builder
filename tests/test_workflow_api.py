"""
Unit tests for Workflow API endpoints.
"""

import pytest
import json
import tempfile
import shutil
from main import app
from app.services.workflow_storage import WorkflowStorage


@pytest.fixture
def client():
    """Create a test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def temp_workflows():
    """Create temporary workflows directory."""
    tmpdir = tempfile.mkdtemp()
    original_storage_dir = None
    
    # Monkey patch the storage directory
    import main
    original_storage_dir = main.workflow_storage.storage_dir
    main.workflow_storage.storage_dir = tmpdir
    
    yield tmpdir
    
    # Restore original
    main.workflow_storage.storage_dir = original_storage_dir
    shutil.rmtree(tmpdir, ignore_errors=True)


class TestWorkflowStartEndpoint:
    """Test POST /api/workshops/{id}/workflow/start endpoint."""

    def test_start_workflow(self, client, temp_workflows):
        """Test starting a new workflow."""
        response = client.post("/api/workshops/workshop_123/workflow/start")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["ok"] is True
        assert "workflow_id" in data
        assert data["current_step"] == 1
        assert "steps_status" in data

    def test_start_workflow_returns_all_steps(self, client, temp_workflows):
        """Test that start returns all 6 steps."""
        response = client.post("/api/workshops/workshop_123/workflow/start")
        
        data = json.loads(response.data)
        assert len(data["steps_status"]) == 6


class TestWorkflowGetEndpoint:
    """Test GET /api/workshops/{id}/workflow/{workflow_id} endpoint."""

    def test_get_workflow(self, client, temp_workflows):
        """Test getting workflow state."""
        # Start workflow
        start_response = client.post("/api/workshops/workshop_123/workflow/start")
        workflow_id = json.loads(start_response.data)["workflow_id"]
        
        # Get workflow
        response = client.get(f"/api/workshops/workshop_123/workflow/{workflow_id}")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["ok"] is True
        assert data["current_step"] == 1
        assert "steps_status" in data
        assert "code_per_step" in data

    def test_get_nonexistent_workflow(self, client, temp_workflows):
        """Test getting a nonexistent workflow."""
        response = client.get("/api/workshops/workshop_123/workflow/nonexistent")
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data["ok"] is False


class TestWorkflowValidateEndpoint:
    """Test POST /api/workshops/{id}/workflow/{workflow_id}/validate-step endpoint."""

    def test_validate_step_1(self, client, temp_workflows):
        """Test validating step 1."""
        # Start workflow
        start_response = client.post("/api/workshops/workshop_123/workflow/start")
        workflow_id = json.loads(start_response.data)["workflow_id"]
        
        # Validate step 1
        test_code = """
def test_add():
    assert 1 + 1 == 2
"""
        response = client.post(
            f"/api/workshops/workshop_123/workflow/{workflow_id}/validate-step",
            json={"step": 1, "code": test_code}
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["ok"] is True
        assert "valid" in data
        assert "validation_result" in data

    def test_validate_step_invalid_step(self, client, temp_workflows):
        """Test validating an invalid step."""
        # Start workflow
        start_response = client.post("/api/workshops/workshop_123/workflow/start")
        workflow_id = json.loads(start_response.data)["workflow_id"]
        
        # Validate invalid step
        response = client.post(
            f"/api/workshops/workshop_123/workflow/{workflow_id}/validate-step",
            json={"step": 99, "code": "pass"}
        )
        
        assert response.status_code == 400


class TestWorkflowAdvanceEndpoint:
    """Test POST /api/workshops/{id}/workflow/{workflow_id}/advance endpoint."""

    def test_advance_workflow(self, client, temp_workflows):
        """Test advancing to next step."""
        # Start workflow
        start_response = client.post("/api/workshops/workshop_123/workflow/start")
        workflow_id = json.loads(start_response.data)["workflow_id"]
        
        # Validate step 1 (mark as complete)
        test_code = """
def test_add():
    assert 1 + 1 == 2
"""
        client.post(
            f"/api/workshops/workshop_123/workflow/{workflow_id}/validate-step",
            json={"step": 1, "code": test_code}
        )
        
        # Advance
        response = client.post(
            f"/api/workshops/workshop_123/workflow/{workflow_id}/advance"
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["ok"] is True
        assert data["current_step"] == 2

    def test_cannot_advance_incomplete_step(self, client, temp_workflows):
        """Test that we cannot advance incomplete step."""
        # Start workflow
        start_response = client.post("/api/workshops/workshop_123/workflow/start")
        workflow_id = json.loads(start_response.data)["workflow_id"]
        
        # Try to advance without completing step 1
        response = client.post(
            f"/api/workshops/workshop_123/workflow/{workflow_id}/advance"
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data["ok"] is False


class TestWorkflowGoBackEndpoint:
    """Test POST /api/workshops/{id}/workflow/{workflow_id}/go-back endpoint."""

    def test_go_back_to_previous_step(self, client, temp_workflows):
        """Test going back to a previous step."""
        # Start workflow
        start_response = client.post("/api/workshops/workshop_123/workflow/start")
        workflow_id = json.loads(start_response.data)["workflow_id"]
        
        # Manually advance to step 3
        import main
        workflow = main.workflow_storage.load_workflow(workflow_id)
        workflow.current_step = 3
        main.workflow_storage.save_workflow(workflow_id, workflow)
        
        # Go back to step 1
        response = client.post(
            f"/api/workshops/workshop_123/workflow/{workflow_id}/go-back",
            json={"target_step": 1}
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["ok"] is True
        assert data["current_step"] == 1

    def test_cannot_go_back_invalid_step(self, client, temp_workflows):
        """Test that we cannot go back to invalid step."""
        # Start workflow
        start_response = client.post("/api/workshops/workshop_123/workflow/start")
        workflow_id = json.loads(start_response.data)["workflow_id"]
        
        # Try to go back to step 99
        response = client.post(
            f"/api/workshops/workshop_123/workflow/{workflow_id}/go-back",
            json={"target_step": 99}
        )
        
        assert response.status_code == 400


class TestWorkflowMetricsEndpoint:
    """Test GET /api/workshops/{id}/workflow/{workflow_id}/metrics endpoint."""

    def test_get_metrics(self, client, temp_workflows):
        """Test getting code metrics."""
        # Start workflow
        start_response = client.post("/api/workshops/workshop_123/workflow/start")
        workflow_id = json.loads(start_response.data)["workflow_id"]
        
        # Set code for current step
        import main
        workflow = main.workflow_storage.load_workflow(workflow_id)
        workflow.set_step_code(1, "def add(a, b): return a + b")
        main.workflow_storage.save_workflow(workflow_id, workflow)
        
        # Get metrics
        response = client.get(
            f"/api/workshops/workshop_123/workflow/{workflow_id}/metrics"
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["ok"] is True
        assert "complexity" in data
        assert "coverage" in data
        assert "duplication" in data
        assert "has_type_hints" in data
        assert "has_docstring" in data

    def test_get_metrics_nonexistent_workflow(self, client, temp_workflows):
        """Test getting metrics for nonexistent workflow."""
        response = client.get(
            "/api/workshops/workshop_123/workflow/nonexistent/metrics"
        )
        
        assert response.status_code == 404

