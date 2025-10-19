"""
Workflow Storage Service
Persists and retrieves workflow state using JSON files.
"""

import json
import os
from typing import Dict, List, Optional
from .workflow_state import TDDWorkflowState
from .workflow_progress import WorkflowProgress


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

    def _get_progress_path(self, user_id: str, workflow_id: str) -> str:
        """Get file path for workflow progress."""
        user_dir = os.path.join(self.storage_dir, user_id)
        return os.path.join(user_dir, f"{workflow_id}_progress.json")

    def _ensure_user_dir(self, user_id: str) -> None:
        """Create user directory if it doesn't exist."""
        user_dir = os.path.join(self.storage_dir, user_id)
        if not os.path.exists(user_dir):
            os.makedirs(user_dir, exist_ok=True)

    def save_progress(self, progress: WorkflowProgress) -> None:
        """
        Save workflow progress to JSON file.

        Args:
            progress: WorkflowProgress instance to save
        """
        self._ensure_user_dir(progress.user_id)
        path = self._get_progress_path(progress.user_id, progress.workflow_id)
        data = progress.to_dict()

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def load_progress(self, user_id: str, workflow_id: str) -> Optional[WorkflowProgress]:
        """
        Load workflow progress from JSON file.

        Args:
            user_id: User identifier
            workflow_id: Workflow identifier

        Returns:
            WorkflowProgress instance or None if not found
        """
        path = self._get_progress_path(user_id, workflow_id)

        if not os.path.exists(path):
            return None

        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return WorkflowProgress.from_dict(data)
        except (json.JSONDecodeError, KeyError):
            return None

    def delete_progress(self, user_id: str, workflow_id: str) -> bool:
        """
        Delete workflow progress file.

        Args:
            user_id: User identifier
            workflow_id: Workflow identifier

        Returns:
            True if deleted, False if not found
        """
        path = self._get_progress_path(user_id, workflow_id)

        if not os.path.exists(path):
            return False

        try:
            os.remove(path)
            return True
        except OSError:
            return False

    def list_user_workflows(self, user_id: str) -> List[str]:
        """
        List all workflow progress files for a user.

        Args:
            user_id: User identifier

        Returns:
            List of workflow IDs
        """
        user_dir = os.path.join(self.storage_dir, user_id)

        if not os.path.exists(user_dir):
            return []

        workflows = []
        for filename in os.listdir(user_dir):
            if filename.endswith('_progress.json'):
                workflow_id = filename[:-14]  # Remove _progress.json
                workflows.append(workflow_id)

        return sorted(workflows)

    def get_progress_stats(self, user_id: str) -> Dict:
        """
        Get aggregated statistics for all user workflows.

        Args:
            user_id: User identifier

        Returns:
            Dictionary with aggregated stats
        """
        workflow_ids = self.list_user_workflows(user_id)

        total_workflows = len(workflow_ids)
        completed_workflows = 0
        total_time_seconds = 0
        total_hints_used = 0
        total_attempts = 0

        for workflow_id in workflow_ids:
            progress = self.load_progress(user_id, workflow_id)
            if progress:
                if progress.is_complete():
                    completed_workflows += 1
                total_time_seconds += progress.time_spent_seconds
                total_hints_used += progress.get_total_hints_used()
                total_attempts += progress.get_total_attempts()

        return {
            "total_workflows": total_workflows,
            "completed_workflows": completed_workflows,
            "completion_rate": (completed_workflows / total_workflows * 100) if total_workflows > 0 else 0,
            "total_time_seconds": total_time_seconds,
            "total_hints_used": total_hints_used,
            "total_attempts": total_attempts,
            "average_time_per_workflow": (total_time_seconds / total_workflows) if total_workflows > 0 else 0,
            "average_hints_per_workflow": (total_hints_used / total_workflows) if total_workflows > 0 else 0,
            "average_attempts_per_workflow": (total_attempts / total_workflows) if total_workflows > 0 else 0,
        }

