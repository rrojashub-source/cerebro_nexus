"""
Neo4j Sync Module

Synchronizes episodes from PostgreSQL to Neo4j Knowledge Graph in real-time.

Design:
- NON-BLOCKING: Neo4j failures do NOT fail the API endpoint
- NON-CRITICAL: PostgreSQL is the source of truth
- REAL-TIME: Sync happens immediately after episode creation
- SIMPLE: Direct write, no queues or cron jobs

Usage:
    from api.neo4j_sync import neo4j_sync

    # After PostgreSQL INSERT:
    neo4j_sync.sync_episode(
        episode_id=episode_id,
        content=content,
        importance_score=importance_score,
        tags=tags,
        created_at=created_at
    )
"""

import sys
import os
import logging
from datetime import datetime
from typing import List, Optional

# Import GraphBuilder from local copy
from graph_builder import GraphBuilder


# Configure logging
logger = logging.getLogger(__name__)


class Neo4jSync:
    """
    Real-time Neo4j synchronization for episodic memory

    Features:
    - Sync episodes to Knowledge Graph immediately after PostgreSQL INSERT
    - Non-blocking: Errors are logged but don't fail the API
    - Uses existing GraphBuilder from NEXUS_CREW
    - Singleton pattern for connection pooling
    """

    def __init__(
        self,
        uri: str = "bolt://nexus_neo4j:7687",
        username: str = "neo4j",
        password: str = "password123"
    ):
        """
        Initialize Neo4j connection

        Args:
            uri: Neo4j bolt URI (default: bolt://nexus_neo4j:7687)
            username: Neo4j username (default: neo4j)
            password: Neo4j password (default: password123)
        """
        self.uri = uri
        self.username = username
        self.password = password
        self.graph_builder = None
        self._initialize_connection()

    def _initialize_connection(self):
        """Initialize GraphBuilder connection (lazy loading)"""
        try:
            self.graph_builder = GraphBuilder(
                uri=self.uri,
                username=self.username,
                password=self.password
            )
            logger.info(f"✅ Neo4j connection initialized: {self.uri}")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Neo4j connection: {e}")
            self.graph_builder = None

    def sync_episode(
        self,
        episode_id: str,
        content: str,
        importance_score: float,
        tags: List[str],
        created_at: datetime
    ) -> bool:
        """
        Sync episode to Neo4j Knowledge Graph

        Args:
            episode_id: Episode UUID from PostgreSQL
            content: Episode content
            importance_score: Importance score (0.0-1.0)
            tags: List of tags
            created_at: Creation timestamp

        Returns:
            True if sync successful, False if failed

        Note:
            This method NEVER raises exceptions - it's designed to be
            non-blocking for the API endpoint.
        """
        # Skip if GraphBuilder failed to initialize
        if not self.graph_builder:
            logger.warning(f"⚠️ Neo4j sync skipped (no connection): {episode_id}")
            return False

        try:
            # Prepare episode data for GraphBuilder
            episode_data = {
                'episode_id': episode_id,
                'content': content,
                'importance_score': importance_score,
                'tags': tags if tags else [],
                'created_at': created_at
            }

            # Sync to Neo4j using GraphBuilder
            success = self.graph_builder.create_episode_node(episode_data)

            if success:
                logger.info(f"✅ Neo4j sync SUCCESS: {episode_id} (tags: {len(tags)})")
                return True
            else:
                logger.warning(f"⚠️ Neo4j sync returned False: {episode_id}")
                return False

        except Exception as e:
            # LOG pero NO fallar - PostgreSQL es source of truth
            logger.error(f"❌ Neo4j sync FAILED for {episode_id}: {e}")
            return False

    def health_check(self) -> dict:
        """
        Check Neo4j connection health

        Returns:
            Dict with status and details
        """
        if not self.graph_builder:
            return {
                'status': 'unhealthy',
                'message': 'GraphBuilder not initialized'
            }

        try:
            # Try a simple query to verify connection
            with self.graph_builder.driver.session() as session:
                result = session.run("RETURN 1 AS test")
                result.single()

            return {
                'status': 'healthy',
                'uri': self.uri
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'message': str(e)
            }

    def close(self):
        """Close Neo4j connection"""
        if self.graph_builder:
            self.graph_builder.close()
            logger.info("🔌 Neo4j connection closed")


# Global singleton instance
# Initialized once when module is imported
neo4j_sync = Neo4jSync()
