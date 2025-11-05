"""
Tests for CerebroAgentCoordinator - Multi-Agent Integration with CEREBRO

Session 15: NEXUS_CREW Integration - Part 2A
TDD: Tests written FIRST (RED phase)
"""

import pytest
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# Import will succeed after implementation (GREEN phase)
from features.nexus_crew_integration.cerebro_agent_coordinator import (
    CerebroAgentCoordinator,
    AgentEpisode,
    AgentContext
)
from features.nexus_crew_integration.shared_memory import (
    SharedTask,
    TaskStatus,
    TaskPriority
)


@pytest.fixture
def temp_shared_memory():
    """Create temporary shared memory directory."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def mock_cerebro_client():
    """Create mock CerebroClient."""
    mock_client = Mock()
    mock_client.health_check.return_value = True
    mock_client.create_episode.return_value = {
        "success": True,
        "episode_id": "ep_test_123",
        "timestamp": "2025-11-05T15:00:00"
    }
    mock_client.get_recent_episodes.return_value = [
        {
            "episode_id": "ep1",
            "content": "Test episode 1",
            "tags": ["test", "shared_with_crew"],
            "timestamp": "2025-11-05T14:00:00"
        }
    ]
    return mock_client


class TestCerebroAgentCoordinatorInit:
    """Test CerebroAgentCoordinator initialization."""

    def test_coordinator_initialization(self, temp_shared_memory):
        """Test that coordinator initializes correctly."""
        coordinator = CerebroAgentCoordinator(
            cerebro_base_url="http://localhost:8003",
            shared_memory_path=temp_shared_memory
        )

        assert coordinator.cerebro_base_url == "http://localhost:8003"
        assert coordinator.shared_memory_path == temp_shared_memory
        assert coordinator.bridge is not None


class TestAgentCreateEpisode:
    """Test agents creating episodes in CEREBRO."""

    @patch('features.nexus_crew_integration.cerebro_agent_coordinator.CerebroClient')
    def test_agent_create_episode_success(self, mock_client_class, temp_shared_memory):
        """Test agent successfully creates episode."""
        mock_client = Mock()
        mock_client.create_episode.return_value = {
            "success": True,
            "episode_id": "ep_agent_123",
            "timestamp": "2025-11-05T15:00:00"
        }
        mock_client_class.return_value = mock_client

        coordinator = CerebroAgentCoordinator(shared_memory_path=temp_shared_memory)

        result = coordinator.agent_create_episode(
            agent_name="Project_Auditor",
            content="Completed project audit - found 5 issues",
            tags=["audit", "project_structure"],
            metadata={"issues_count": 5}
        )

        assert result["success"] is True
        assert result["episode_id"] == "ep_agent_123"
        mock_client.create_episode.assert_called_once()

    @patch('features.nexus_crew_integration.cerebro_agent_coordinator.CerebroClient')
    def test_agent_create_episode_with_agent_tag(self, mock_client_class, temp_shared_memory):
        """Test that agent_name is added to tags automatically."""
        mock_client = Mock()
        mock_client.create_episode.return_value = {
            "success": True,
            "episode_id": "ep_test"
        }
        mock_client_class.return_value = mock_client

        coordinator = CerebroAgentCoordinator(shared_memory_path=temp_shared_memory)

        coordinator.agent_create_episode(
            agent_name="Memory_Curator",
            content="Test content",
            tags=["test"]
        )

        call_args = mock_client.create_episode.call_args
        called_tags = call_args[1]["tags"]

        assert "memory_curator" in called_tags
        assert "agent_task" in called_tags
        assert "shared_with_crew" in called_tags


class TestAgentReadContext:
    """Test agents reading context from CEREBRO."""

    @patch('features.nexus_crew_integration.cerebro_agent_coordinator.CerebroClient')
    def test_agent_read_context_success(self, mock_client_class, temp_shared_memory):
        """Test agent reads recent episodes as context."""
        mock_client = Mock()
        mock_client.get_recent_episodes.return_value = [
            {
                "episode_id": "ep1",
                "content": "Episode 1",
                "tags": ["test"],
                "timestamp": "2025-11-05T14:00:00"
            },
            {
                "episode_id": "ep2",
                "content": "Episode 2",
                "tags": ["test"],
                "timestamp": "2025-11-05T14:05:00"
            }
        ]
        mock_client_class.return_value = mock_client

        coordinator = CerebroAgentCoordinator(shared_memory_path=temp_shared_memory)

        context = coordinator.agent_read_context(
            agent_name="Semantic_Router",
            limit=10
        )

        assert len(context["episodes"]) == 2
        assert context["episodes"][0]["episode_id"] == "ep1"
        assert context["agent_name"] == "Semantic_Router"

    @patch('features.nexus_crew_integration.cerebro_agent_coordinator.CerebroClient')
    def test_agent_read_context_with_tag_filter(self, mock_client_class, temp_shared_memory):
        """Test agent reads context filtered by specific tag."""
        mock_client = Mock()
        mock_client.get_recent_episodes.return_value = [
            {
                "episode_id": "ep_filtered",
                "content": "Filtered episode",
                "tags": ["audit", "shared_with_crew"],
                "timestamp": "2025-11-05T14:00:00"
            }
        ]
        mock_client_class.return_value = mock_client

        coordinator = CerebroAgentCoordinator(shared_memory_path=temp_shared_memory)

        context = coordinator.agent_read_context(
            agent_name="Project_Auditor",
            limit=5,
            tag_filter="audit"
        )

        assert len(context["episodes"]) == 1
        mock_client.get_recent_episodes.assert_called_with(limit=5, tag_filter="audit")


class TestAgentSyncResults:
    """Test agents syncing results to CEREBRO + SharedMemory."""

    @patch('features.nexus_crew_integration.cerebro_agent_coordinator.CerebroClient')
    def test_agent_sync_results_success(self, mock_client_class, temp_shared_memory):
        """Test agent syncs task results to both systems."""
        mock_client = Mock()
        mock_client.create_episode.return_value = {
            "success": True,
            "episode_id": "ep_result_123"
        }
        mock_client_class.return_value = mock_client

        coordinator = CerebroAgentCoordinator(shared_memory_path=temp_shared_memory)

        agent_results = {
            "agent_name": "Document_Reconciler",
            "task_type": "reconciliation",
            "status": "completed",
            "result": {
                "conflicts_resolved": 3,
                "files_synced": 10
            }
        }

        result = coordinator.agent_sync_results(agent_results)

        assert result["cerebro_synced"] is True
        assert result["shared_memory_synced"] is True
        assert result["episode_id"] == "ep_result_123"

    @patch('features.nexus_crew_integration.cerebro_agent_coordinator.CerebroClient')
    def test_agent_sync_results_creates_shared_task(self, mock_client_class, temp_shared_memory):
        """Test that sync creates task in shared memory."""
        mock_client = Mock()
        mock_client.create_episode.return_value = {
            "success": True,
            "episode_id": "ep_task_sync"
        }
        mock_client_class.return_value = mock_client

        coordinator = CerebroAgentCoordinator(shared_memory_path=temp_shared_memory)

        agent_results = {
            "agent_name": "Memory_Curator",
            "task_type": "graph_building",
            "status": "completed",
            "result": {"relationships_created": 1000}
        }

        coordinator.agent_sync_results(agent_results)

        # Verify task created in shared memory
        from features.nexus_crew_integration.shared_memory import GitHubMemorySync
        github_memory = GitHubMemorySync(temp_shared_memory)

        # Task should exist with episode_id as task_id
        task = github_memory.get_task("ep_task_sync")
        assert task is not None
        assert task.assigned_node == "Memory_Curator"
        assert task.status == TaskStatus.COMPLETED


class TestMultiAgentCoordination:
    """Test coordination between multiple agents."""

    @patch('features.nexus_crew_integration.cerebro_agent_coordinator.CerebroClient')
    def test_multiple_agents_create_episodes(self, mock_client_class, temp_shared_memory):
        """Test multiple agents can create episodes simultaneously."""
        mock_client = Mock()
        mock_client.create_episode.side_effect = [
            {"success": True, "episode_id": "ep_agent1"},
            {"success": True, "episode_id": "ep_agent2"},
            {"success": True, "episode_id": "ep_agent3"}
        ]
        mock_client_class.return_value = mock_client

        coordinator = CerebroAgentCoordinator(shared_memory_path=temp_shared_memory)

        agents = ["Project_Auditor", "Memory_Curator", "Semantic_Router"]
        results = []

        for agent in agents:
            result = coordinator.agent_create_episode(
                agent_name=agent,
                content=f"{agent} completed task",
                tags=["test"]
            )
            results.append(result)

        assert len(results) == 3
        assert all(r["success"] for r in results)
        assert results[0]["episode_id"] == "ep_agent1"
        assert results[1]["episode_id"] == "ep_agent2"
        assert results[2]["episode_id"] == "ep_agent3"


class TestAgentEpisodeModel:
    """Test AgentEpisode data model."""

    def test_agent_episode_creation(self):
        """Test creating AgentEpisode object."""
        episode = AgentEpisode(
            agent_name="Test_Agent",
            content="Test content",
            tags=["test"],
            metadata={"key": "value"}
        )

        assert episode.agent_name == "Test_Agent"
        assert episode.content == "Test content"
        assert episode.tags == ["test"]
        assert episode.metadata == {"key": "value"}

    def test_agent_episode_to_dict(self):
        """Test converting AgentEpisode to dictionary."""
        episode = AgentEpisode(
            agent_name="Project_Auditor",
            content="Audit complete",
            tags=["audit"],
            metadata={"issues": 5}
        )

        episode_dict = episode.to_dict()

        assert isinstance(episode_dict, dict)
        assert episode_dict["metadata"]["agent"] == "Project_Auditor"
        assert episode_dict["content"] == "[Project_Auditor] Audit complete"
        assert "agent_task" in episode_dict["tags"]
        assert "shared_with_crew" in episode_dict["tags"]
        assert "project_auditor" in episode_dict["tags"]


class TestAgentContextModel:
    """Test AgentContext data model."""

    def test_agent_context_creation(self):
        """Test creating AgentContext object."""
        context = AgentContext(
            agent_name="Semantic_Router",
            episodes=[
                {"episode_id": "ep1", "content": "Episode 1"},
                {"episode_id": "ep2", "content": "Episode 2"}
            ],
            total_episodes=2
        )

        assert context.agent_name == "Semantic_Router"
        assert len(context.episodes) == 2
        assert context.total_episodes == 2


class TestErrorHandling:
    """Test error handling in coordinator."""

    @patch('features.nexus_crew_integration.cerebro_agent_coordinator.CerebroClient')
    def test_cerebro_connection_error(self, mock_client_class, temp_shared_memory):
        """Test handling of CEREBRO connection errors."""
        mock_client = Mock()
        mock_client.create_episode.side_effect = Exception("Connection refused")
        mock_client_class.return_value = mock_client

        coordinator = CerebroAgentCoordinator(shared_memory_path=temp_shared_memory)

        result = coordinator.agent_create_episode(
            agent_name="Test_Agent",
            content="Test",
            tags=["test"]
        )

        assert result["success"] is False
        assert "error" in result
        assert "Connection refused" in result["error"]

    @patch('features.nexus_crew_integration.cerebro_agent_coordinator.CerebroClient')
    def test_invalid_agent_name(self, mock_client_class, temp_shared_memory):
        """Test handling of invalid agent name."""
        mock_client_class.return_value = Mock()

        coordinator = CerebroAgentCoordinator(shared_memory_path=temp_shared_memory)

        with pytest.raises(ValueError):
            coordinator.agent_create_episode(
                agent_name="",  # Empty agent name
                content="Test",
                tags=["test"]
            )


class TestAgentCoordinatorIntegration:
    """Test integration between coordinator and CerebroMemoryBridge."""

    @patch('features.nexus_crew_integration.cerebro_agent_coordinator.CerebroClient')
    def test_coordinator_uses_bridge_for_sync(self, mock_client_class, temp_shared_memory):
        """Test that coordinator uses CerebroMemoryBridge internally."""
        mock_client = Mock()
        mock_client.create_episode.return_value = {"success": True, "episode_id": "ep_test"}
        mock_client_class.return_value = mock_client

        coordinator = CerebroAgentCoordinator(shared_memory_path=temp_shared_memory)

        # This should use bridge internally
        coordinator.agent_create_episode(
            agent_name="Test_Agent",
            content="Test",
            tags=["test"]
        )

        # Verify bridge was used (episode created in CEREBRO)
        mock_client.create_episode.assert_called_once()

    @patch('features.nexus_crew_integration.cerebro_agent_coordinator.CerebroClient')
    def test_bidirectional_flow_agent_to_cerebro_to_agent(self, mock_client_class, temp_shared_memory):
        """Test complete bidirectional flow: Agent → CEREBRO → Agent."""
        mock_client = Mock()

        # Agent 1 creates episode
        mock_client.create_episode.return_value = {
            "success": True,
            "episode_id": "ep_agent1_result"
        }

        # Agent 2 reads that episode
        mock_client.get_recent_episodes.return_value = [
            {
                "episode_id": "ep_agent1_result",
                "content": "Agent 1 completed task",
                "tags": ["agent_task", "shared_with_crew"],
                "timestamp": "2025-11-05T15:00:00"
            }
        ]

        mock_client_class.return_value = mock_client

        coordinator = CerebroAgentCoordinator(shared_memory_path=temp_shared_memory)

        # Agent 1 creates episode
        create_result = coordinator.agent_create_episode(
            agent_name="Agent_1",
            content="Agent 1 completed task",
            tags=["test"]
        )

        # Agent 2 reads context (including Agent 1's episode)
        context = coordinator.agent_read_context(
            agent_name="Agent_2",
            limit=10
        )

        assert create_result["success"] is True
        assert len(context["episodes"]) == 1
        assert context["episodes"][0]["episode_id"] == "ep_agent1_result"
