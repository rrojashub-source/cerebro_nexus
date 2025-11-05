"""
CerebroAgentCoordinator - Multi-Agent Integration with CEREBRO

Session 15: NEXUS_CREW Integration - Part 2A
Coordinates NEXUS_CREW agents with CEREBRO episodic memory.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, field, asdict
import logging

from .cerebro_client import CerebroClient
from .cerebro_bridge import CerebroMemoryBridge
from .shared_memory import SharedTask, TaskStatus, TaskPriority, GitHubMemorySync


# Setup logging
logger = logging.getLogger(__name__)


@dataclass
class AgentEpisode:
    """
    Represents an episode created by an agent.

    Automatically adds agent metadata and standardized tags.
    """
    agent_name: str
    content: str
    tags: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary for CEREBRO API.

        Adds standard agent tags automatically.
        """
        # Normalize agent name for tag
        agent_tag = self.agent_name.lower().replace(" ", "_")

        # Standard tags for all agent episodes
        standard_tags = ["agent_task", "shared_with_crew", agent_tag]

        # Merge with provided tags (deduplicate)
        all_tags = list(set(standard_tags + self.tags))

        return {
            "content": f"[{self.agent_name}] {self.content}",
            "tags": all_tags,
            "current_emotion": "neutral",
            "metadata": {
                "agent": self.agent_name,
                "timestamp": self.timestamp,
                **self.metadata
            }
        }


@dataclass
class AgentContext:
    """
    Represents context retrieved for an agent.

    Contains recent episodes relevant to agent's work.
    """
    agent_name: str
    episodes: List[Dict[str, Any]]
    total_episodes: int
    retrieved_at: str = field(default_factory=lambda: datetime.now().isoformat())


class CerebroAgentCoordinator:
    """
    Coordinates NEXUS_CREW agents with CEREBRO episodic memory.

    Provides:
    - Agent → CEREBRO episode creation
    - CEREBRO → Agent context retrieval
    - Bidirectional sync (agent results → CEREBRO + SharedMemory)
    - Multi-agent coordination support
    """

    def __init__(
        self,
        cerebro_base_url: str = "http://localhost:8003",
        shared_memory_path: str = ".shared_memory"
    ):
        """
        Initialize CerebroAgentCoordinator.

        Args:
            cerebro_base_url: Base URL of CEREBRO API (default: http://localhost:8003)
            shared_memory_path: Path to shared memory storage (default: .shared_memory)
        """
        self.cerebro_base_url = cerebro_base_url
        self.shared_memory_path = shared_memory_path

        # Initialize clients
        self.cerebro_client = CerebroClient(cerebro_base_url)
        self.bridge = CerebroMemoryBridge(
            cerebro_base_url=cerebro_base_url,
            shared_memory_path=shared_memory_path
        )
        self.github_memory = GitHubMemorySync(shared_memory_path)

        logger.info(f"CerebroAgentCoordinator initialized (CEREBRO: {cerebro_base_url})")

    def agent_create_episode(
        self,
        agent_name: str,
        content: str,
        tags: List[str],
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Agent creates episode in CEREBRO.

        Args:
            agent_name: Name of agent creating episode (e.g., "Project_Auditor")
            content: Episode content (agent's action description)
            tags: Custom tags for episode
            metadata: Optional metadata dictionary

        Returns:
            Dict with keys: success, episode_id (if success), error (if failed)

        Raises:
            ValueError: If agent_name is empty
        """
        # Validation
        if not agent_name or not agent_name.strip():
            raise ValueError("agent_name cannot be empty")

        try:
            # Create AgentEpisode
            episode = AgentEpisode(
                agent_name=agent_name,
                content=content,
                tags=tags,
                metadata=metadata or {}
            )

            # Convert to CEREBRO format
            episode_dict = episode.to_dict()

            # Create in CEREBRO
            response = self.cerebro_client.create_episode(**episode_dict)

            if response.get("success"):
                logger.info(f"Agent '{agent_name}' created episode: {response.get('episode_id')}")
                return {
                    "success": True,
                    "episode_id": response.get("episode_id"),
                    "timestamp": response.get("timestamp")
                }
            else:
                logger.warning(f"Agent '{agent_name}' failed to create episode")
                return {
                    "success": False,
                    "error": response.get("message", "Unknown error")
                }

        except Exception as e:
            logger.error(f"Error in agent_create_episode for '{agent_name}': {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def agent_read_context(
        self,
        agent_name: str,
        limit: int = 10,
        tag_filter: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Agent reads recent episodes as context.

        Args:
            agent_name: Name of agent reading context
            limit: Max number of episodes to retrieve
            tag_filter: Optional tag to filter episodes (e.g., "audit")

        Returns:
            Dict with keys: agent_name, episodes, total_episodes, retrieved_at
        """
        try:
            # Get recent episodes from CEREBRO
            episodes = self.cerebro_client.get_recent_episodes(
                limit=limit,
                tag_filter=tag_filter
            )

            logger.info(f"Agent '{agent_name}' retrieved {len(episodes)} episodes")

            # Create context
            context = AgentContext(
                agent_name=agent_name,
                episodes=episodes,
                total_episodes=len(episodes)
            )

            return {
                "agent_name": context.agent_name,
                "episodes": context.episodes,
                "total_episodes": context.total_episodes,
                "retrieved_at": context.retrieved_at
            }

        except Exception as e:
            logger.error(f"Error in agent_read_context for '{agent_name}': {e}")
            return {
                "agent_name": agent_name,
                "episodes": [],
                "total_episodes": 0,
                "error": str(e)
            }

    def agent_sync_results(
        self,
        agent_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Agent syncs task results to CEREBRO + SharedMemory.

        Creates:
        1. Episode in CEREBRO with agent results
        2. Task in SharedMemory for other agents to see

        Args:
            agent_results: Dict with keys:
                - agent_name: str
                - task_type: str
                - status: str (e.g., "completed", "failed")
                - result: Dict (task-specific results)

        Returns:
            Dict with keys:
                - cerebro_synced: bool
                - shared_memory_synced: bool
                - episode_id: str (if cerebro_synced)
                - task_id: str (if shared_memory_synced)
                - error: str (if failed)
        """
        try:
            agent_name = agent_results["agent_name"]
            task_type = agent_results["task_type"]
            status = agent_results["status"]
            result = agent_results.get("result", {})

            # 1. Create episode in CEREBRO
            content = f"Task '{task_type}' {status}"
            if result:
                # Add result summary to content
                result_summary = ", ".join([f"{k}: {v}" for k, v in list(result.items())[:3]])
                content += f" - {result_summary}"

            episode_response = self.agent_create_episode(
                agent_name=agent_name,
                content=content,
                tags=[task_type, status, "agent_result"],
                metadata={
                    "task_type": task_type,
                    "status": status,
                    "result": result
                }
            )

            cerebro_synced = episode_response.get("success", False)
            episode_id = episode_response.get("episode_id")

            # 2. Create task in SharedMemory
            shared_memory_synced = False
            task_id = None

            if cerebro_synced and episode_id:
                # Map status string to TaskStatus enum
                status_map = {
                    "completed": TaskStatus.COMPLETED,
                    "failed": TaskStatus.FAILED,
                    "in_progress": TaskStatus.IN_PROGRESS,
                    "pending": TaskStatus.PENDING
                }
                task_status = status_map.get(status.lower(), TaskStatus.COMPLETED)

                # Create SharedTask
                task = SharedTask(
                    task_id=episode_id,  # Use episode_id as task_id
                    task_type=task_type,
                    description=content,
                    assigned_node=agent_name,
                    status=task_status,
                    priority=TaskPriority.MEDIUM,
                    result=result,
                    metadata={
                        "cerebro_episode_id": episode_id,
                        "agent": agent_name,
                        "synced_at": datetime.now().isoformat()
                    }
                )

                # Create in SharedMemory
                shared_memory_synced = self.github_memory.create_task(task)
                task_id = episode_id if shared_memory_synced else None

            logger.info(f"Agent '{agent_name}' synced results (CEREBRO: {cerebro_synced}, SharedMemory: {shared_memory_synced})")

            return {
                "cerebro_synced": cerebro_synced,
                "shared_memory_synced": shared_memory_synced,
                "episode_id": episode_id,
                "task_id": task_id
            }

        except Exception as e:
            logger.error(f"Error in agent_sync_results: {e}")
            return {
                "cerebro_synced": False,
                "shared_memory_synced": False,
                "error": str(e)
            }

    def get_agent_history(
        self,
        agent_name: str,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Get history of episodes created by specific agent.

        Args:
            agent_name: Name of agent
            limit: Max episodes to retrieve

        Returns:
            List of episodes created by agent
        """
        try:
            # Normalize agent name to tag format
            agent_tag = agent_name.lower().replace(" ", "_")

            # Get episodes with agent's tag
            episodes = self.cerebro_client.get_recent_episodes(
                limit=limit,
                tag_filter=agent_tag
            )

            logger.info(f"Retrieved {len(episodes)} episodes for agent '{agent_name}'")
            return episodes

        except Exception as e:
            logger.error(f"Error in get_agent_history for '{agent_name}': {e}")
            return []

    def get_coordinator_stats(self) -> Dict[str, Any]:
        """
        Get coordination statistics.

        Returns:
            Dict with coordination stats
        """
        try:
            # Get health from CEREBRO
            cerebro_healthy = self.cerebro_client.health_check()

            # Get tasks from SharedMemory
            all_tasks = self.github_memory.get_all_tasks()
            agent_tasks = [t for t in all_tasks if "agent" in t.metadata]

            return {
                "cerebro_healthy": cerebro_healthy,
                "cerebro_url": self.cerebro_base_url,
                "shared_memory_path": self.shared_memory_path,
                "total_agent_tasks": len(agent_tasks),
                "tasks_by_status": {
                    "completed": len([t for t in agent_tasks if t.status == TaskStatus.COMPLETED]),
                    "pending": len([t for t in agent_tasks if t.status == TaskStatus.PENDING]),
                    "in_progress": len([t for t in agent_tasks if t.status == TaskStatus.IN_PROGRESS]),
                    "failed": len([t for t in agent_tasks if t.status == TaskStatus.FAILED])
                }
            }

        except Exception as e:
            logger.error(f"Error in get_coordinator_stats: {e}")
            return {
                "cerebro_healthy": False,
                "error": str(e)
            }
