"""
CerebroClient - HTTP client for CEREBRO API

Session 14: NEXUS_CREW Integration
Implements: HTTP communication with CEREBRO_NEXUS_V3.0.0 API
"""

from typing import Dict, List, Optional
import requests


class CerebroClient:
    """
    HTTP client for CEREBRO_NEXUS_V3.0.0 API.

    Provides methods to:
    - Create episodes
    - Search episodes
    - Get recent episodes
    - Check health status
    """

    def __init__(self, base_url: str = "http://localhost:8003"):
        """
        Initialize CEREBRO client.

        Args:
            base_url: Base URL of CEREBRO API (default: http://localhost:8003)
        """
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def create_episode(
        self,
        content: str,
        tags: List[str],
        current_emotion: str = "neutral",
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Create episode in CEREBRO.

        Args:
            content: Episode content (text)
            tags: List of tags for categorization
            current_emotion: Current emotional state (default: "neutral")
            metadata: Optional metadata dictionary

        Returns:
            Dict with keys: success, episode_id, timestamp, message

        Raises:
            requests.exceptions.ConnectionError: If CEREBRO is unreachable
            requests.exceptions.Timeout: If request times out
            requests.exceptions.HTTPError: If HTTP error occurs
        """
        url = f"{self.base_url}/memory/action"

        # Prepare action_details with content and emotion
        action_details = {
            "content": content,
            "current_emotion": current_emotion
        }

        if metadata:
            action_details.update(metadata)

        # Build payload according to MemoryActionRequest schema
        payload = {
            "action_type": "agent_episode",  # Type identifier for agent-created episodes
            "action_details": action_details,
            "tags": tags
        }

        response = self.session.post(url, json=payload)
        response.raise_for_status()

        return response.json()

    def search_episodes(
        self,
        query: str,
        limit: int = 10
    ) -> List[Dict]:
        """
        Search episodes by query (semantic search).

        Args:
            query: Search query string
            limit: Maximum number of results (default: 10)

        Returns:
            List of episode dictionaries with keys: episode_id, content, similarity

        Raises:
            requests.exceptions.ConnectionError: If CEREBRO is unreachable
            requests.exceptions.Timeout: If request times out
            requests.exceptions.HTTPError: If HTTP error occurs
        """
        url = f"{self.base_url}/memory/search"

        payload = {
            "query": query,
            "limit": limit
        }

        response = self.session.post(url, json=payload)
        response.raise_for_status()

        result = response.json()
        return result.get("episodes", [])

    def get_recent_episodes(
        self,
        limit: int = 10,
        tag_filter: Optional[str] = None
    ) -> List[Dict]:
        """
        Get recent episodes, optionally filtered by tag.

        Args:
            limit: Maximum number of episodes (default: 10)
            tag_filter: Optional tag to filter by (e.g., "shared_with_crew")

        Returns:
            List of episode dictionaries

        Raises:
            requests.exceptions.ConnectionError: If CEREBRO is unreachable
            requests.exceptions.Timeout: If request times out
            requests.exceptions.HTTPError: If HTTP error occurs
        """
        url = f"{self.base_url}/memory/episodic/recent"

        params = {"limit": limit}
        if tag_filter:
            params["tag_filter"] = tag_filter

        response = self.session.get(url, params=params)
        response.raise_for_status()

        result = response.json()
        return result.get("episodes", [])

    def get_consciousness_state(self) -> Dict:
        """
        Get current consciousness state (8D emotional + 7D somatic).

        Returns:
            Dict with keys: emotional_state, somatic_state, timestamp

        Raises:
            requests.exceptions.ConnectionError: If CEREBRO is unreachable
            requests.exceptions.Timeout: If request times out
            requests.exceptions.HTTPError: If HTTP error occurs
        """
        url = f"{self.base_url}/consciousness/current"

        response = self.session.get(url)
        response.raise_for_status()

        return response.json()

    def health_check(self) -> bool:
        """
        Check if CEREBRO is healthy and reachable.

        Returns:
            True if healthy, False otherwise
        """
        try:
            url = f"{self.base_url}/health"
            response = self.session.get(url, timeout=5)
            return response.status_code == 200
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.RequestException
        ):
            return False
