"""
CerebroMemoryBridge - Bidirectional sync between CEREBRO and NEXUS_CREW

Session 14: NEXUS_CREW Integration - Part 1B
Implements: Bidirectional synchronization of episodic memory
"""

from typing import Dict, List, Optional, Set, Any
from datetime import datetime
import logging

from .cerebro_client import CerebroClient
from .shared_memory import SharedTask, TaskStatus, TaskPriority, GitHubMemorySync


# Setup logging
logger = logging.getLogger(__name__)


class CerebroMemoryBridge:
    """
    Bidirectional sync between CEREBRO and NEXUS_CREW shared memory.

    Provides:
    - Episode → Task conversion
    - Task → Episode conversion
    - CEREBRO → CREW sync
    - CREW → CEREBRO sync
    - Bidirectional sync
    - Duplicate prevention
    """

    def __init__(
        self,
        cerebro_base_url: str = "http://localhost:8003",
        shared_memory_path: str = ".shared_memory",
        sync_interval_seconds: int = 30,
        cerebro_tag_filter: str = "shared_with_crew"
    ):
        """
        Initialize CerebroMemoryBridge.

        Args:
            cerebro_base_url: Base URL of CEREBRO API (default: http://localhost:8003)
            shared_memory_path: Path to shared memory storage (default: .shared_memory)
            sync_interval_seconds: Sync interval in seconds (default: 30)
            cerebro_tag_filter: Tag to filter episodes for sync (default: shared_with_crew)
        """
        self.cerebro_base_url = cerebro_base_url
        self.shared_memory_path = shared_memory_path
        self.sync_interval = sync_interval_seconds
        self.cerebro_tag_filter = cerebro_tag_filter

        # Initialize clients
        self.cerebro_client = CerebroClient(cerebro_base_url)
        self.github_memory = GitHubMemorySync(shared_memory_path)

        # Track sync state (to prevent duplicates)
        self.synced_episodes: Set[str] = set()
        self.synced_tasks: Set[str] = set()
        self.last_sync_timestamp: Optional[datetime] = None

    def episode_to_task(self, episode: Dict) -> SharedTask:
        """
        Convert CEREBRO episode to NEXUS_CREW SharedTask.

        Args:
            episode: Episode dictionary from CEREBRO

        Returns:
            SharedTask object

        Raises:
            KeyError: If required fields are missing
            ValueError: If data is invalid
        """
        # Extract required fields
        episode_id = episode["episode_id"]
        content = episode["content"]
        tags = episode["tags"]
        timestamp = episode.get("timestamp", datetime.now().isoformat())

        # Extract optional fields
        emotional_state = episode.get("emotional_state", {})
        metadata = episode.get("metadata", {})

        # Create SharedTask
        task = SharedTask(
            task_id=episode_id,
            task_type="cerebro_episode",
            description=content,
            assigned_node="NEXUS_CREW",
            status=TaskStatus.COMPLETED,  # Episodes are already "completed" events
            priority=TaskPriority.MEDIUM,
            created_at=timestamp,
            updated_at=timestamp,
            result=None,
            metadata={
                "cerebro_episode_id": episode_id,
                "cerebro_tags": tags,
                "emotional_state": emotional_state,
                **metadata  # Merge original metadata
            }
        )

        return task

    def task_to_episode_request(self, task: SharedTask) -> Dict:
        """
        Convert NEXUS_CREW SharedTask to CEREBRO episode request.

        Args:
            task: SharedTask object

        Returns:
            Dictionary for POST /memory/action
        """
        # Format content with agent prefix
        content = f"[{task.assigned_node}] {task.description}"

        # Build tags
        tags = [
            "agent_task",
            task.assigned_node.lower(),  # Keep underscores
            task.task_type
        ]

        # Build metadata
        metadata = {
            "crew_task_id": task.task_id,
            "agent": task.assigned_node,
            "task_status": task.status.value,
            "task_type": task.task_type,
            "task_priority": task.priority.value,
            "created_at": task.created_at,
            "updated_at": task.updated_at
        }

        # Add result if present
        if task.result:
            metadata["task_result"] = task.result

        # Merge original task metadata
        metadata.update(task.metadata)

        # Create episode request
        episode_request = {
            "content": content,
            "tags": tags,
            "current_emotion": "neutral",  # Default, could be enhanced
            "metadata": metadata
        }

        return episode_request

    def sync_cerebro_to_crew(self) -> Dict[str, Any]:
        """
        Sync CEREBRO episodes → NEXUS_CREW tasks.

        Fetches recent episodes with configured tag filter and creates
        corresponding tasks in shared memory.

        Returns:
            Dict with keys: synced_count, episodes, error (if any)
        """
        try:
            # Fetch recent episodes filtered by tag
            episodes = self.cerebro_client.get_recent_episodes(
                limit=50,
                tag_filter=self.cerebro_tag_filter
            )

            synced_episodes = []

            for episode in episodes:
                episode_id = episode["episode_id"]

                # Verify episode has the required tag (defense-in-depth)
                episode_tags = episode.get("tags", [])
                if self.cerebro_tag_filter not in episode_tags:
                    continue  # Skip episodes without the required tag

                # Skip if already synced
                if episode_id in self.synced_episodes:
                    continue

                # Check if task already exists in shared memory
                existing_task = self.github_memory.get_task(episode_id)
                if existing_task:
                    self.synced_episodes.add(episode_id)
                    continue

                # Convert and create task
                task = self.episode_to_task(episode)
                success = self.github_memory.create_task(task)

                if success:
                    synced_episodes.append(episode_id)
                    self.synced_episodes.add(episode_id)

            return {
                "synced_count": len(synced_episodes),
                "episodes": synced_episodes
            }

        except Exception as e:
            logger.error(f"Error syncing CEREBRO → CREW: {e}")
            return {
                "synced_count": 0,
                "episodes": [],
                "error": str(e)
            }

    def sync_crew_to_cerebro(self) -> Dict[str, Any]:
        """
        Sync NEXUS_CREW tasks → CEREBRO episodes.

        Fetches all tasks from shared memory and creates corresponding
        episodes in CEREBRO for tasks not yet synced.

        Returns:
            Dict with keys: synced_count, tasks, error (if any)
        """
        try:
            # Get all tasks from shared memory
            all_tasks = self.github_memory.get_all_tasks()

            synced_tasks = []

            for task in all_tasks:
                task_id = task.task_id

                # Skip if already synced
                if task_id in self.synced_tasks:
                    continue

                # Check if task already has cerebro_episode_id in metadata
                if "cerebro_episode_id" in task.metadata:
                    self.synced_tasks.add(task_id)
                    continue

                # Convert and create episode
                episode_request = self.task_to_episode_request(task)
                response = self.cerebro_client.create_episode(**episode_request)

                if response.get("success"):
                    # Update task metadata with new episode_id
                    episode_id = response.get("episode_id")
                    task.metadata["cerebro_episode_id"] = episode_id
                    task.metadata["cerebro_synced_at"] = datetime.now().isoformat()
                    self.github_memory.create_task(task)  # Update task

                    synced_tasks.append(task_id)
                    self.synced_tasks.add(task_id)

            return {
                "synced_count": len(synced_tasks),
                "tasks": synced_tasks
            }

        except Exception as e:
            logger.error(f"Error syncing CREW → CEREBRO: {e}")
            return {
                "synced_count": 0,
                "tasks": [],
                "error": str(e)
            }

    def bidirectional_sync(self) -> Dict[str, Any]:
        """
        Run bidirectional sync (CEREBRO ↔ CREW).

        Performs both CEREBRO → CREW and CREW → CEREBRO sync.

        Returns:
            Dict with keys: cerebro_to_crew, crew_to_cerebro, total_synced
        """
        # Sync CEREBRO → CREW
        cerebro_to_crew_result = self.sync_cerebro_to_crew()

        # Sync CREW → CEREBRO
        crew_to_cerebro_result = self.sync_crew_to_cerebro()

        # Update timestamp
        self.last_sync_timestamp = datetime.now()

        # Return combined result
        total_synced = (
            cerebro_to_crew_result["synced_count"] +
            crew_to_cerebro_result["synced_count"]
        )

        return {
            "cerebro_to_crew": cerebro_to_crew_result,
            "crew_to_cerebro": crew_to_cerebro_result,
            "total_synced": total_synced,
            "timestamp": self.last_sync_timestamp.isoformat()
        }

    def get_sync_stats(self) -> Dict[str, Any]:
        """
        Get sync statistics.

        Returns:
            Dict with sync statistics
        """
        return {
            "synced_episodes_count": len(self.synced_episodes),
            "synced_tasks_count": len(self.synced_tasks),
            "last_sync_timestamp": (
                self.last_sync_timestamp.isoformat()
                if self.last_sync_timestamp
                else None
            ),
            "cerebro_tag_filter": self.cerebro_tag_filter,
            "shared_memory_path": self.shared_memory_path
        }

    def reset_sync_state(self):
        """
        Reset sync state (clear tracked episodes/tasks).

        Useful for testing or forcing a full re-sync.
        """
        self.synced_episodes.clear()
        self.synced_tasks.clear()
        self.last_sync_timestamp = None
