"""
Workflow Storage Service
Persists and retrieves workflow state using JSON files.
"""

import json
import os
from typing import Dict, List, Optional
from .workflow_state import TDDWorkflowState


class WorkflowStorage:
    """
    Manages persistence of workflow state to JSON files.
    """

    def __init__(self, storage_dir: str = "workflows"):
        """
        Initialize workflow storage.
        
        Args:
            storage_dir: Directory to store workflow JSON files
        """
        self.storage_dir = storage_dir
        self._ensure_storage_dir()

    def _ensure_storage_dir(self) -> None:
        """Create storage directory if it doesn't exist."""
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir, exist_ok=True)

    def _get_workflow_path(self, workflow_id: str) -> str:
        """Get file path for a workflow."""
        return os.path.join(self.storage_dir, f"{workflow_id}.json")

    def save_workflow(self, workflow_id: str, state: TDDWorkflowState) -> None:
        """
        Save workflow state to JSON file.
        
        Args:
            workflow_id: Unique workflow identifier
            state: TDDWorkflowState instance to save
        """
        path = self._get_workflow_path(workflow_id)
        data = state.to_dict()
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def load_workflow(self, workflow_id: str) -> Optional[TDDWorkflowState]:
        """
        Load workflow state from JSON file.
        
        Args:
            workflow_id: Unique workflow identifier
            
        Returns:
            TDDWorkflowState instance or None if not found
        """
        path = self._get_workflow_path(workflow_id)
        
        if not os.path.exists(path):
            return None
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return TDDWorkflowState.from_dict(data)
        except (json.JSONDecodeError, KeyError) as e:
            return None

    def delete_workflow(self, workflow_id: str) -> bool:
        """
        Delete workflow state file.
        
        Args:
            workflow_id: Unique workflow identifier
            
        Returns:
            True if deleted, False if not found
        """
        path = self._get_workflow_path(workflow_id)
        
        if not os.path.exists(path):
            return False
        
        try:
            os.remove(path)
            return True
        except OSError:
            return False

    def list_workflows(self, user_id: str = None) -> List[str]:
        """
        List all workflow IDs in storage.
        
        Args:
            user_id: Optional user filter (for future multi-user support)
            
        Returns:
            List of workflow IDs
        """
        if not os.path.exists(self.storage_dir):
            return []
        
        workflows = []
        for filename in os.listdir(self.storage_dir):
            if filename.endswith('.json'):
                workflow_id = filename[:-5]  # Remove .json extension
                workflows.append(workflow_id)
        
        return sorted(workflows)

    def workflow_exists(self, workflow_id: str) -> bool:
        """
        Check if a workflow exists.
        
        Args:
            workflow_id: Unique workflow identifier
            
        Returns:
            True if workflow exists
        """
        path = self._get_workflow_path(workflow_id)
        return os.path.exists(path)

