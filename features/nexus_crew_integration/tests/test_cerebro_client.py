"""
Tests for CerebroClient - HTTP client for CEREBRO API

Session 14: NEXUS_CREW Integration
TDD: Tests written FIRST (RED phase)
"""

import pytest
from unittest.mock import Mock, patch
import requests

# Import will fail initially - this is expected in RED phase
from features.nexus_crew_integration.cerebro_client import CerebroClient


class TestCerebroClientInit:
    """Test CerebroClient initialization."""

    def test_client_initialization(self):
        """Test that client initializes with correct base_url."""
        client = CerebroClient(base_url="http://localhost:8003")

        assert client.base_url == "http://localhost:8003"
        assert client.session is not None
        assert client.session.headers["Content-Type"] == "application/json"


class TestCreateEpisode:
    """Test create_episode method."""

    @patch('requests.Session.post')
    def test_create_episode_success(self, mock_post):
        """Test successful episode creation."""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "episode_id": "924abf52",
            "timestamp": "2025-11-05T10:30:00"
        }
        mock_post.return_value = mock_response

        # Create client and episode
        client = CerebroClient()
        result = client.create_episode(
            content="Test episode",
            tags=["test", "shared_with_crew"],
            current_emotion="joy"
        )

        # Verify API call
        mock_post.assert_called_once()
        call_args = mock_post.call_args

        # Verify result
        assert result["success"] is True
        assert result["episode_id"] == "924abf52"

    @patch('requests.Session.post')
    def test_create_episode_with_metadata(self, mock_post):
        """Test episode creation with metadata."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "episode_id": "abc123"
        }
        mock_post.return_value = mock_response

        client = CerebroClient()
        metadata = {"crew_task_id": "task_123", "agent": "Project_Auditor"}
        result = client.create_episode(
            content="Audit complete",
            tags=["audit"],
            metadata=metadata
        )

        # Verify metadata was passed
        call_args = mock_post.call_args
        request_body = call_args[1]["json"]
        assert "metadata" in request_body
        assert request_body["metadata"]["crew_task_id"] == "task_123"


class TestSearchEpisodes:
    """Test search_episodes method."""

    @patch('requests.Session.post')
    def test_search_episodes_success(self, mock_post):
        """Test successful episode search."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "episodes": [
                {
                    "episode_id": "ep1",
                    "content": "First episode",
                    "similarity": 0.95
                },
                {
                    "episode_id": "ep2",
                    "content": "Second episode",
                    "similarity": 0.87
                }
            ]
        }
        mock_post.return_value = mock_response

        client = CerebroClient()
        result = client.search_episodes(query="test", limit=2)

        # Verify result
        assert len(result) == 2
        assert result[0]["episode_id"] == "ep1"
        assert result[1]["similarity"] == 0.87

    @patch('requests.Session.post')
    def test_search_episodes_empty_result(self, mock_post):
        """Test search with no results."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"episodes": []}
        mock_post.return_value = mock_response

        client = CerebroClient()
        result = client.search_episodes(query="nonexistent")

        assert result == []


class TestGetRecentEpisodes:
    """Test get_recent_episodes method."""

    @patch('requests.Session.get')
    def test_get_recent_episodes_success(self, mock_get):
        """Test getting recent episodes."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "episodes": [
                {"episode_id": "ep1", "content": "Recent 1"},
                {"episode_id": "ep2", "content": "Recent 2"}
            ]
        }
        mock_get.return_value = mock_response

        client = CerebroClient()
        result = client.get_recent_episodes(limit=2)

        # Verify API call
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        call_url = call_args[0][0]
        call_params = call_args[1]["params"]

        assert "/memory/episodic/recent" in call_url
        assert call_params["limit"] == 2

        # Verify result
        assert len(result) == 2
        assert result[0]["episode_id"] == "ep1"

    @patch('requests.Session.get')
    def test_get_recent_episodes_with_tag_filter(self, mock_get):
        """Test getting recent episodes filtered by tag."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "episodes": [
                {"episode_id": "ep1", "tags": ["shared_with_crew"]}
            ]
        }
        mock_get.return_value = mock_response

        client = CerebroClient()
        result = client.get_recent_episodes(limit=10, tag_filter="shared_with_crew")

        # Verify tag_filter was passed
        call_args = mock_get.call_args
        call_params = call_args[1]["params"]

        assert call_params["tag_filter"] == "shared_with_crew"
        assert call_params["limit"] == 10

        assert len(result) == 1


class TestHealthCheck:
    """Test health_check method."""

    @patch('requests.Session.get')
    def test_health_check_healthy(self, mock_get):
        """Test health check when CEREBRO is healthy."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "healthy",
            "version": "3.0.0"
        }
        mock_get.return_value = mock_response

        client = CerebroClient()
        result = client.health_check()

        assert result is True

    @patch('requests.Session.get')
    def test_health_check_unhealthy(self, mock_get):
        """Test health check when CEREBRO is down."""
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection refused")

        client = CerebroClient()
        result = client.health_check()

        assert result is False


class TestConnectionErrorHandling:
    """Test error handling for connection issues."""

    @patch('requests.Session.post')
    def test_create_episode_connection_error(self, mock_post):
        """Test handling of connection error during create_episode."""
        mock_post.side_effect = requests.exceptions.ConnectionError("Connection refused")

        client = CerebroClient()

        with pytest.raises(requests.exceptions.ConnectionError):
            client.create_episode(content="Test", tags=["test"])

    @patch('requests.Session.post')
    def test_search_episodes_timeout_error(self, mock_post):
        """Test handling of timeout error during search."""
        mock_post.side_effect = requests.exceptions.Timeout("Request timeout")

        client = CerebroClient()

        with pytest.raises(requests.exceptions.Timeout):
            client.search_episodes(query="test")

    @patch('requests.Session.get')
    def test_get_recent_episodes_http_error(self, mock_get):
        """Test handling of HTTP error (4xx/5xx)."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Internal Server Error")
        mock_get.return_value = mock_response

        client = CerebroClient()

        with pytest.raises(requests.exceptions.HTTPError):
            client.get_recent_episodes()
