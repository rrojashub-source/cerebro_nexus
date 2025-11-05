"""
Tests for CerebroMemoryBridge - Bidirectional sync engine

Session 14: NEXUS_CREW Integration - Part 1B
TDD: Tests written FIRST (RED phase)
"""

import pytest
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# Import will fail initially - this is expected in RED phase
from features.nexus_crew_integration.cerebro_bridge import CerebroMemoryBridge
from features.nexus_crew_integration.shared_memory import (
    SharedTask,
    TaskStatus,
    TaskPriority,
    GitHubMemorySync
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
    return mock_client


class TestEpisodeToTaskConversion:
    """Test conversion of CEREBRO episodes to NEXUS_CREW tasks."""

    def test_episode_to_task_basic(self, temp_shared_memory):
        """Test basic episode to task conversion."""
        bridge = CerebroMemoryBridge(
            cerebro_base_url="http://localhost:8003",
            shared_memory_path=temp_shared_memory
        )

        episode = {
            "episode_id": "924abf52",
            "content": "Completed Session 14 design phase",
            "tags": ["session_14", "architecture", "shared_with_crew"],
            "timestamp": "2025-11-05T10:30:00",
            "emotional_state": {"joy": 0.8, "trust": 0.7}
        }

        task = bridge.episode_to_task(episode)

        # Verify conversion
        assert task.task_id == "924abf52"
        assert task.task_type == "cerebro_episode"
        assert "Session 14" in task.description
        assert task.assigned_node == "NEXUS_CREW"
        assert task.status == TaskStatus.COMPLETED
        assert task.metadata["cerebro_episode_id"] == "924abf52"
        assert task.metadata["cerebro_tags"] == ["session_14", "architecture", "shared_with_crew"]
        assert "emotional_state" in task.metadata

    def test_episode_to_task_with_metadata(self, temp_shared_memory):
        """Test episode with additional metadata."""
        bridge = CerebroMemoryBridge(shared_memory_path=temp_shared_memory)

        episode = {
            "episode_id": "ep123",
            "content": "Test episode",
            "tags": ["test"],
            "timestamp": "2025-11-05T10:00:00",
            "metadata": {"custom_field": "value"}
        }

        task = bridge.episode_to_task(episode)

        # Verify metadata preservation
        assert task.metadata["custom_field"] == "value"


class TestTaskToEpisodeConversion:
    """Test conversion of NEXUS_CREW tasks to CEREBRO episodes."""

    def test_task_to_episode_basic(self, temp_shared_memory):
        """Test basic task to episode conversion."""
        bridge = CerebroMemoryBridge(shared_memory_path=temp_shared_memory)

        task = SharedTask(
            task_id="task_123",
            task_type="project_audit",
            description="Audited CEREBRO_NEXUS_V3.0.0 structure",
            assigned_node="Project_Auditor",
            status=TaskStatus.COMPLETED,
            result={"found_issues": 2, "recommendations": ["Fix A", "Fix B"]}
        )

        episode_request = bridge.task_to_episode_request(task)

        # Verify conversion
        assert "[Project_Auditor]" in episode_request["content"]
        assert "Audited CEREBRO" in episode_request["content"]
        assert "agent_task" in episode_request["tags"]
        assert "project_auditor" in episode_request["tags"]
        assert "project_audit" in episode_request["tags"]
        assert episode_request["metadata"]["crew_task_id"] == "task_123"
        assert episode_request["metadata"]["agent"] == "Project_Auditor"
        assert episode_request["metadata"]["task_status"] == "completed"

    def test_task_to_episode_with_failed_status(self, temp_shared_memory):
        """Test task with FAILED status."""
        bridge = CerebroMemoryBridge(shared_memory_path=temp_shared_memory)

        task = SharedTask(
            task_id="task_456",
            task_type="test",
            description="Failed task",
            assigned_node="Test_Agent",
            status=TaskStatus.FAILED,
            result={"error": "Connection timeout"}
        )

        episode_request = bridge.task_to_episode_request(task)

        # Verify failed status is preserved
        assert episode_request["metadata"]["task_status"] == "failed"
        assert episode_request["metadata"]["task_result"]["error"] == "Connection timeout"


class TestSyncCerebroToCrew:
    """Test syncing CEREBRO episodes to NEXUS_CREW tasks."""

    @patch('features.nexus_crew_integration.cerebro_bridge.CerebroClient')
    def test_sync_cerebro_to_crew_basic(self, mock_client_class, temp_shared_memory):
        """Test basic CEREBRO → CREW sync."""
        # Mock CerebroClient
        mock_client = Mock()
        mock_client.get_recent_episodes.return_value = [
            {
                "episode_id": "ep1",
                "content": "Episode 1",
                "tags": ["shared_with_crew"],
                "timestamp": "2025-11-05T10:00:00"
            },
            {
                "episode_id": "ep2",
                "content": "Episode 2",
                "tags": ["shared_with_crew"],
                "timestamp": "2025-11-05T10:05:00"
            }
        ]
        mock_client_class.return_value = mock_client

        bridge = CerebroMemoryBridge(shared_memory_path=temp_shared_memory)
        result = bridge.sync_cerebro_to_crew()

        # Verify sync result
        assert result["synced_count"] == 2
        assert len(result["episodes"]) == 2
        assert "ep1" in result["episodes"]
        assert "ep2" in result["episodes"]

        # Verify tasks were created in shared memory
        github_memory = GitHubMemorySync(temp_shared_memory)
        task1 = github_memory.get_task("ep1")
        task2 = github_memory.get_task("ep2")

        assert task1 is not None
        assert task2 is not None
        assert task1.description == "Episode 1"
        assert task2.description == "Episode 2"

    @patch('features.nexus_crew_integration.cerebro_bridge.CerebroClient')
    def test_sync_cerebro_to_crew_no_shared_tag(self, mock_client_class, temp_shared_memory):
        """Test that episodes without 'shared_with_crew' tag are NOT synced."""
        mock_client = Mock()
        mock_client.get_recent_episodes.return_value = [
            {
                "episode_id": "ep_private",
                "content": "Private episode",
                "tags": ["internal", "private"],  # No "shared_with_crew"
                "timestamp": "2025-11-05T10:00:00"
            }
        ]
        mock_client_class.return_value = mock_client

        bridge = CerebroMemoryBridge(shared_memory_path=temp_shared_memory)
        result = bridge.sync_cerebro_to_crew()

        # Should sync 0 episodes (filtered by tag)
        assert result["synced_count"] == 0


class TestSyncCrewToCerebro:
    """Test syncing NEXUS_CREW tasks to CEREBRO episodes."""

    @patch('features.nexus_crew_integration.cerebro_bridge.CerebroClient')
    def test_sync_crew_to_cerebro_basic(self, mock_client_class, temp_shared_memory):
        """Test basic CREW → CEREBRO sync."""
        # Create tasks in shared memory
        github_memory = GitHubMemorySync(temp_shared_memory)
        task1 = SharedTask(
            task_id="task_new_1",
            task_type="audit",
            description="Audit complete",
            assigned_node="Project_Auditor",
            status=TaskStatus.COMPLETED
        )
        github_memory.create_task(task1)

        # Mock CerebroClient
        mock_client = Mock()
        mock_client.create_episode.return_value = {
            "success": True,
            "episode_id": "new_ep_1",
            "timestamp": "2025-11-05T10:30:00"
        }
        mock_client_class.return_value = mock_client

        bridge = CerebroMemoryBridge(shared_memory_path=temp_shared_memory)
        result = bridge.sync_crew_to_cerebro()

        # Verify sync result
        assert result["synced_count"] == 1
        assert "task_new_1" in result["tasks"]

        # Verify episode was created
        mock_client.create_episode.assert_called_once()

        # Verify task metadata was updated with episode_id
        updated_task = github_memory.get_task("task_new_1")
        assert updated_task.metadata["cerebro_episode_id"] == "new_ep_1"


class TestBidirectionalSync:
    """Test bidirectional syncing."""

    @patch('features.nexus_crew_integration.cerebro_bridge.CerebroClient')
    def test_bidirectional_sync(self, mock_client_class, temp_shared_memory):
        """Test both directions sync in one call."""
        # Setup: episode in CEREBRO, task in CREW
        mock_client = Mock()
        mock_client.get_recent_episodes.return_value = [
            {"episode_id": "ep1", "content": "Cerebro episode", "tags": ["shared_with_crew"], "timestamp": "2025-11-05T10:00:00"}
        ]
        mock_client.create_episode.return_value = {
            "success": True, "episode_id": "new_ep", "timestamp": "2025-11-05T10:30:00"
        }
        mock_client_class.return_value = mock_client

        # Create task in CREW
        github_memory = GitHubMemorySync(temp_shared_memory)
        task = SharedTask(task_id="task1", task_type="test", description="Test", assigned_node="Agent", status=TaskStatus.COMPLETED)
        github_memory.create_task(task)

        bridge = CerebroMemoryBridge(shared_memory_path=temp_shared_memory)
        result = bridge.bidirectional_sync()

        # Verify both directions synced
        assert result["cerebro_to_crew"]["synced_count"] == 1
        assert result["crew_to_cerebro"]["synced_count"] == 1


class TestDuplicatePrevention:
    """Test duplicate detection and prevention."""

    @patch('features.nexus_crew_integration.cerebro_bridge.CerebroClient')
    def test_duplicate_episode_not_synced_twice(self, mock_client_class, temp_shared_memory):
        """Test that already synced episodes are not synced again."""
        mock_client = Mock()
        mock_client.get_recent_episodes.return_value = [
            {"episode_id": "ep_dup", "content": "Duplicate test", "tags": ["shared_with_crew"], "timestamp": "2025-11-05T10:00:00"}
        ]
        mock_client_class.return_value = mock_client

        bridge = CerebroMemoryBridge(shared_memory_path=temp_shared_memory)

        # First sync
        result1 = bridge.sync_cerebro_to_crew()
        assert result1["synced_count"] == 1

        # Second sync (same episode)
        result2 = bridge.sync_cerebro_to_crew()
        assert result2["synced_count"] == 0  # Already synced, should skip


class TestTagFiltering:
    """Test tag-based filtering."""

    @patch('features.nexus_crew_integration.cerebro_bridge.CerebroClient')
    def test_custom_tag_filter(self, mock_client_class, temp_shared_memory):
        """Test using custom tag filter."""
        mock_client = Mock()
        mock_client.get_recent_episodes.return_value = [
            {"episode_id": "ep1", "content": "Test", "tags": ["custom_tag"], "timestamp": "2025-11-05T10:00:00"}
        ]
        mock_client_class.return_value = mock_client

        bridge = CerebroMemoryBridge(
            shared_memory_path=temp_shared_memory,
            cerebro_tag_filter="custom_tag"
        )

        result = bridge.sync_cerebro_to_crew()
        assert result["synced_count"] == 1


class TestMetadataPreservation:
    """Test metadata is preserved during conversions."""

    def test_metadata_roundtrip(self, temp_shared_memory):
        """Test metadata survives Episode → Task → Episode conversion."""
        bridge = CerebroMemoryBridge(shared_memory_path=temp_shared_memory)

        # Original episode with rich metadata
        original_episode = {
            "episode_id": "ep_meta",
            "content": "Test content",
            "tags": ["test", "metadata"],
            "timestamp": "2025-11-05T10:00:00",
            "emotional_state": {"joy": 0.9, "trust": 0.8},
            "metadata": {"custom_field": "important_value", "session": 14}
        }

        # Convert to task
        task = bridge.episode_to_task(original_episode)

        # Verify metadata preserved
        assert task.metadata["cerebro_episode_id"] == "ep_meta"
        assert task.metadata["custom_field"] == "important_value"
        assert task.metadata["session"] == 14
        assert "emotional_state" in task.metadata


class TestErrorHandling:
    """Test error handling in sync operations."""

    @patch('features.nexus_crew_integration.cerebro_bridge.CerebroClient')
    def test_cerebro_connection_error(self, mock_client_class, temp_shared_memory):
        """Test handling of CEREBRO connection errors."""
        mock_client = Mock()
        mock_client.get_recent_episodes.side_effect = Exception("Connection refused")
        mock_client_class.return_value = mock_client

        bridge = CerebroMemoryBridge(shared_memory_path=temp_shared_memory)

        # Should handle error gracefully
        result = bridge.sync_cerebro_to_crew()

        assert result["synced_count"] == 0
        assert "error" in result
        assert "Connection refused" in result["error"]

    def test_invalid_episode_data(self, temp_shared_memory):
        """Test handling of invalid episode data."""
        bridge = CerebroMemoryBridge(shared_memory_path=temp_shared_memory)

        # Invalid episode (missing required fields)
        invalid_episode = {"episode_id": "bad"}

        # Should handle gracefully without crashing
        try:
            task = bridge.episode_to_task(invalid_episode)
            # Should either return None or raise specific exception
        except (KeyError, ValueError) as e:
            # Expected behavior: raise error for invalid data
            assert "content" in str(e) or "tags" in str(e)
