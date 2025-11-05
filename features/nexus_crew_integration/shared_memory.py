"""
Shared Memory System - Adapted from NEXUS_CREW

Session 14: NEXUS_CREW Integration
Provides SharedTask and GitHubMemorySync classes for bidirectional sync.
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional
from enum import Enum
from datetime import datetime
import json
import os


class TaskStatus(Enum):
    """Task status enumeration."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskPriority(Enum):
    """Task priority enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class SharedTask:
    """
    Shared task structure for NEXUS_CREW coordination.

    Represents a task that can be synced between CEREBRO and NEXUS_CREW agents.
    """
    task_id: str
    task_type: str
    description: str
    assigned_node: str
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    result: Optional[Dict] = None
    metadata: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary with enum values as strings."""
        data = asdict(self)
        data["status"] = self.status.value
        data["priority"] = self.priority.value
        return data

    @classmethod
    def from_dict(cls, data: Dict) -> "SharedTask":
        """Create SharedTask from dictionary."""
        # Convert string status/priority back to enums
        if isinstance(data.get("status"), str):
            data["status"] = TaskStatus(data["status"])
        if isinstance(data.get("priority"), str):
            data["priority"] = TaskPriority(data["priority"])
        return cls(**data)


class GitHubMemorySync:
    """
    File-based shared memory (simulates GitHub Issues).

    Provides CRUD operations for SharedTask objects stored as JSON files.
    """

    def __init__(self, storage_path: str = ".shared_memory"):
        """
        Initialize GitHubMemorySync.

        Args:
            storage_path: Directory to store task JSON files (default: .shared_memory)
        """
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)

    def create_task(self, task: SharedTask) -> bool:
        """
        Create or update a task.

        Args:
            task: SharedTask to create/update

        Returns:
            True if successful
        """
        filepath = os.path.join(self.storage_path, f"{task.task_id}.json")
        with open(filepath, 'w') as f:
            json.dump(task.to_dict(), f, indent=2)
        return True

    def get_task(self, task_id: str) -> Optional[SharedTask]:
        """
        Get task by ID.

        Args:
            task_id: Task ID

        Returns:
            SharedTask if found, None otherwise
        """
        filepath = os.path.join(self.storage_path, f"{task_id}.json")
        if not os.path.exists(filepath):
            return None

        with open(filepath, 'r') as f:
            data = json.load(f)

        return SharedTask.from_dict(data)

    def update_task_status(
        self,
        task_id: str,
        status: TaskStatus,
        result: Optional[Dict] = None
    ) -> bool:
        """
        Update task status and optionally result.

        Args:
            task_id: Task ID
            status: New TaskStatus
            result: Optional result dictionary

        Returns:
            True if successful, False if task not found
        """
        task = self.get_task(task_id)
        if not task:
            return False

        task.status = status
        task.updated_at = datetime.now().isoformat()
        if result:
            task.result = result

        return self.create_task(task)

    def search_tasks(
        self,
        status: Optional[TaskStatus] = None,
        assigned_node: Optional[str] = None
    ) -> List[SharedTask]:
        """
        Search tasks by filters.

        Args:
            status: Optional TaskStatus filter
            assigned_node: Optional assigned node filter

        Returns:
            List of matching SharedTask objects
        """
        tasks = []

        for filename in os.listdir(self.storage_path):
            if not filename.endswith('.json'):
                continue

            task_id = filename[:-5]  # Remove .json extension
            task = self.get_task(task_id)

            if task:
                # Apply filters
                if status and task.status != status:
                    continue
                if assigned_node and task.assigned_node != assigned_node:
                    continue

                tasks.append(task)

        return tasks

    def get_all_tasks(self) -> List[SharedTask]:
        """
        Get all tasks without filters.

        Returns:
            List of all SharedTask objects
        """
        return self.search_tasks()

    def delete_task(self, task_id: str) -> bool:
        """
        Delete task by ID.

        Args:
            task_id: Task ID

        Returns:
            True if deleted, False if not found
        """
        filepath = os.path.join(self.storage_path, f"{task_id}.json")
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False
