"""
NEXUS_CREW Integration - Shared Episodic Memory System

Provides bidirectional sync between CEREBRO_NEXUS_V3.0.0 and NEXUS_CREW agents.

Session 14: CerebroClient + CerebroMemoryBridge
Session 15: CerebroAgentCoordinator (Multi-Agent Integration)
"""

from .cerebro_client import CerebroClient
from .cerebro_bridge import CerebroMemoryBridge
from .cerebro_agent_coordinator import (
    CerebroAgentCoordinator,
    AgentEpisode,
    AgentContext
)
from .shared_memory import (
    SharedTask,
    TaskStatus,
    TaskPriority,
    GitHubMemorySync
)

__all__ = [
    # Session 14
    "CerebroClient",
    "CerebroMemoryBridge",
    # Session 15
    "CerebroAgentCoordinator",
    "AgentEpisode",
    "AgentContext",
    # Shared Memory
    "SharedTask",
    "TaskStatus",
    "TaskPriority",
    "GitHubMemorySync",
]
